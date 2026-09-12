"""Find skills whose triggers collide, and say which phrases they collide on.

Not TF-IDF. Cosine similarity over descriptions was tried first and fails on
this corpus: `chief-financial-officer` and `fp-and-a-analyst` score 0.219 and
never surface, because they collide on the concepts they *claim* (which live in
the body) rather than on description vocabulary. Feeding bodies to TF-IDF makes
it worse - shared boilerplate ranks unrelated pairs highly.

What works is a rare-n-gram concept-collision index. Extract multi-word phrases,
keep only those owned by a handful of skills (a phrase in one skill is that
skill's own territory; a phrase in thirty is a domain word), and score each pair
by how rare its shared phrases are. The output is a worklist naming the literal
colliding phrases, which is what you actually need to write a "Do NOT use for"
boundary.

Usage:
    python scripts/overlap.py                          # markdown worklist
    python scripts/overlap.py --min-score 4            # longer tail
    python scripts/overlap.py --json > work/overlap.json
    python scripts/overlap.py --check-boundaries       # CI: every cluster names a sibling
    python scripts/overlap.py --regress work/overlap.json    # same, plus score movement
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from skillary import iter_skills, strip_boilerplate_tail  # noqa: E402

# Sections that exist in nearly every skill and say nothing distinguishing.
# Leaving them in is what produced the nonsense `it-service-manager` /
# `email-strategist` pairing when this was first tried with TF-IDF.
GENERIC_SECTIONS = re.compile(
    r"^##+\s*(?:[^\w\s]*\s*)?(Output format|Critical Rules|Verification"
    r"|Anti-Patterns|What NOT to do|Phased Workflow|Success Metrics"
    r"|(?:Your )?Core Mission|Additional notes|Final note)\b.*?(?=^##+\s|\Z)",
    re.M | re.S | re.I,
)

# Heading-based stripping is not enough on its own: the same stamped lines turn
# up under `## Output format` in most skills and `## Additional notes (merged)`
# in others. Scoring on them paired `code-reviewer` with `technical-writer` at
# 16.1, which is meaningless. Drop the lines by content, wherever they sit.
BOILERPLATE_LINES = [
    "Lead with the result the user asked for",
    "Use clear headings and bullet lists where helpful",
    "Call out assumptions and open questions at the end",
    "avoid generic filler",
    "Code compiles cleanly and passes all automated tests",
    "Edge cases, boundary conditions, and error states handled explicitly",
    "No hardcoded secrets, test credentials, or insecure defaults",
    "Performance and resource utilization verified against baseline",
    "NEVER bypass automated tests or typecheckers",
    "NEVER leave unhandled promise rejections",
    "NEVER introduce breaking API changes",
]


def drop_boilerplate_lines(text: str) -> str:
    keep = [
        line
        for line in text.splitlines()
        if not any(fragment in line for fragment in BOILERPLATE_LINES)
    ]
    return "\n".join(keep)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "in",
    "into", "is", "it", "its", "of", "on", "or", "that", "the", "their", "them",
    "then", "there", "these", "they", "this", "to", "use", "used", "using",
    "was", "were", "when", "which", "with", "you", "your", "user", "users",
    "skill", "skills", "need", "needs", "also", "any", "each", "how", "what",
    "who", "why", "can", "will", "should", "must", "not", "no", "all", "one",
    "two", "three", "more", "most", "other", "such", "own", "same", "so", "than",
}

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z&/+-]*")

# A phrase held by 1 skill is unique; a phrase held by many is a domain word.
# Genuine trigger collisions live in the band between.
MIN_OWNERS = 2
MAX_OWNERS = 8

# Multiplier per side that claims a concept in its description rather than only
# in its body. Concepts marked `*` in the worklist are claimed by both sides.
# Kept modest deliberately: at 3.0 the scores inflate enough that union-find
# chains unrelated skills into a single 23-member component spanning business,
# finance, data and marketing, which is not an actionable worklist.
DESCRIPTION_WEIGHT = 1.0

# A connected component larger than this means a generic concept leaked into the
# discriminative band and chained unrelated skills together. Report it, don't
# pretend it is one overlap to resolve.
MAX_CLUSTER = 6


def concepts(text: str) -> set[str]:
    """Multi-word phrases plus substantial unigrams, minus stopword edges."""
    out: set[str] = set()
    for sentence in re.split(r"[.\n;:!?]", text.lower()):
        tokens = TOKEN_RE.findall(sentence)
        for size in (1, 2, 3):
            for i in range(len(tokens) - size + 1):
                gram = tokens[i : i + size]
                if gram[0] in STOPWORDS or gram[-1] in STOPWORDS:
                    continue
                if size == 1 and len(gram[0]) <= 4:
                    continue
                out.add(" ".join(gram))
    return out


# Two skills that both embed an HTML table "collide" on `tr td` / `td td td`.
# That paired design/dark-mode-adapter with finance/financial-plan-starter at
# 9.0. Code samples are not claimed territory - drop them before scoring.
FENCED_CODE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)

# Some skills embed raw HTML tables inline rather than in a fence - and in the
# leaked-frontmatter cases, inside the description itself. Same problem: markup
# is not claimed territory.
HTML_TAG = re.compile(r"<[^>]{1,200}>")


def signal_text(skill) -> str:
    body = FENCED_CODE.sub("", skill.body)
    body = drop_boilerplate_lines(GENERIC_SECTIONS.sub("", body))
    text = f"{strip_boilerplate_tail(skill.description)}\n{body}"
    return HTML_TAG.sub(" ", text)


class Union:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def join(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def build(min_score: float = 10.0, skills: dict[str, Skill] | list[Skill] | None = None):
    if skills is None:
        skills = {s.rel: s for s in iter_skills()}
    elif isinstance(skills, list):
        skills = {s.rel: s for s in skills}
    owners: dict[str, set[str]] = defaultdict(set)
    # Concepts that appear in the description are what Claude actually matches
    # on when choosing a skill, so a collision there is worth more than one
    # buried in the body. Without this, a terse skill like
    # `chief-financial-officer` scores 0.58 against `fp-and-a-analyst` and never
    # surfaces, even though their descriptions both claim FP&A and forecasting.
    in_description: dict[str, set[str]] = defaultdict(set)
    for rel, skill in skills.items():
        desc_concepts = concepts(strip_boilerplate_tail(skill.description))
        for concept in concepts(signal_text(skill)):
            owners[concept].add(rel)
            if concept in desc_concepts:
                in_description[concept].add(rel)

    discriminative = {
        concept: sorted(who)
        for concept, who in owners.items()
        if MIN_OWNERS <= len(who) <= MAX_OWNERS and " " in concept
    }

    scores: dict[tuple[str, str], float] = defaultdict(float)
    shared: dict[tuple[str, str], list[str]] = defaultdict(list)
    for concept, who in discriminative.items():
        base = 1.0 / (len(who) - 1)
        for pair in combinations(who, 2):
            # Both sides claiming it in their description is the routing-level
            # collision; one side is a partial signal.
            claimed = len(in_description[concept] & set(pair))
            scores[pair] += base * (1 + DESCRIPTION_WEIGHT * claimed)
            shared[pair].append(f"{concept}*" if claimed == 2 else concept)

    pairs = sorted(
        ((p, s) for p, s in scores.items() if s >= min_score),
        key=lambda kv: -kv[1],
    )

    union = Union()
    for (a, b), _ in pairs:
        union.join(a, b)
    clusters: dict[str, set[str]] = defaultdict(set)
    for (a, b), _ in pairs:
        clusters[union.find(a)] |= {a, b}

    return skills, discriminative, pairs, shared, clusters


def find_collisions(skills: list, min_score: float = 0.5) -> list[dict]:
    """Find trigger collisions within a specific set of skills (e.g. installed set)."""
    skills_map = {}
    for s in skills:
        rel = getattr(s, "rel", None) or f"{getattr(s, 'repo', 'installed')}/skills/{s.slug}"
        skills_map[rel] = s

    owners: dict[str, set[str]] = defaultdict(set)
    in_description: dict[str, set[str]] = defaultdict(set)
    for rel, skill in skills_map.items():
        desc_concepts = concepts(strip_boilerplate_tail(skill.description))
        for concept in concepts(signal_text(skill)):
            owners[concept].add(rel)
            if concept in desc_concepts:
                in_description[concept].add(rel)

    discriminative = {
        concept: sorted(who)
        for concept, who in owners.items()
        if len(who) >= 2 and (len(skills_map) <= 20 or " " in concept)
    }

    scores: dict[tuple[str, str], float] = defaultdict(float)
    shared: dict[tuple[str, str], list[str]] = defaultdict(list)
    for concept, who in discriminative.items():
        base = 1.0 / (len(who) - 1)
        for pair in combinations(who, 2):
            claimed = len(in_description[concept] & set(pair))
            scores[pair] += base * (1 + DESCRIPTION_WEIGHT * claimed)
            shared[pair].append(concept)

    collisions = []
    for pair, score in scores.items():
        if score >= min_score:
            slug_a = skills_map[pair[0]].slug
            slug_b = skills_map[pair[1]].slug
            collisions.append({
                "pair": (slug_a, slug_b),
                "words": sorted(set(shared[pair])),
                "score": round(score, 2),
            })
    return collisions


def has_boundary(skill, all_slugs: set[str]) -> bool:
    """A boundary is a description that points at a named sibling skill.

    Matching the prose instead ("not for", "do not use for") misses the
    equally valid "For UE5 specifically, use unreal-technical-artist" and
    "Not tool setup - use second-brain-architect". Naming another skill is the
    signal; how the sentence is phrased is not.
    """
    # Match slugs directly rather than tokenising: a length filter drops short
    # but real skill names like `n8n`.
    text = skill.description.lower()
    return any(
        slug != skill.slug and re.search(rf"(?<![a-z0-9-]){re.escape(slug)}(?![a-z0-9-])", text)
        for slug in all_slugs
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # 10.0 tuned against this corpus: 14 clusters, no chained components.
    # Drop to ~6 for a longer tail once the top clusters are resolved.
    parser.add_argument("--min-score", type=float, default=10.0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--check-boundaries",
        action="store_true",
        help="fail if any clustered skill does not name a sibling",
    )
    parser.add_argument(
        "--regress",
        nargs="?",
        const="",
        help="same check, plus informational score movement against a baseline JSON",
    )
    parser.add_argument("--top-concepts", type=int, default=8)
    args = parser.parse_args()

    skills, discriminative, pairs, shared, clusters = build(args.min_score)

    if args.check_boundaries or args.regress is not None:
        # The baseline is optional: it only produces informational score
        # movement. The pass/fail criterion is boundaries, so CI does not
        # need a committed baseline file.
        worse = []
        if args.regress:
            baseline = {tuple(k.split("||")): v for k, v in json.loads(Path(args.regress).read_text()).items()}
            worse = [p for p, s in dict(pairs).items() if s > baseline.get(p, 0) + 1e-9]
        slugs = {s.slug for s in skills.values()}
        unbounded = [
            rel
            for cluster in clusters.values()
            for rel in cluster
            if not has_boundary(skills[rel], slugs)
        ]
        # Score movement alone is not failure: once two skills name each other,
        # they legitimately share vocabulary. The criterion is whether every
        # clustered skill points at its sibling.
        for pair in worse:
            print(f"note: {pair[0]} <-> {pair[1]} scores higher than baseline")
        for rel in sorted(set(unbounded)):
            print(f"NO BOUNDARY: {rel} overlaps a sibling but does not name one")
        return 1 if unbounded else 0

    if args.json:
        print(json.dumps({f"{a}||{b}": round(s, 3) for (a, b), s in pairs}, indent=2))
        return 0

    print(f"# Overlap worklist\n")
    print(f"{len(skills)} skills, {len(discriminative)} discriminative concepts, "
          f"{len(pairs)} pairs at or above {args.min_score}, {len(clusters)} clusters.\n")

    all_slugs = {s.slug for s in skills.values()}
    ordered = sorted(clusters.values(), key=lambda c: -max(
        (s for (a, b), s in pairs if a in c and b in c), default=0))

    oversized = [c for c in ordered if len(c) > MAX_CLUSTER]
    if oversized:
        print(f"> {len(oversized)} component(s) exceed {MAX_CLUSTER} members. That is chaining "
              f"through weak links, not one overlap - raise --min-score for these.\n")

    for cluster in ordered:
        members = sorted(cluster)
        best = max((s for (a, b), s in pairs if a in cluster and b in cluster), default=0)
        cross = len({rel.split("/")[0] for rel in members}) > 1
        flag = "  **[oversized - chained]**" if len(cluster) > MAX_CLUSTER else ""
        print(f"\n## {' + '.join(m.split('/')[-1] for m in members)}"
              f"{'  **[cross-repo]**' if cross else ''}{flag}  _(top pair {best:.1f})_\n")
        for rel in members:
            mark = "" if has_boundary(skills[rel], all_slugs) else "  <- no boundary"
            print(f"- `{rel}`{mark}")
        print()
        for (a, b), score in pairs:
            if a in cluster and b in cluster:
                phrases = sorted(shared[(a, b)], key=lambda c: -len(c))[: args.top_concepts]
                print(f"  - {score:6.1f}  {a.split('/')[-1]} <-> {b.split('/')[-1]}")
                print(f"            shared: {', '.join(repr(p) for p in phrases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
