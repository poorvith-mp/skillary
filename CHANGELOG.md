# Changelog

Versioning note: earlier releases used two conflicting schemes (`v0.1`/`v0.2`/`v0.3` in changelogs and commits, `v2.0` in the README and on GitHub Releases). From v2.1.0 onward there is one scheme: semver, continuing from the published v2.0.

## v4.0.0 — September 2026

Modernized architecture, 277 skills across 12 focused repositories, standalone `skillary-agents` multi-agent orchestrator, and strict 200-character description gates.

**Catalog Modernization (277 Skills Across 12 Repos)**
- **Rebalanced Collections**: Structured into 12 core category repositories: `skills-developer` (58), `skills-marketing` (44), `skills-gamedev` (26), `skills-business` (23), `skills-design` (21), `skills-education` (21), `skills-agents` (17), `skills-personal` (15), `skills-writing` (15), `skills-sales` (14), `skills-finance` (12), and `skills-legal` (11).
- **New Dedicated Repositories**: Scaffolded `skills-agents` (agent architecture, RAG, MCP, prompt engineering, n8n) and `skills-legal` (contracts, privacy, compliance, IP, licensed-review requirement).
- **Dissolved Catch-All Repos**: Retired `skills-specialized` (40 skills rehomed or deprecated) and `skills-meta` (tooling relocated to `skillary/scripts/`).
- **Category Renaming**: Promoted `skills-sales-support` to `skills-sales`.
- **Redirect Discipline**: Added deprecation stubs for legacy and renamed skills to provide non-breaking migration paths while excluding them from active index distributions.

**Autonomous Multi-Agent Orchestration (`skillary-agents`)**
- Shipped standalone `skillary-agents` repository implementing depth-1 parent-child crew dispatching across Claude Code, Google Antigravity, and Codex/Cursor CLI.
- Authored 6 zero-slug role contracts (`scout`, `planner`, `worker`, `verifier`, `security-auditor`, `shipper`) and 8 cross-category functional playbooks (`launch-business`, `sell-a-thing`, `fundraise`, `content-engine`, `ship-feature`, `codebase-rescue`, `security-review`, `hire-a-team`).

**Linter & Gate Hardening**
- **Strict Spec Limits**: Enforced 200-character hard description ceiling and 30-character kebab-case slug limit across all 277 skills.
- **Routing Evals**: Added per-skill `evals/routing.yaml` test harnesses enforcing positive triggers and neighbour disambiguation.
- **Zero Indicators**: Verified 100% clean passes on `validate.py`, `security.py` (0 security indicators), and `test_index.py` (277 indexed skills).

## v3.0.0 — September 2026

Major architecture, security, and integrity release. Enforces cross-agent portability, prunes non-target skills, hardens the supply-chain security gate, and enables direct hub installation.

**Security & Supply Chain**
- **Automated Security Scanner**: Shipped `scripts/security.py` running continuous static analysis across 24 indicators (prompt injection, hidden Unicode, base64 payloads, credential harvesting, zip traversal) asserting zero security issues across all 307 skills and bundles.
- **Supply-Chain CI Hardening**: Pinned GitHub Actions in `.github/workflows/validate.yml` to full commit SHAs with explicit `permissions: contents: read` and pinned dependencies.
- **Signed Distribution**: Added reproducible bundle archives and generated `dist/SHA256SUMS` catalog checksums.
- **Security Policy**: Added repository `SECURITY.md` defining responsible disclosure guidelines and SLAs.

