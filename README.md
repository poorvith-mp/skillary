<p align="center"><img src="docs/assets/logo.svg" width="88" alt="Skillary logo"></p>

# skillary

![Skillary — focused skills for AI agents](docs/assets/cover.svg)

Central index for the Claude skills multi-repo library by [@poorvith-mp](https://github.com/poorvith-mp).

- Version: **v4.0.0**
- Last updated: **September 2026**
- License: **MIT**
- Total skills (all category repos): **277**

Each category is its own repo and its own installable plugin, so you take only the domains you want.

---

## Category repositories

<!-- BEGIN:REPOS -->

| Category | Repository | Skills |
|----------|------------|--------|
| Developer | [skills-developer](https://github.com/poorvith-mp/skills-developer) | 58 |
| Marketing | [skills-marketing](https://github.com/poorvith-mp/skills-marketing) | 44 |
| Game Dev | [skills-gamedev](https://github.com/poorvith-mp/skills-gamedev) | 26 |
| Business | [skills-business](https://github.com/poorvith-mp/skills-business) | 23 |
| Design | [skills-design](https://github.com/poorvith-mp/skills-design) | 21 |
| Education | [skills-education](https://github.com/poorvith-mp/skills-education) | 21 |
| Agents | [skills-agents](https://github.com/poorvith-mp/skills-agents) | 17 |
| Personal | [skills-personal](https://github.com/poorvith-mp/skills-personal) | 15 |
| Writing | [skills-writing](https://github.com/poorvith-mp/skills-writing) | 15 |
| Sales & Support | [skills-sales](https://github.com/poorvith-mp/skills-sales) | 14 |
| Finance | [skills-finance](https://github.com/poorvith-mp/skills-finance) | 12 |
| Legal | [skills-legal](https://github.com/poorvith-mp/skills-legal) | 11 |

**Total: 277 skills across 12 repositories.**

<!-- END:REPOS -->

## Multi-Agent Orchestration
 
Multi-agent orchestration and protocol roles live in [skillary-agents](https://github.com/poorvith-mp/skillary-agents):
- **Autonomous agent runtimes** — host-neutral multi-agent orchestrator protocol and zero-slug role templates.
- **Playbooks & state machines** — shared context, task handoffs, and verification loops across agent teams.

---

## Install

This repo is an index and a plugin marketplace. It contains no skills itself — each category lives in its own repo.

### Claude Code

```bash
/plugin marketplace add poorvith-mp/skillary
/plugin install skills-finance@skillary
```

### Codex, Cursor, Gemini CLI and 70+ other agents

`npx skills` reads the manifests in these repos, so no custom installer is needed:

```bash
npx skills add poorvith-mp/skills-finance
npx skills add poorvith-mp/skills-finance/fp-and-a-analyst   # one skill
npx skills add poorvith-mp/skills-finance -g                 # user-global
```

### Manual

Clone the **category** repo, not this one, then copy the folder you want:

```bash
git clone https://github.com/poorvith-mp/skills-finance
cp -R skills-finance/skills/fp-and-a-analyst ~/.claude/skills/
```

| Agent | Personal | Project |
|-------|----------|---------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.agents/skills/` |
| VS Code / Copilot | `~/.copilot/skills/` | `.github/skills/` |

`.agents/skills/` is the emerging vendor-neutral path that several agents read.

### Claude.ai
Every skill ships a `<skill-id>.skill` bundle. Upload it via **Settings → Capabilities → Skills**.

---

## Conventions

All skills adhere to the official **Agent Skills Specification** (`agentskills.io`):

```text
skill-id/
├── SKILL.md       # Metadata + Progressive execution instructions
├── references/    # Optional: Deep domain references (loaded on-demand)
├── scripts/       # Optional: Executable automation scripts
└── assets/        # Optional: Schemas, templates, fixtures
```

`scripts/` and `assets/` are part of the spec but are not yet used across this library.

## Quality

A file-level audit across all 277 skills in September 2026 found that earlier releases contained stubs, mismatched QA checklists, and truncated trigger clauses. Everything found has been fixed:

| Defect | Was | Now |
|---|---:|---:|
| Skills shipped as import-failure stubs | 30 | 0 |
| Wrong-domain QA checklists (finance skills verifying that code compiles) | 281 | 0 |
| Descriptions over the ~250-char listing limit, trigger clause cut off | 228 | 0 |
| Descriptions ending in generated boilerplate | 180 | 0 |
| Triggers that just restate the skill's own name | 148 | 0 |
| No trigger clause in the visible part of the description | 60 | 0 |
| Reference files the body never links, so they can never load | 13 | 0 |

Enforced by `scripts/validate.py`, which reports zero findings across all 277 skills. Run it yourself:

```bash
python scripts/validate.py
```

Skills that overlap each other now name their sibling in the description (`financial-analyst` says "Not for budget-vs-actual variance work — use `fp-and-a-analyst`"), so routing between similar skills is deliberate rather than arbitrary. `scripts/overlap.py --regress` enforces that.

Still open: no skill ships `scripts/` or `assets/` yet, so every skill is instructions rather than executable capability.

---

## Full skill index

<!-- BEGIN:INDEX -->

### Developer — [skills-developer](https://github.com/poorvith-mp/skills-developer) (58 skills)

| Skill ID | Title |
|----------|-------|
| `accessibility-fix` | Accessibility Fix |
| `api-design` | API Design |
| `audit-readiness` | Audit Readiness |
| `authentication` | Authentication |
| `backend-build` | Backend Build |
| `branching-strategy` | Branching Strategy |
| `change-notes` | Change Notes |
| `ci-pipelines` | CI Pipelines |
| `cloud-cost` | Cloud Cost |
| `cloud-security` | Cloud Security |
| `code-review` | Code Review |
| `codebase-map` | Codebase Map |
| `commerce-platform` | Commerce Platform |
| `data-pipelines` | Data Pipelines |
| `database` | Database |
| `debugging` | Debugging |
| `dependency-audit` | Dependency Audit |
| `deployment` | Deployment |
| `developer-platform` | Developer Platform |
| `error-handling` | Error Handling |
| `firmware` | Firmware |
| `frontend-build` | Frontend Build |
| `git-operations` | Git Operations |
| `github-workflow` | Github Workflow |
| `implementation-plan` | Implementation Plan |
| `incident-response` | Incident Response |
| `infrastructure` | Infrastructure |
| `job-scheduling` | Job Scheduling |
| `llm-evals` | Llm Evals |
| `load-testing` | Load Testing |
| `migration` | Migration |
| `minimal-diff` | Minimal Diff |
| `ml-deployment` | Ml Deployment |
| `mobile-build` | Mobile Build |
| `model-audit` | Model Audit |
| `monorepo` | Monorepo |
| `pen-test` | Pen Test |
| `performance-audit` | Performance Audit |
| `port-code` | Port Code |
| `prototype` | Prototype |
| `realtime-systems` | Realtime Systems |
| `refactor` | Refactor |
| `regex` | Regex |
| `reliability` | Reliability |
| `repo-docs` | Repo Docs |
| `salesforce` | Salesforce |
| `secrets-management` | Secrets Management |
| `security-review` | Security Review |
| `smart-contract-audit` | Smart Contract Audit |
| `smart-contracts` | Smart Contracts |
| `solution-exploration` | Solution Exploration |
| `spec-writing` | Spec Writing |
| `speech-pipelines` | Speech Pipelines |
| `stack-choice` | Stack Choice |
| `system-design` | System Design |
| `test-suite` | Test Suite |
| `threat-detection` | Threat Detection |
| `webhooks` | Webhooks |

### Marketing — [skills-marketing](https://github.com/poorvith-mp/skills-marketing) (44 skills)

| Skill ID | Title |
|----------|-------|
| `activation` | Activation |
| `ad-creative` | Ad Creative |
| `ai-visibility` | AI Visibility |
| `analytics-setup` | Analytics Setup |
| `app-store-optimization` | App Store Optimization |
| `article-writing` | Article Writing |
| `attribution` | Attribution |
| `behavioral-levers` | Behavioral Levers |
| `community` | Community |
| `competitive-intel` | Competitive Intel |
| `content-strategy` | Content Strategy |
| `conversion-audit` | Conversion Audit |
| `customer-research` | Customer Research |
| `directory-submissions` | Directory Submissions |
| `experimentation` | Experimentation |
| `free-tools` | Free Tools |
| `growth-loops` | Growth Loops |
| `growth-plan` | Growth Plan |
| `landing-copy` | Landing Copy |
| `launch` | Launch |
| `lead-magnets` | Lead Magnets |
| `lifecycle-messaging` | Lifecycle Messaging |
| `link-building` | Link Building |
| `marketing-council` | Marketing Council |
| `marketing-report` | Marketing Report |
| `naming` | Naming |
| `offer-design` | Offer Design |
| `page-scale` | Page Scale |
| `paid-campaigns` | Paid Campaigns |
| `partnerships` | Partnerships |
| `positioning` | Positioning |
| `pricing` | Pricing |
| `public-relations` | Public Relations |
| `referrals` | Referrals |
| `retention` | Retention |
| `revops` | Revops |
| `sales-enablement` | Sales Enablement |
| `seo-audit` | SEO Audit |
| `social-content` | Social Content |
| `social-listening` | Social Listening |
| `unit-economics` | Unit Economics |
| `upgrade-paths` | Upgrade Paths |
| `video-production` | Video Production |
| `visual-assets` | Visual Assets |

### Game Dev — [skills-gamedev](https://github.com/poorvith-mp/skills-gamedev) (26 skills)

| Skill ID | Title |
|----------|-------|
| `anti-cheat` | Anti Cheat |
| `blender-animation` | Blender Animation |
| `blender-modeling` | Blender Modeling |
| `blender-tooling` | Blender Tooling |
| `game-ai` | Game AI |
| `game-audio` | Game Audio |
| `game-build-pipeline` | Game Build Pipeline |
| `game-design` | Game Design |
| `game-ideation` | Game Ideation |
| `game-monetization` | Game Monetization |
| `game-performance` | Game Performance |
| `game-ui` | Game UI |
| `game-version-control` | Game Version Control |
| `level-design` | Level Design |
| `narrative-design` | Narrative Design |
| `playtesting` | Playtesting |
| `production-planning` | Production Planning |
| `tech-art` | Tech Art |
| `unity-architecture` | Unity Architecture |
| `unity-multiplayer` | Unity Multiplayer |
| `unity-shaders` | Unity Shaders |
| `unity-tooling` | Unity Tooling |
| `unreal-multiplayer` | Unreal Multiplayer |
| `unreal-systems` | Unreal Systems |
| `unreal-tech-art` | Unreal Tech Art |
| `unreal-worlds` | Unreal Worlds |

### Business — [skills-business](https://github.com/poorvith-mp/skills-business) (23 skills)

| Skill ID | Title |
|----------|-------|
| `alliances` | Alliances |
| `board-reporting` | Board Reporting |
| `business-plan` | Business Plan |
| `business-strategy` | Business Strategy |
| `change-management` | Change Management |
| `chief-of-staff` | Chief Of Staff |
| `decision-making` | Decision Making |
| `fundraising` | Fundraising |
| `hiring` | Hiring |
| `internal-reporting` | Internal Reporting |
| `investor-deck` | Investor Deck |
| `market-trends` | Market Trends |
| `negotiation` | Negotiation |
| `okrs` | Okrs |
| `operations` | Operations |
| `portfolio-ops` | Portfolio Ops |
| `process-redesign` | Process Redesign |
| `product-management` | Product Management |
| `project-planning` | Project Planning |
| `sprint-planning` | Sprint Planning |
| `supply-chain` | Supply Chain |
| `team-dynamics` | Team Dynamics |
| `vendor-selection` | Vendor Selection |

### Design — [skills-design](https://github.com/poorvith-mp/skills-design) (21 skills)

| Skill ID | Title |
|----------|-------|
| `accessibility-review` | Accessibility Review |
| `brand-system` | Brand System |
| `color-psychology` | Color Psychology |
| `color-system` | Color System |
| `component-library` | Component Library |
| `delight` | Delight |
| `design-critique` | Design Critique |
| `design-direction` | Design Direction |
| `design-taste` | Design Taste |
| `frontend-design` | Frontend Design |
| `icon-design` | Icon Design |
| `image-prompts` | Image Prompts |
| `information-architecture` | Information Architecture |
| `interactive-prototype` | Interactive Prototype |
| `motion-design` | Motion Design |
| `print-packaging` | Print Packaging |
| `responsive-rules` | Responsive Rules |
| `type-system` | Type System |
| `ui-copy` | UI Copy |
| `ui-design` | UI Design |
| `ux-research` | UX Research |

### Education — [skills-education](https://github.com/poorvith-mp/skills-education) (21 skills)

| Skill ID | Title |
|----------|-------|
| `academic-project` | Academic Project |
| `active-recall` | Active Recall |
| `assessment-design` | Assessment Design |
| `citations` | Citations |
| `concept-explainer` | Concept Explainer |
| `essay-structure` | Essay Structure |
| `exam-strategy` | Exam Strategy |
| `flashcards` | Flashcards |
| `learning-roadmap` | Learning Roadmap |
| `literature-review` | Literature Review |
| `mentoring` | Mentoring |
| `mind-maps` | Mind Maps |
| `mock-exams` | Mock Exams |
| `paper-summary` | Paper Summary |
| `quizzes` | Quizzes |
| `research` | Research |
| `research-methods` | Research Methods |
| `source-evaluation` | Source Evaluation |
| `study-plan` | Study Plan |
| `topic-selection` | Topic Selection |
| `training-design` | Training Design |

### Agents — [skills-agents](https://github.com/poorvith-mp/skills-agents) (17 skills)

| Skill ID | Title |
|----------|-------|
| `agent-architecture` | Agent Architecture |
| `agent-identity` | Agent Identity |
| `agent-orchestration` | Agent Orchestration |
| `agent-safety` | Agent Safety |
| `automation-review` | Automation Review |
| `composio` | Composio |
| `create-skill` | Create Skill |
| `document-generation` | Document Generation |
| `mcp-builder` | MCP Builder |
| `n8n` | N8n |
| `prompt-engineering` | Prompt Engineering |
| `prompt-library` | Prompt Library |
| `rag-systems` | Rag Systems |
| `report-automation` | Report Automation |
| `skill-linter` | Skill Linter |
| `trigger-dev` | Trigger Dev |
| `workflow-mapping` | Workflow Mapping |

### Personal — [skills-personal](https://github.com/poorvith-mp/skills-personal) (15 skills)

| Skill ID | Title |
|----------|-------|
| `3d-printing` | 3D Printing |
| `fitness-nutrition` | Fitness Nutrition |
| `habits` | Habits |
| `interview-prep` | Interview Prep |
| `job-search` | Job Search |
| `linkedin-profile` | Linkedin Profile |
| `note-system` | Note System |
| `periodic-review` | Periodic Review |
| `personal-context` | Personal Context |
| `personal-crm` | Personal CRM |
| `personal-finance` | Personal Finance |
| `productivity-audit` | Productivity Audit |
| `resume` | Resume |
| `travel-planning` | Travel Planning |
| `voice-profile` | Voice Profile |

### Writing — [skills-writing](https://github.com/poorvith-mp/skills-writing) (15 skills)

| Skill ID | Title |
|----------|-------|
| `book-writing` | Book Writing |
| `executive-summary` | Executive Summary |
| `feedback-writing` | Feedback Writing |
| `grant-writing` | Grant Writing |
| `historical-accuracy` | Historical Accuracy |
| `job-descriptions` | Job Descriptions |
| `line-editing` | Line Editing |
| `meeting-notes` | Meeting Notes |
| `screenwriting` | Screenwriting |
| `sop-writing` | SOP Writing |
| `talk-writing` | Talk Writing |
| `technical-docs` | Technical Docs |
| `thread-to-article` | Thread To Article |
| `translation` | Translation |
| `writing-taste` | Writing Taste |

### Sales & Support — [skills-sales](https://github.com/poorvith-mp/skills-sales) (14 skills)

| Skill ID | Title |
|----------|-------|
| `account-management` | Account Management |
| `client-onboarding` | Client Onboarding |
| `cold-outreach` | Cold Outreach |
| `discovery` | Discovery |
| `freelance-bidding` | Freelance Bidding |
| `pipeline-health` | Pipeline Health |
| `proposals` | Proposals |
| `prospecting` | Prospecting |
| `public-sector-bids` | Public Sector Bids |
| `renewals` | Renewals |
| `sales-coaching` | Sales Coaching |
| `solution-engineering` | Solution Engineering |
| `support-replies` | Support Replies |
| `win-loss-analysis` | Win Loss Analysis |

### Finance — [skills-finance](https://github.com/poorvith-mp/skills-finance) (12 skills)

| Skill ID | Title |
|----------|-------|
| `accounts-payable` | Accounts Payable |
| `bookkeeping` | Bookkeeping |
| `budgeting` | Budgeting |
| `cap-table` | Cap Table |
| `crypto-tax` | Crypto Tax |
| `finance-strategy` | Finance Strategy |
| `financial-modeling` | Financial Modeling |
| `investment-research` | Investment Research |
| `invoicing` | Invoicing |
| `runway-planning` | Runway Planning |
| `saas-metrics` | Saas Metrics |
| `tax-strategy` | Tax Strategy |

### Legal — [skills-legal](https://github.com/poorvith-mp/skills-legal) (11 skills)

| Skill ID | Title |
|----------|-------|
| `ai-governance` | AI Governance |
| `company-formation` | Company Formation |
| `contract-drafting` | Contract Drafting |
| `contract-review` | Contract Review |
| `data-privacy` | Data Privacy |
| `employment-law` | Employment Law |
| `esg-reporting` | ESG Reporting |
| `ip-protection` | Ip Protection |
| `legal-documents` | Legal Documents |
| `open-source-licensing` | Open Source Licensing |
| `regulatory-compliance` | Regulatory Compliance |

<!-- END:INDEX -->
