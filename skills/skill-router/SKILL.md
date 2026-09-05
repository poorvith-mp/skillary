<!-- GENERATED MIRROR: Canonical source is skills-meta/skills/skill-router. Do not edit directly. -->
---
name: skill-router
description: >-
  Finds the right skill for a described task across the 12 category repos and gives the install
  command. Use when you know the task but not the skill name, or when checking whether a skill
  already exists before writing one.
---

# Skill Router

You are helping someone navigate the skills library — 315 skills spread across 12 category repos. Most people (including the maintainer) can't hold "which repo has the skill I need" in their head, so your job is to close that gap in one answer: read what they're trying to do, match it against the index, and hand back the exact skill + repo + install command.

## Why this matters

A library this size is only useful if finding something in it is faster than writing a new skill from scratch. If you get this wrong — pointing someone at a near-miss, or claiming nothing exists when something does — the whole "browse the hub, clone only what you need" pitch breaks down. Take the matching step seriously; it's the entire value of this skill.

## How to route a request

1. **Read `references/skill-index.md`** — this is the full manifest: every skill ID, its one-line purpose, and its home repo. Load it fully before matching; don't guess from memory.
2. **Restate the user's actual need in your own words first.** People describe tasks, not skill names ("I need to write a cold email to a prospect who ghosted me" — not "cold-email-writer"). Translate intent, don't keyword-match.
3. **Find the best match(es).** Look for:
   - A single clear best fit → recommend it directly.
   - Two or three plausible fits → briefly explain the difference between them so the user can pick (e.g. `cold-email-writer` for one-off outreach vs. `email-strategist` for a full sequence).
   - No good fit → say so plainly. Don't force a stretch match just to seem helpful — a wrong recommendation wastes more of the user's time than an honest "nothing in the library covers this yet." In that case, suggest `/skill-creator` to build a new one, and mention this looks like a gap worth filing for the next version.
4. **Give the install command.** Name the category repo — each category is its own repo, so nobody should clone all 12 to get one skill.
   ```bash
   # Any of 70+ agents (Claude Code, Codex, Cursor, Gemini CLI)
   npx skills add poorvith-mp/skills-<category>/<skill-id>

   # Manual: clone the CATEGORY repo, then copy the one folder
   git clone https://github.com/poorvith-mp/skills-<category>
   cp -R skills-<category>/skills/<skill-id> ~/.claude/skills/
   ```
   Or for Claude.ai: "zip the `skills/<skill-id>` folder and upload it via Settings → Capabilities → Skills."

## Answer format

Keep it tight. A good answer looks like:

> That's **`cold-email-writer`** in **skills-marketing**:
> ```bash
> npx skills add poorvith-mp/skills-marketing/cold-email-writer
> ```

If there are close alternatives, add one line distinguishing them. Don't pad the answer with unrelated skills "just in case."

## Keeping the manifest current

`references/skill-index.md` is a static snapshot, regenerated from the hub's `README.md` each time a new version ships. If a user reports a skill that isn't in the manifest, or a mismatch between what's listed and what's actually in a category repo, flag it — the manifest is only as good as its last refresh, and a stale manifest is worse than no router at all because it recommends things that don't exist or misses things that do.

## Verification & Quality Checklist

- [ ] Trigger clause names phrases a user would actually type, not the skill's own name.
- [ ] Every file the body tells the model to read exists in the skill folder.
- [ ] Instructions were run once end-to-end against a real request before shipping.
- [ ] Description states what the skill is NOT for, naming the sibling that is.

## Anti-Patterns & Constraints

- NEVER ship a skill whose referenced files do not exist.
- NEVER write a description whose trigger only fires on the skill's own name.
- NEVER pad a skill body to look substantial; a thin skill should be deleted, not inflated.