**Integrity & Quality Gates**
- **Unescaped Markdown**: Cleaned 122 `SKILL.md` files corrupted by JSON round-trip escaping outside code fences (`\*`, `\[`, `\]`, `` \` ``, `\|`, etc.) and reflowed table rows containing literal `<br>`. Added permanent `escaped-markdown` and `br-in-markdown` checks to `scripts/validate.py`.
- **Dangling References Fixed**: Authored full reference documentation across 6 core skills (`composio`, `create-skill`, `n8n`, `trigger-dev`, `customer-support`, `know-me`) and stripped stale imports in `build-premium-website`, `new-client-system`, `readme-generator`, `setup-codex-precheck`, `instantly-campaign`, and `skill-router`.
- **Pruned Preview Blobs & Duplicate Titles**: Eliminated preview text welded between duplicate H1 tags in `code-reviewer`, `bug-explainer`, `git-commit-writer`, and `client-proposal-writer`. Added `truncated-blob` validator check.
- **Tooling Archetype**: Introduced `tooling` archetype in `taxonomy/checklists.yaml` and mapped meta/orchestrator skills to verify genuine skill contracts rather than irrelevant compilation checks.

**Portability & Discovery**
- **Agent Portability**: Removed `${CLAUDE_SKILL_DIR}` and vendor-specific paths (`~/.claude`), standardizing on relative Markdown paths compatible with Claude Code, Codex, Cursor, Gemini CLI, and `npx skills`.
- **Universal Hub Installation**: Added generated `skills/` mirror in the hub via `build_index.py --hub-skills`, making `npx skills add poorvith-mp/skillary` resolve directly to the router skill.
- **Catalog Pruning**: Deleted 8 China-market skills (`feishu-integration-developer`, `wechat-mini-program-developer`, `bilibili-content-strategist`, `china-e-commerce-operator`, `china-market-localization-strategist`, `wechat-official-account`, `zhihu-strategist`, `healthcare-compliance-auditor`), right-sizing the catalog from 315 to 307 high-signal skills.
- **Rehomed create-skill**: Moved `create-skill` from `skills-developer` to `skills-meta` to unify the author-lint-route workflow.

## v2.1.0 — August 2026

The release where the quality claim is actually true, and the first one you can install.

v2.0 was published as "315 production-grade skills". A file-level audit of every `SKILL.md` found that was not accurate. This fixes all of it.

**Content**

- **30 skills were import stubs.** Their body contained `Full .md body could not be fetched` instead of instructions. All 30 now have real content: an approach, an ordered process, and the deliverables they produce.
- **281 skills carried a software-engineering QA checklist regardless of domain.** Every finance and education skill was instructed to verify that its code compiles. Replaced with domain-appropriate checklists from `taxonomy/checklists.yaml`, seeded from the 32 hand-written ones already in the library. Those 32, plus 35 hand-written anti-pattern sections, were left untouched.
- **All 315 descriptions rewritten.** 228 exceeded the ~250-character listing limit with the trigger clause at the end, where it gets truncated — which is the mechanical reason skills under-fire. 180 ended in generated boilerplate that triggered on the skill's own name. Now: capability first, concrete triggers second, all inside the limit.
- **Overlapping skills name each other.** `financial-analyst` says "Not for budget-vs-actual variance work — use `fp-and-a-analyst`", and vice versa. Without that, whichever fires first is arbitrary.
- 13 reference files were never linked from their body, so they could never load. 11 skills had no title. Both fixed.

**Distribution**

- **Installable as a plugin marketplace.** `.claude-plugin/marketplace.json` lists all 12 category repos as separate plugins, each with its own `plugin.json`, so you install only the domains you want.
- **`npx skills` reads the same manifests**, so Codex, Cursor, Gemini CLI and 70+ other agents work with no custom installer.
- **Hub renamed** `open-claude-skills` → `skillary`. GitHub redirects the old URL.

**Maintenance**

- The README index, `skill-router`'s reference index, all 13 manifests and all 315 `.skill` bundles are generated by scripts in `scripts/`, not hand-maintained. The index had drifted before.
- `scripts/validate.py` enforces every rule above and reports zero findings across all 315 skills. CI runs it on every push, plus drift checks for the index, manifests and bundles.
- `skill-router` pointed at 37 skills that no longer existed and missed 210 that did. `skill-linter` required `NOTE.md` files that zero skills have ever had. Both corrected.

Still open: no skill ships `scripts/` or `assets/` yet, so all 315 are instructions rather than executable capability.

## v0.2 — July 2026

- Total skill count corrected: 319 -> 342 (index had drifted from what the category repos actually contained)
- Developer count corrected: 82 -> 88
- Business count corrected: 26 -> 29
- Marketing, Specialized, Design, Game Dev, Sales & Support, Finance counts synced to their repos' actual skill folders
- Added 29 previously-undocumented or newly-added skills to the full skill index across 11 category tables:
  `ci-cd-pipeline-builder`, `iac-provisioner`, `citation-formatter`, `budget-expense-auditor`,
  `cap-table-fundraising-modeler`, `meta-ads-copywriter`, `fitness-nutrition-planner`, `screenplay-writer`,
  `android-developer`, `ios-developer`, `graphql-api-designer`, `load-testing-engineer`,
  `dependency-upgrade-auditor`, `board-deck-builder`, `vendor-procurement-manager`, `churn-analyst`,
  `renewal-strategist`, `conversion-rate-optimizer`, `influencer-outreach-strategist`, `pinterest-strategist`,
  `crypto-tax-specialist`, `insurance-actuary-analyst`, `game-monetization-designer`, `playtest-feedback-analyzer`,
  `hiring-plan-org-chart-builder`, `regulatory-compliance-officer`, `logo-brand-mark-designer`,
  `motion-graphics-producer`, `print-packaging-designer`
- Added `skills-meta` to the category table with a proper repo link (was listed without one)
- Added CHANGELOG.md and CODE_OF_CONDUCT.md to this repo (were missing)

## v0.1 — July 2026

- Initial public hub linking all category repositories
- MIT License
