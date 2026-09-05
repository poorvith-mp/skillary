<p align="center"><img src="docs/assets/logo.svg" width="88" alt="Skillary logo"></p>

# skillary

![Skillary — focused skills for AI agents](docs/assets/cover.svg)

Central index for the Claude skills multi-repo library by [@poorvith-mp](https://github.com/poorvith-mp).

- Version: **v2.1.0**
- Last updated: **August 2026**
- License: **MIT**
- Total skills (all category repos): **315**

Each category is its own repo and its own installable plugin, so you take only the domains you want.

---

## Category repositories

<!-- BEGIN:REPOS -->

| Category | Repository | Skills |
|----------|------------|--------|
| Developer | [skills-developer](https://github.com/poorvith-mp/skills-developer) | 77 |
| Marketing | [skills-marketing](https://github.com/poorvith-mp/skills-marketing) | 47 |
| Specialized | [skills-specialized](https://github.com/poorvith-mp/skills-specialized) | 40 |
| Design | [skills-design](https://github.com/poorvith-mp/skills-design) | 29 |
| Business | [skills-business](https://github.com/poorvith-mp/skills-business) | 29 |
| Game Dev | [skills-gamedev](https://github.com/poorvith-mp/skills-gamedev) | 22 |
| Sales & Support | [skills-sales-support](https://github.com/poorvith-mp/skills-sales-support) | 17 |
| Education | [skills-education](https://github.com/poorvith-mp/skills-education) | 15 |
| Finance | [skills-finance](https://github.com/poorvith-mp/skills-finance) | 12 |
| Personal | [skills-personal](https://github.com/poorvith-mp/skills-personal) | 10 |
| Writing | [skills-writing](https://github.com/poorvith-mp/skills-writing) | 5 |
| Meta | [skills-meta](https://github.com/poorvith-mp/skills-meta) | 4 |

**Total: 307 skills across 12 repositories.**

<!-- END:REPOS -->

## Meta

`skills-meta` holds skills that operate on the library itself rather than a domain:
- **skill-router** — finds the right skill + repo for a described task, with the install command.
- **skill-linter** — checks a draft SKILL.md against house conventions before it's committed.
- **prompt-library-curator** — maintains versioned prompt template libraries across teams.

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

A file-level audit of all 315 skills in August 2026 found that the release labelled "v2.0 — production-grade" was not accurate. Everything it found has since been fixed:

| Defect | Was | Now |
|---|---:|---:|
| Skills shipped as import-failure stubs | 30 | 0 |
| Wrong-domain QA checklists (finance skills verifying that code compiles) | 281 | 0 |
| Descriptions over the ~250-char listing limit, trigger clause cut off | 228 | 0 |
| Descriptions ending in generated boilerplate | 180 | 0 |
| Triggers that just restate the skill's own name | 148 | 0 |
| No trigger clause in the visible part of the description | 60 | 0 |
| Reference files the body never links, so they can never load | 13 | 0 |

Enforced by `scripts/validate.py`, which reports zero findings across all 315 skills. Run it yourself:

```bash
python scripts/validate.py
```

Skills that overlap each other now name their sibling in the description (`financial-analyst` says "Not for budget-vs-actual variance work — use `fp-and-a-analyst`"), so routing between similar skills is deliberate rather than arbitrary. `scripts/overlap.py --regress` enforces that.

Still open: no skill ships `scripts/` or `assets/` yet, so every skill is instructions rather than executable capability.

---

## Full skill index

<!-- BEGIN:INDEX -->

### Developer — [skills-developer](https://github.com/poorvith-mp/skills-developer) (77 skills)

| Skill ID | Title |
|----------|-------|
| `accessibility-engineer` | Accessibility Engineer |
| `ai-data-remediation-engineer` | AI Data Remediation Engineer |
| `ai-engineer` | AI Engineer |
| `ai-eval-suite-builder` | AI Eval Suite Builder |
| `android-developer` | Android Developer |
| `api-lifecycle-engineer` | API Lifecycle Engineer |
| `appsec-architect` | Appsec Architect |
| `autonomous-optimization-architect` | Autonomous Optimization Architect |
| `backend-architect` | Backend Architect |
| `blockchain-security-auditor` | Blockchain Security Auditor |
| `bug-explainer` | Bug Explainer |
| `changelog-writer` | Changelog Writer |
| `ci-cd-pipeline-builder` | CI CD Pipeline Builder |
| `cloud-security-architect` | Cloud Security Architect |
| `code-comment-writer` | Code Comment Writer |
| `code-reviewer` | Code Reviewer |
| `code-translator` | Code Translator |
| `codebase-onboarding-engineer` | Codebase Onboarding Engineer |
| `compliance-auditor` | Compliance Auditor |
| `composio` | Composio |
| `cron-job-planner` | Cron Job Planner |
| `data-engineer` | Data Engineer |
| `data-pipeline-architect` | Data Pipeline Architect |
| `database-optimizer` | Database Optimizer |
| `database-schema-designer` | Database Schema Designer |
| `debugging-strategist` | Debugging Strategist |
| `dependency-upgrade-auditor` | Dependency Upgrade Auditor |
| `deployment-checklist` | Deployment Checklist |
| `devops-automator` | Devops Automator |
| `ecommerce-cms-architect` | eCommerce CMS Architect |
| `email-intelligence-engineer` | Email Intelligence Engineer |
| `embedded-firmware-engineer` | Embedded Firmware Engineer |
| `environment-setup-guide` | Environment Setup Guide |
| `error-boundary-designer` | Error Boundary Designer |
| `evidence-collector` | Evidence Collector |
| `filament-optimizer` | Filament Optimizer |
| `finops-engineer` | FinOps Engineer |
| `frontend-developer` | Frontend Developer |
| `git-commit-writer` | Git Commit Writer |
| `git-workflow-architect` | Git Workflow Architect |
| `graphql-api-designer` | GraphQL API Designer |
| `iac-provisioner` | IaC Provisioner |
| `incident-commander` | Incident Commander |
| `ios-developer` | iOS Developer |
| `it-service-manager` | IT Service Manager |
| `legacy-code-modernizer` | Legacy Code Modernizer |
| `load-testing-engineer` | Load Testing Engineer |
| `migration-engineer` | Migration Engineer |
| `minimal-change-engineer` | Minimal Change Engineer |
| `mobile-app-builder` | Mobile App Builder |
| `monorepo-planner` | Monorepo Planner |
| `multi-agent-systems-architect` | Multi Agent Systems Architect |
| `n8n` | N8n |
| `new-client-system` | New Client System |
| `observability-engineer` | Observability Engineer |
| `orgscript-engineer` | Orgscript Engineer |
| `penetration-tester` | Penetration Tester |
| `performance-optimizer` | Performance Optimizer |
| `platform-engineer` | Platform Engineer |
| `pr-description-writer` | PR Description Writer |
| `prompt-engineer` | Prompt Engineer |
| `rapid-prototyper` | Rapid Prototyper |
| `readme-generator` | Readme Generator |
| `refactor-assistant` | Refactor Assistant |
| `regex-builder` | Regex Builder |
| `secops-intelligence-engineer` | Secops Intelligence Engineer |
| `setup-codex-precheck` | Setup Codex Precheck |
| `software-architect` | Software Architect |
| `solidity-smart-contract-engineer` | Solidity Smart Contract Engineer |
| `sre-site-reliability-engineer` | SRE Site Reliability Engineer |
| `tech-stack-advisor` | Tech Stack Advisor |
| `test-writer` | Test Writer |
| `trigger-dev` | Trigger Dev |
| `typescript-migrator` | Typescript Migrator |
| `voice-ai-integration-engineer` | Voice AI Integration Engineer |
| `webhook-handler-builder` | Webhook Handler Builder |
| `workflow-optimizer` | Workflow Optimizer |

### Marketing — [skills-marketing](https://github.com/poorvith-mp/skills-marketing) (47 skills)

| Skill ID | Title |
|----------|-------|
| `aeo-foundations` | Aeo Foundations |
| `affiliate-program-designer` | Affiliate Program Designer |
| `ai-citation-strategist` | AI Citation Strategist |
| `app-store-optimizer` | App Store Optimizer |
| `book-co-author` | Book Co Author |
| `carousel-growth-engine` | Carousel Growth Engine |
| `cold-email-writer` | Cold Email Writer |
| `community-post-writer` | Community Post Writer |
| `competitor-analyser` | Competitor Analyser |
| `content-calendar-builder` | Content Calendar Builder |
| `content-repurposer` | Content Repurposer |
| `conversion-rate-optimizer` | Conversion Rate Optimizer |
| `cross-border-ecommerce-operator` | Cross Border eCommerce Operator |
| `email-strategist` | Email Strategist |
| `growth-hacker` | Growth Hacker |
| `hashtag-researcher` | Hashtag Researcher |
| `influencer-outreach-strategist` | Influencer Outreach Strategist |
| `instagram-curator` | Instagram Curator |
| `instantly-campaign` | Instantly Campaign |
| `landing-page-copywriter` | Landing Page Copywriter |
| `launch-week-planner` | Launch Week Planner |
| `livestream-commerce-coach` | Livestream Commerce Coach |
| `multi-platform-publisher` | Multi Platform Publisher |
| `newsletter-writer` | Newsletter Writer |
| `paid-media-copywriter` | Paid Media Copywriter |
| `pinterest-strategist` | Pinterest Strategist |
| `podcast-pitch-writer` | Podcast Pitch Writer |
| `podcast-strategist` | Podcast Strategist |
| `pr-and-communications-manager` | PR And Communications Manager |
| `pricing-strategist` | Pricing Strategist |
| `private-domain-operator` | Private Domain Operator |
| `product-hunt-launcher` | Product Hunt Launcher |
| `reddit-community-builder` | Reddit Community Builder |
| `search-engine-optimizer` | Search Engine Optimizer |
| `seo-article-writer` | SEO Article Writer |
| `short-video-editing-coach` | Short Video Editing Coach |
| `social-content-creator` | Social Content Creator |
| `social-media-strategist` | Social Media Strategist |
| `testimonial-extractor` | Testimonial Extractor |
| `tiktok-strategist` | Tiktok Strategist |
| `twitter-engager` | Twitter Engager |
| `video-optimizer` | Video Optimizer |
| `video-script-writer` | Video Script Writer |
| `viral-hook-generator` | Viral Hook Generator |
| `x-twitter-intelligence-analyst` | X Twitter Intelligence Analyst |
| `youtube-b-roll-maker` | Youtube B Roll Maker |
| `youtube-clipper` | Youtube Clipper |

### Specialized — [skills-specialized](https://github.com/poorvith-mp/skills-specialized) (40 skills)

| Skill ID | Title |
|----------|-------|
| `accounts-payable-agent` | Accounts Payable Agent |
| `agentic-identity-and-trust-architect` | Agentic Identity And Trust Architect |
| `agents-orchestrator` | Agents Orchestrator |
| `automation-governance-architect` | Automation Governance Architect |
| `business-strategist` | Business Strategist |
| `change-management-consultant` | Change Management Consultant |
| `chief-of-staff` | Chief Of Staff |
| `civil-engineer` | Civil Engineer |
| `corporate-training-designer` | Corporate Training Designer |
| `cultural-intelligence-strategist` | Cultural Intelligence Strategist |
| `customer-success-manager` | Customer Success Manager |
| `data-consolidation-agent` | Data Consolidation Agent |
| `data-privacy-officer` | Data Privacy Officer |
| `developer-advocate` | Developer Advocate |
| `document-generator` | Document Generator |
| `esg-sustainability-officer` | ESG Sustainability Officer |
| `government-digital-presales-consultant` | Government Digital Presales Consultant |
| `grant-writer` | Grant Writer |
| `hiring-plan-org-chart-builder` | Hiring Plan Org Chart Builder |
| `hr-onboarding` | Hr Onboarding |
| `identity-graph-operator` | Identity Graph Operator |
| `language-translator` | Language Translator |
| `legal-practice-assistant` | Legal Practice Assistant |
| `loan-officer-assistant` | Loan Officer Assistant |
| `lsp-index-engineer` | Lsp Index Engineer |
| `m-and-a-integration-manager` | M And A Integration Manager |
| `mcp-builder` | MCP Builder |
| `medical-billing-coder` | Medical Billing Coder |
| `model-qa-evaluator` | Model QA Evaluator |
| `operations-manager` | Operations Manager |
| `organizational-psychologist` | Organizational Psychologist |
| `pricing-analyst` | Pricing Analyst |
| `real-estate-advisor` | Real Estate Advisor |
| `regulatory-compliance-officer` | Regulatory Compliance Officer |
| `report-distribution-agent` | Report Distribution Agent |
| `salesforce-architect` | Salesforce Architect |
| `supply-chain-strategist` | Supply Chain Strategist |
| `talent-acquisition-manager` | Talent Acquisition Manager |
| `workflow-architect` | Workflow Architect |
| `zk-steward` | ZK Steward |

### Design — [skills-design](https://github.com/poorvith-mp/skills-design) (29 skills)

| Skill ID | Title |
|----------|-------|
| `a-b-test-designer` | A B Test Designer |
| `animation-planner` | Animation Planner |
| `brand-guardian` | Brand Guardian |
| `build-premium-website` | Build Premium Website |
| `color-palette-generator` | Color Palette Generator |
| `component-namer` | Component Namer |
| `dark-mode-adapter` | Dark Mode Adapter |
| `design-critique` | Design Critique |
| `figma-to-copy` | Figma To Copy |
| `frontend-design` | Frontend Design |
| `heatmap-interpreter` | Heatmap Interpreter |
| `icon-brief-writer` | Icon Brief Writer |
| `image-prompt-engineer` | Image Prompt Engineer |
| `inclusive-visuals-designer` | Inclusive Visuals Designer |
| `logo-brand-mark-designer` | Logo Brand Mark Designer |
| `motion-graphics-producer` | Motion Graphics Producer |
| `onboarding-flow-designer` | Onboarding Flow Designer |
| `print-packaging-designer` | Print Packaging Designer |
| `responsive-breakpoint-advisor` | Responsive Breakpoint Advisor |
| `typography-system-builder` | Typography System Builder |
| `ui-designer` | UI Designer |
| `user-persona-builder` | User Persona Builder |
| `ux-architect` | UX Architect |
| `ux-copy-writer` | UX Copy Writer |
| `ux-researcher` | UX Researcher |
| `visual-storyteller` | Visual Storyteller |
| `whimsy-injector` | Whimsy Injector |
| `youtube-popup-graphic` | Youtube Popup Graphic |
| `youtube-thumbnail-maker` | Youtube Thumbnail Maker |

### Business — [skills-business](https://github.com/poorvith-mp/skills-business) (29 skills)

| Skill ID | Title |
|----------|-------|
| `ai-governance-architect` | AI Governance Architect |
| `board-deck-builder` | Board Deck Builder |
| `business-plan-outliner` | Business Plan Outliner |
| `change-management-leader` | Change Management Leader |
| `client-proposal-writer` | Client Proposal Writer |
| `contract-clause-explainer` | Contract Clause Explainer |
| `decision-framework` | Decision Framework |
| `experiment-tracker` | Experiment Tracker |
| `feedback-giver` | Feedback Giver |
| `investor-pitch-deck-writer` | Investor Pitch Deck Writer |
| `jira-workflow-steward` | Jira Workflow Steward |
| `job-description-writer` | Job Description Writer |
| `meeting-summariser` | Meeting Summariser |
| `negotiation-strategist` | Negotiation Strategist |
| `notion-database-architect` | Notion Database Architect |
| `okr-designer` | OKR Designer |
| `product-manager` | Product Manager |
| `productivity-audit` | Productivity Audit |
| `project-manager` | Project Manager |
| `project-shepherd` | Project Shepherd |
| `sop-writer` | SOP Writer |
| `sprint-prioritizer` | Sprint Prioritizer |
| `studio-operations` | Studio Operations |
| `studio-producer` | Studio Producer |
| `trend-researcher` | Trend Researcher |
| `upwork` | Upwork |
| `upwork-proposal` | Upwork Proposal |
| `vendor-procurement-manager` | Vendor Procurement Manager |
| `workflow-redesign-consultant` | Workflow Redesign Consultant |

### Game Dev — [skills-gamedev](https://github.com/poorvith-mp/skills-gamedev) (22 skills)

| Skill ID | Title |
|----------|-------|
| `blender-add-on-engineer` | Blender Add On Engineer |
| `game-audio-engineer` | Game Audio Engineer |
| `game-designer` | Game Designer |
| `game-monetization-designer` | Game Monetization Designer |
| `godot-gameplay-scripter` | Godot Gameplay Scripter |
| `godot-multiplayer-engineer` | Godot Multiplayer Engineer |
| `godot-shader-developer` | Godot Shader Developer |
| `level-designer` | Level Designer |
| `narrative-designer` | Narrative Designer |
| `playtest-feedback-analyzer` | Playtest Feedback Analyzer |
| `roblox-avatar-creator` | Roblox Avatar Creator |
| `roblox-experience-designer` | Roblox Experience Designer |
| `roblox-systems-scripter` | Roblox Systems Scripter |
| `technical-artist` | Technical Artist |
| `unity-architect` | Unity Architect |
| `unity-editor-tool-developer` | Unity Editor Tool Developer |
| `unity-multiplayer-engineer` | Unity Multiplayer Engineer |
| `unity-shader-graph-artist` | Unity Shader Graph Artist |
| `unreal-multiplayer-architect` | Unreal Multiplayer Architect |
| `unreal-systems-engineer` | Unreal Systems Engineer |
| `unreal-technical-artist` | Unreal Technical Artist |
| `unreal-world-builder` | Unreal World Builder |

### Sales & Support — [skills-sales-support](https://github.com/poorvith-mp/skills-sales-support) (17 skills)

| Skill ID | Title |
|----------|-------|
| `account-strategist` | Account Strategist |
| `analytics-reporter` | Analytics Reporter |
| `churn-analyst` | Churn Analyst |
| `cross-channel-support-agent` | Cross Channel Support Agent |
| `customer-support` | Customer Support |
| `discovery-coach` | Discovery Coach |
| `executive-summary-generator` | Executive Summary Generator |
| `finance-tracker` | Finance Tracker |
| `legal-compliance-checker` | Legal Compliance Checker |
| `outbound-strategist` | Outbound Strategist |
| `pipeline-analyst` | Pipeline Analyst |
| `proposal-strategist` | Proposal Strategist |
| `renewal-strategist` | Renewal Strategist |
| `sales-coach` | Sales Coach |
| `sales-data-extraction-agent` | Sales Data Extraction Agent |
| `sales-engineer` | Sales Engineer |
| `sales-outreach` | Sales Outreach |

### Education — [skills-education](https://github.com/poorvith-mp/skills-education) (15 skills)

| Skill ID | Title |
|----------|-------|
| `citation-formatter` | Citation Formatter |
| `concept-explainer` | Concept Explainer |
| `essay-structurer` | Essay Structurer |
| `exam-question-generator` | Exam Question Generator |
| `flashcard-generator` | Flashcard Generator |
| `historian` | Historian |
| `interview-prep-coach` | Interview Prep Coach |
| `mental-model-teacher` | Mental Model Teacher |
| `mentor-simulator` | Mentor Simulator |
| `reading-list-curator` | Reading List Curator |
| `research-paper-summariser` | Research Paper Summariser |
| `researcher` | Researcher |
| `skill-roadmap-builder` | Skill Roadmap Builder |
| `study-abroad-advisor` | Study Abroad Advisor |
| `study-plan-builder` | Study Plan Builder |

### Finance — [skills-finance](https://github.com/poorvith-mp/skills-finance) (12 skills)

| Skill ID | Title |
|----------|-------|
| `bookkeeper-and-controller` | Bookkeeper And Controller |
| `budget-expense-auditor` | Budget Expense Auditor |
| `cap-table-fundraising-modeler` | Cap Table Fundraising Modeler |
| `chief-financial-officer` | Chief Financial Officer |
| `crypto-tax-advisor` | Crypto Tax Advisor |
| `financial-analyst` | Financial Analyst |
| `financial-plan-starter` | Financial Plan Starter |
| `fp-and-a-analyst` | Fp And A Analyst |
| `insurance-actuary-analyst` | Insurance Actuary Analyst |
| `investment-researcher` | Investment Researcher |
| `invoice-and-payment-writer` | Invoice And Payment Writer |
| `tax-strategist` | Tax Strategist |

### Personal — [skills-personal](https://github.com/poorvith-mp/skills-personal) (10 skills)

| Skill ID | Title |
|----------|-------|
| `fitness-nutrition-planner` | Fitness Nutrition Planner |
| `habit-tracker-designer` | Habit Tracker Designer |
| `know-me` | Know Me |
| `knowledge-management-architect` | Knowledge Management Architect |
| `linkedin-profile-optimizer` | Linkedin Profile Optimizer |
| `periodic-review-system` | Periodic Review System |
| `relationship-crm-builder` | Relationship CRM Builder |
| `resume-optimizer` | Resume Optimizer |
| `second-brain-architect` | Second Brain Architect |
| `travel-planner` | Travel Planner |

### Writing — [skills-writing](https://github.com/poorvith-mp/skills-writing) (5 skills)

| Skill ID | Title |
|----------|-------|
| `longform-book-author` | Longform Book Author |
| `marketing-copywriter` | Marketing Copywriter |
| `screenplay-writer` | Screenplay Writer |
| `technical-writer` | Technical Writer |
| `thread-to-blog-converter` | Thread To Blog Converter |

### Meta — [skills-meta](https://github.com/poorvith-mp/skills-meta) (4 skills)

| Skill ID | Title |
|----------|-------|
| `create-skill` | Create Skill |
| `prompt-library-curator` | Prompt Library Curator |
| `skill-linter` | Skill Linter |
| `skill-router` | Skill Router |

<!-- END:INDEX -->
