"""Build mapping between 307 v3 skills and 277 v4 skills.

Outputs a dictionary:
- new_skill_slug -> {
    'target_repo': str,
    'group': str,
    'description': str,
    'source_skill': (old_repo, old_slug) | None,
    'merge_sources': list[(old_repo, old_slug)],
  }
- old_skill_slug -> {
    'old_repo': str,
    'target_slug': str | None,
    'target_repo': str | None,
  }
"""

from __future__ import annotations

import json
from pathlib import Path
from v4_catalog_data import load_v4_catalog, get_all_v4_skills

own_dir = Path("c:/Users/poorv/projects/own")

# Collect existing v3 skills
existing = {}
for repo_dir in own_dir.glob("skills-*"):
    skills_dir = repo_dir / "skills"
    if skills_dir.exists():
        for sdir in skills_dir.iterdir():
            if sdir.is_dir() and (sdir / "SKILL.md").exists():
                existing[sdir.name] = repo_dir.name

print(f"Total existing v3 skills: {len(existing)}")

catalog_skills = get_all_v4_skills()
print(f"Total target v4 skills: {len(catalog_skills)}")

# High confidence stem / synonym mapping
# old_slug -> target_slug
OLD_TO_NEW = {
    # Developer
    "codebase-onboarding-engineer": "codebase-map",
    "software-architect": "system-design",
    "api-lifecycle-engineer": "api-design",
    "graphql-api-designer": "api-design",
    "database-schema-designer": "database",
    "database-optimizer": "database",
    "tech-stack-advisor": "stack-choice",
    "frontend-developer": "frontend-build",
    "mobile-app-builder": "mobile-build",
    "ios-developer": "mobile-build",
    "android-developer": "mobile-build",
    "backend-architect": "backend-build",
    "rapid-prototyper": "prototype",
    "minimal-change-engineer": "minimal-diff",
    "refactor-assistant": "refactor",
    "code-translator": "port-code",
    "typescript-migrator": "port-code",
    "data-pipeline-architect": "data-pipelines",
    "data-engineer": "data-pipelines",
    "ai-data-remediation-engineer": "data-pipelines",
    "ai-engineer": "ml-deployment",
    "ai-eval-suite-builder": "llm-evals",
    "voice-ai-integration-engineer": "speech-pipelines",
    "code-reviewer": "code-review",
    "test-writer": "test-suite",
    "bug-explainer": "debugging",
    "debugging-strategist": "debugging",
    "performance-optimizer": "performance-audit",
    "load-testing-engineer": "load-testing",
    "appsec-architect": "security-review",
    "penetration-tester": "pen-test",
    "dependency-upgrade-auditor": "dependency-audit",
    "cloud-security-architect": "cloud-security",
    "secops-intelligence-engineer": "threat-detection",
    "compliance-auditor": "audit-readiness",
    "evidence-collector": "audit-readiness",
    "ci-cd-pipeline-builder": "ci-pipelines",
    "iac-provisioner": "infrastructure",
    "deployment-checklist": "deployment",
    "devops-automator": "deployment",
    "observability-engineer": "reliability",
    "sre-site-reliability-engineer": "reliability",
    "incident-commander": "incident-response",
    "finops-engineer": "cloud-cost",
    "platform-engineer": "developer-platform",
    "cron-job-planner": "job-scheduling",
    "migration-engineer": "migration",
    "legacy-code-modernizer": "migration",
    "monorepo-planner": "monorepo",
    "readme-generator": "repo-docs",
    "code-comment-writer": "repo-docs",
    "changelog-writer": "change-notes",
    "git-commit-writer": "change-notes",
    "pr-description-writer": "change-notes",
    "git-workflow-architect": "branching-strategy",
    "accessibility-engineer": "accessibility-fix",
    "error-boundary-designer": "error-handling",
    "webhook-handler-builder": "webhooks",
    "regex-builder": "regex",
    "embedded-firmware-engineer": "firmware",
    "solidity-smart-contract-engineer": "smart-contracts",
    "blockchain-security-auditor": "smart-contract-audit",
    "ecommerce-cms-architect": "commerce-platform",

    # Marketing
    "brand-positioning-strategist": "positioning",
    "customer-researcher": "customer-research",
    "competitor-intelligence-analyst": "competitive-intel",
    "gtm-planner": "growth-plan",
    "growth-marketer": "growth-plan",
    "pricing-strategist": "pricing",
    "unit-economics-analyst": "unit-economics",
    "seo-auditor": "seo-audit",
    "programmatic-seo-specialist": "page-scale",
    "content-strategist": "content-strategy",
    "seo-content-writer": "article-writing",
    "landing-page-copywriter": "landing-copy",
    "conversion-rate-optimizer": "conversion-audit",
    "user-onboarding-specialist": "activation",
    "paid-ads-manager": "paid-campaigns",
    "ad-creative-director": "ad-creative",
    "sales-enablement-specialist": "sales-enablement",
    "revops-specialist": "revops",
    "email-marketing-specialist": "lifecycle-messaging",
    "churn-reduction-specialist": "retention",
    "paywall-designer": "upgrade-paths",
    "social-media-strategist": "social-content",
    "social-listening-analyst": "social-listening",
    "product-hunt-launcher": "launch",
    "pr-media-strategist": "public-relations",
    "partnership-manager": "partnerships",
    "community-manager": "community",
    "referral-program-designer": "referrals",
    "lead-magnet-creator": "lead-magnets",
    "free-tool-ideator": "free-tools",
    "marketing-designer": "visual-assets",
    "video-marketing-producer": "video-production",
    "ga4-analytics-specialist": "analytics-setup",
    "marketing-attribution-analyst": "attribution",
    "ab-testing-specialist": "experimentation",
    "marketing-reporting-analyst": "marketing-report",
    "growth-loops-architect": "growth-loops",
    "marketing-psychology-consultant": "behavioral-levers",
    "legendary-marketing-council": "marketing-council",
    "aso-specialist": "app-store-optimization",
    "product-namer": "naming",

    # Game Dev
    "game-ideator": "game-ideation",
    "game-production-planner": "production-planning",
    "game-designer": "game-design",
    "level-designer": "level-design",
    "narrative-designer": "narrative-design",
    "game-ai-developer": "game-ai",
    "game-ui-ux-designer": "game-ui",
    "game-economy-designer": "game-monetization",
    "playtesting-coordinator": "playtesting",
    "game-audio-engineer": "game-audio",
    "technical-artist": "tech-art",
    "blender-3d-modeler": "blender-modeling",
    "blender-animator": "blender-animation",
    "blender-pipeline-tooler": "blender-tooling",
    "unity-game-architect": "unity-architecture",
    "unity-editor-tooler": "unity-tooling",
    "unity-multiplayer-developer": "unity-multiplayer",
    "unity-shader-artist": "unity-shaders",
    "unreal-gameplay-architect": "unreal-systems",
    "unreal-multiplayer-developer": "unreal-multiplayer",
    "unreal-technical-artist": "unreal-tech-art",
    "unreal-world-builder": "unreal-worlds",

    # Business
    "business-strategy-consultant": "business-strategy",
    "business-model-architect": "business-plan",
    "market-research-analyst": "market-trends",
    "decision-framework-consultant": "decision-making",
    "pitch-deck-creator": "investor-deck",
    "fundraising-advisor": "fundraising",
    "board-meeting-pack-creator": "board-reporting",
    "deal-negotiator": "negotiation",
    "product-manager": "product-management",
    "project-manager": "project-planning",
    "sprint-planner": "sprint-planning",
    "okr-architect": "okrs",
    "business-operations-manager": "operations",
    "process-optimization-consultant": "process-redesign",
    "portfolio-manager": "portfolio-ops",
    "vendor-procurement-manager": "vendor-selection",
    "supply-chain-architect": "supply-chain",
    "strategic-partnership-broker": "alliances",
    "headcount-planner": "hiring",
    "talent-acquisition-specialist": "hiring",
    "change-management-consultant": "change-management",
    "team-culture-optimizer": "team-dynamics",
    "kpi-dashboard-architect": "internal-reporting",

    # Design
    "ux-researcher": "ux-research",
    "design-system-architect": "design-critique",
    "accessibility-designer": "accessibility-review",
    "typography-specialist": "type-system",
    "color-palette-designer": "color-system",
    "ui-component-designer": "component-library",
    "responsive-design-specialist": "responsive-rules",
    "ui-designer": "ui-design",
    "information-architect": "information-architecture",
    "microcopy-writer": "ui-copy",
    "motion-designer": "motion-design",
    "interactive-prototyper": "interactive-prototype",
    "brand-identity-designer": "brand-system",
    "iconographer": "icon-design",
    "packaging-designer": "print-packaging",
    "ai-image-prompter": "image-prompts",

    # Education
    "learning-path-designer": "learning-roadmap",
    "curriculum-developer": "study-plan",
    "visual-note-maker": "mind-maps",
    "spaced-repetition-expert": "flashcards",
    "concept-explainer": "concept-explainer",
    "socratic-tutor": "mentoring",
    "academic-researcher": "research",
    "source-evaluator": "source-evaluation",
    "paper-summarizer": "paper-summary",
    "literature-reviewer": "literature-review",
    "research-methodologist": "research-methods",
    "citation-specialist": "citations",
    "quiz-generator": "quizzes",
    "instructional-designer": "training-design",
    "thesis-advisor": "academic-project",

    # Agents (assembled from developer, specialized, meta)
    "multi-agent-systems-architect": "agent-architecture",
    "rag-architect": "rag-systems",
    "mcp-builder": "mcp-builder",
    "composio": "composio",
    "prompt-engineer": "prompt-engineering",
    "create-skill": "create-skill",
    "skill-linter": "skill-linter",
    "workflow-optimizer": "workflow-mapping",
    "automation-auditor": "automation-review",
    "n8n": "n8n",
    "trigger-dev": "trigger-dev",
    "document-generator": "document-generation",
    "report-consolidator": "report-automation",

    # Personal
    "know-me": "personal-context",
    "resume-builder": "resume",
    "linkedin-profile-optimizer": "linkedin-profile",
    "job-hunt-strategist": "job-search",
    "interview-prep-coach": "interview-prep",
    "second-brain-architect": "note-system",
    "productivity-audit": "productivity-audit",
    "review-ritual-designer": "periodic-review",
    "habit-loop-designer": "habits",
    "fitness-nutrition-planner": "fitness-nutrition",
    "budget-planner": "personal-finance",
    "personal-crm-designer": "personal-crm",
    "travel-itinerary-builder": "travel-planning",
    "filament-optimizer": "3d-printing",

    # Writing
    "book-outliner": "book-writing",
    "screenwriter": "screenwriting",
    "speech-writer": "talk-writing",
    "technical-writer": "technical-docs",
    "sop-creator": "sop-writing",
    "executive-briefing-writer": "executive-summary",
    "meeting-insights-extractor": "meeting-notes",
    "grant-proposal-writer": "grant-writing",
    "job-description-writer": "job-descriptions",
    "performance-review-writer": "feedback-writing",
    "thread-to-article-converter": "thread-to-article",
    "multilingual-translator": "translation",
    "historical-accuracy-checker": "historical-accuracy",

    # Sales
    "prospect-list-builder": "prospecting",
    "cold-email-writer": "cold-outreach",
    "discovery-call-strategist": "discovery",
    "sales-demo-engineer": "solution-engineering",
    "client-proposal-writer": "proposals",
    "sales-pipeline-auditor": "pipeline-health",
    "win-loss-interviewer": "win-loss-analysis",
    "account-manager": "account-management",
    "contract-renewal-manager": "renewals",
    "client-onboarding-specialist": "client-onboarding",
    "customer-support-agent": "support-replies",
    "sales-coach": "sales-coaching",
    "freelance-pitch-writer": "freelance-bidding",
    "rfp-response-builder": "public-sector-bids",

    # Finance
    "bookkeeper": "bookkeeping",
    "budget-forecast-modeler": "budgeting",
    "invoice-generator": "invoicing",
    "accounts-payable-automation": "accounts-payable",
    "financial-modeling-specialist": "financial-modeling",
    "cap-table-dilution-modeler": "cap-table",
    "runway-burn-calculator": "runway-planning",
    "saas-metrics-analyst": "saas-metrics",
    "cfos-fractional-advisor": "finance-strategy",
    "tax-strategy-planner": "tax-strategy",
    "crypto-tax-calculator": "crypto-tax",
    "investment-analyst": "investment-research",

    # Legal
    "contract-reviewer": "contract-review",
    "contract-drafter": "contract-drafting",
    "terms-privacy-generator": "legal-documents",
    "data-privacy-compliance-officer": "data-privacy",
    "startup-incorporation-advisor": "company-formation",
    "employment-law-advisor": "employment-law",
    "ip-trademark-strategist": "ip-protection",
    "open-source-license-checker": "open-source-licensing",
    "regulatory-compliance-officer": "regulatory-compliance",
    "responsible-ai-governance-auditor": "ai-governance",
    "esg-reporting-specialist": "esg-reporting",
    "chief-of-staff": "chief-of-staff",
}

print(f"Explicit mappings defined: {len(OLD_TO_NEW)}")
# Verify all target slugs in OLD_TO_NEW exist in v4 catalog
catalog_slugs = {s["slug"] for s in catalog_skills}
invalid = [t for t in OLD_TO_NEW.values() if t not in catalog_slugs]
if invalid:
    print(f"Warning: mapped to invalid catalog slugs: {set(invalid)}")
else:
    print("All mapped targets exist in v4 catalog!")
