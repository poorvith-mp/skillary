# Skill Index

GENERATED FILE - do not edit by hand. Rebuild with `python scripts/build_index.py --router` in the hub repo.

307 skills across 12 category repos.

Format: `skill-id` — description — `repo`

## skills-developer

- `accessibility-engineer` — Audits and refactors web apps for WCAG 2.1/2.2 AA and AAA: ARIA, keyboard operability and screen reader support. Use when fixing accessibility failures or preparing an accessibility audit.
- `ai-data-remediation-engineer` — Builds self-healing data pipelines that detect, classify and correct data anomalies using local models and semantic clustering. Use when data quality breaks repeatedly and manual cleanup does not...
- `ai-engineer` — Develops and deploys ML models into production: training, serving, evaluation and integration. Use when shipping a model. Not for eval harnesses - use ai-eval-suite-builder.
- `ai-eval-suite-builder` — Builds LLM evaluation harnesses: regression datasets, scoring rubrics, prompt drift detection and benchmarks. Use when replacing eyeballed output quality with automated evals.
- `android-developer` — Builds native Android apps in Kotlin and Jetpack Compose with Material 3, MVVM/MVI and Hilt. Use for Android-specific work. For cross-platform, use mobile-app-builder.
- `api-lifecycle-engineer` — Designs, documents, mocks and tests REST, GraphQL and gRPC APIs with OpenAPI and contract testing. Use when designing an API surface. For GraphQL schema depth, use graphql-api-designer.
- `appsec-architect` — Runs application security reviews: STRIDE threat modelling, OWASP Top 10 code auditing and secure design. Use when threat modelling a system. Not for live testing - use penetration-tester.
- `autonomous-optimization-architect` — Designs systems that tune themselves - autoscaling, adaptive parameters and feedback-driven optimisation with safe bounds. Use when a system needs to self-correct rather than be tuned by hand.
- `backend-architect` — Designs backend systems: service boundaries, database architecture, API structure and cloud infrastructure. Use when designing a backend. Not for whole-system architecture - use software-architect.
- `blockchain-security-auditor` — Audits smart contracts and on-chain systems for reentrancy, access control flaws, oracle manipulation and economic exploits. Use when reviewing contract security before deployment.
- `bug-explainer` — Turns an error message or stack trace into a plain explanation of what broke, why, and what to check next. Use when a trace is opaque. Not for systematic root-cause work - use debugging-strategist.
- `changelog-writer` — Writes changelogs in Keep a Changelog format with categorised entries and audience-appropriate wording. Use when preparing a release note from commits or a diff.
- `ci-cd-pipeline-builder` — Builds CI/CD pipelines with build, test, security scan and deploy stages across common providers. Use when setting up or repairing a pipeline. Not for infrastructure itself - use iac-provisioner.
- `cloud-security-architect` — Designs cloud security: identity and access boundaries, network segmentation, key management and workload isolation across AWS, Azure and GCP. Use when securing a cloud estate.
- `code-comment-writer` — Writes comments and docstrings that explain intent and non-obvious decisions rather than restating the code. Use when documenting a function or module for the next reader.
- `code-reviewer` — Reviews code for correctness, performance, security, readability, test coverage and architectural fit. Use when reviewing a diff or PR before merge.
- `code-translator` — Translates code between languages while preserving behaviour, idiom and test coverage. Use when porting a module to another language rather than rewriting it from scratch.
- `codebase-onboarding-engineer` — Maps an unfamiliar codebase: entry points, data flow, key abstractions and where to make a first change. Use when joining a project. Not for modernising it - use legacy-code-modernizer.
- `compliance-auditor` — Prepares for SOC 2, ISO 27001, HIPAA and PCI-DSS audits: readiness assessment, control mapping and evidence collection. Use when preparing for a technical audit. Name the framework.
- `composio` — Integrates Composio to give agents authenticated access to third-party SaaS tools. Use when wiring an agent to external services through Composio's connectors.
- `cron-job-planner` — Designs cron schedules with timezone handling, overlap prevention, failure alerting and dependency ordering. Use when scheduling recurring jobs or fixing overlapping runs.
- `data-engineer` — Builds data pipelines, lakehouse architectures and data infrastructure. Use for implementation and operation. For pipeline design patterns and schema evolution, use data-pipeline-architect.
- `data-pipeline-architect` — Designs ETL/ELT pipelines, data quality validation, schema evolution and streaming versus batch architecture. Use when choosing an approach. For building it, use data-engineer.
- `database-optimizer` — Diagnoses and fixes slow queries: execution plans, index design, N+1 access patterns and denormalisation trade-offs. Use when a database is the bottleneck.
- `database-schema-designer` — Designs SQL schemas with relationships, indexes, constraints and normalisation suited to the access patterns. Use when modelling a new schema. Not for tuning an existing one - use database-optimizer.
- `debugging-strategist` — Applies systematic debugging: binary search isolation, hypothesis-driven log analysis, memory and race condition profiling. Use when a bug resists guessing. Not for reading one trace - use...
- `dependency-upgrade-auditor` — Audits dependencies for outdated versions, CVEs, license compliance and breaking-change risk, and sequences the upgrade. Use when planning a dependency bump or clearing a security alert.
- `deployment-checklist` — Produces pre- and post-deployment verification checklists covering migrations, feature flags, rollback and smoke checks. Use when preparing a release cutover.
- `devops-automator` — Automates infrastructure and cloud operations: provisioning, configuration management and operational tooling. Use for day-to-day DevOps. For pipelines, use ci-cd-pipeline-builder.
- `ecommerce-cms-architect` — Architects CMS-based commerce: cart pipelines, checkout flows, payment gateway integration and PCI-aware handling. Use when building or hardening an online store.
- `email-intelligence-engineer` — Extracts structured, reasoning-ready data from raw email threads for agents and automation. Use when turning messy inbox content into usable structured records.
- `embedded-firmware-engineer` — Writes bare-metal and RTOS firmware for ESP32/ESP-IDF, ARM Cortex-M, STM32 and Nordic nRF. Use when developing or debugging firmware on constrained hardware.
- `environment-setup-guide` — Writes local development setup guides with dependency installation, configuration, seed data and a verification step. Use when onboarding developers onto a project's tooling.
- `error-boundary-designer` — Designs error handling: boundaries, fallback UIs, retry strategy, circuit breakers and degradation paths. Use when failures cascade or surface as blank screens.
- `evidence-collector` — Runs QA that demands visual proof, defaulting to finding several concrete issues with screenshots. Use when verifying a change actually works rather than trusting that it does.
- `filament-optimizer` — Tunes 3D printing filament profiles: temperature, flow, retraction and cooling against material and printer. Use when print quality problems trace to material settings.
- `finops-engineer` — Analyses and reduces cloud cost: unit economics, showback/chargeback, rightsizing and commitment planning. Use when cloud spend outpaces usage or needs allocating to teams.
- `frontend-developer` — Implements web UIs in React, Vue or Angular with attention to performance and correctness. Use when building frontend features. Not for visual design - use ui-designer or frontend-design.
- `git-commit-writer` — Writes Conventional Commits messages with correct type, scope and breaking-change footers. Use when committing. Not for PR descriptions - use pr-description-writer.
- `git-workflow-architect` — Designs branching and release strategy: trunk-based or GitFlow, protection rules, review policy and release tagging. Use when a team's git process causes conflicts or unclear release state.
- `graphql-api-designer` — Designs GraphQL schemas: types, queries and mutations, resolver patterns, pagination and N+1 avoidance. Use for GraphQL specifically. For REST or gRPC, use api-lifecycle-engineer.
- `iac-provisioner` — Writes Terraform, Pulumi or CloudFormation with modular resources, state management and drift detection. Use when provisioning infrastructure as code.
- `incident-commander` — Runs incident response: severity classification, diagnostic triage, stakeholder comms, mitigation and post-mortem. Use when a production incident is active or when writing the post-mortem afterwards.
- `ios-developer` — Builds native iOS apps in Swift and SwiftUI following Apple HIG, with Combine and App Store requirements. Use for iOS-specific work. For cross-platform, use mobile-app-builder.
- `it-service-manager` — Runs IT service management: incident, problem and change processes, service catalogue and SLA tracking. Use when structuring an IT support function.
- `legacy-code-modernizer` — Maps dependencies and debt hotspots in a legacy codebase and plans incremental migration with strangler-fig staging. Use when modernising without a rewrite. For the cutover, use migration-engineer.
- `load-testing-engineer` — Designs and runs load tests with k6, Locust or JMeter using realistic traffic patterns and baselines. Use when validating capacity or finding a breaking point.
- `migration-engineer` — Executes zero-downtime migrations: database cutovers, cloud-to-cloud moves and monolith decomposition with rollback. Use when moving live data or traffic. For planning debt reduction, use...
- `minimal-change-engineer` — Makes the smallest correct change to fix a problem, resisting incidental refactors and scope creep. Use when a codebase is fragile and the diff must stay reviewable.
- `mobile-app-builder` — Builds mobile apps across native and cross-platform frameworks. Use when the platform is undecided or the app targets both. For platform-specific depth, use ios-developer or android-developer.
- `monorepo-planner` — Structures monorepos with Turborepo, Nx or pnpm workspaces, build caching and affected-module detection. Use when a repo's builds are slow or its boundaries unclear.
- `multi-agent-systems-architect` — Designs multi-agent systems: role decomposition, message passing, shared state and failure isolation. Use when one agent is not enough and coordination becomes the problem.
- `n8n` — Builds n8n automation workflows: node wiring, credentials, error branches and scheduling. Use when automating in n8n. Not for governance review - use automation-governance-architect.
- `new-client-system` — Sets up the onboarding system for a new client engagement: intake, access, environments, communication cadence and deliverable tracking. Use when starting client work.
- `observability-engineer` — Instruments services with OpenTelemetry traces, metrics and structured logs, and designs SLO/SLI dashboards and alerts. Use when incidents are hard to diagnose or alerts are noisy.
- `orgscript-engineer` — Encodes organisational processes as executable scripts and templates so recurring work runs consistently. Use when a process lives only in people's heads.
- `penetration-tester` — Conducts authorised penetration tests and red team operations against networks, applications and cloud. Use for live offensive testing. For design review, use appsec-architect.
- `performance-optimizer` — Profiles and optimises performance across frontend Core Web Vitals, backend queries and infrastructure. Use when something is slow and the cause is not yet known.
- `platform-engineer` — Builds internal developer platforms: golden path templates, self-service provisioning and developer experience. Use when developers wait on tickets to ship.
- `pr-description-writer` — Writes pull request descriptions with context, motivation, approach, testing performed and review guidance. Use when opening a PR. Not for commit messages - use git-commit-writer.
- `prompt-engineer` — Crafts, tests and systematically optimises LLM prompts, turning vague instructions into reliable production behaviour. Use when a prompt is inconsistent or needs evaluating.
- `rapid-prototyper` — Builds a working prototype fast, choosing throwaway shortcuts deliberately and marking what must be rebuilt. Use when validating an idea rather than shipping it.
- `readme-generator` — Writes project READMEs with purpose, install steps, usage examples, configuration and contribution notes. Use when a project has no README or an unusable one.
- `refactor-assistant` — Identifies code smells and proposes refactorings - extract method, replace conditional with polymorphism, introduce parameter object - with safe sequencing. Use when improving structure without...
- `regex-builder` — Builds and explains regular expressions, with a breakdown of each component and the cases they match. Use when writing a non-trivial pattern or debugging one that misfires.
- `secops-intelligence-engineer` — Writes threat detection rules, correlates SIEM/SOC telemetry and maps adversary behaviour to MITRE ATT&CK. Use when building detections or triaging security events.
- `setup-codex-precheck` — Runs pre-flight checks before a Codex session: environment, dependencies, credentials and repo state. Use when preparing a repository for agent-driven work.
- `software-architect` — Designs whole-system architecture: domain-driven design, architectural patterns and technical decision records. Use for system-level design. For backend specifics, use backend-architect.
- `solidity-smart-contract-engineer` — Writes Solidity for EVM: contract architecture, gas optimisation, upgradeable proxies and DeFi patterns. Use when building contracts. For auditing them, use blockchain-security-auditor.
- `sre-site-reliability-engineer` — Practises SRE: SLOs, error budgets, chaos engineering and toil reduction. Use when setting reliability targets. For instrumentation, use observability-engineer.
- `tech-stack-advisor` — Evaluates technology options against requirements, team skill, scalability and total cost of ownership. Use when choosing a stack or justifying a technology decision.
- `test-writer` — Writes test suites covering happy paths, edge cases and failure modes for a function, component or API. Use when adding coverage or writing tests before an implementation.
- `trigger-dev` — Builds Trigger.dev background jobs: task definitions, retries, scheduling and observability. Use when running long or scheduled work off the request path. For visual no-code automation, use n8n.
- `typescript-migrator` — Plans and executes JavaScript to TypeScript migration with incremental strictness, type strategy and tsconfig staging. Use when adding types to an existing JS codebase.
- `voice-ai-integration-engineer` — Builds speech transcription pipelines with Whisper-style models and cloud ASR, from audio ingestion to structured output. Use when adding transcription or voice input to a product.
- `webhook-handler-builder` — Builds webhook receivers with signature verification, idempotent processing, retries and dead letter queues. Use when receiving webhooks that must not double-process or silently drop.
- `workflow-optimizer` — Analyses and automates business workflows to cut handoffs, waiting and rework. Use when improving an existing process. For a full redesign before automating, use workflow-redesign-consultant.

## skills-marketing

- `aeo-foundations` — Establishes answer engine optimisation basics: structuring content so AI assistants can quote it, with entity clarity and citable claims. Use when starting AEO work. Not for auditing existing...
- `affiliate-program-designer` — Designs affiliate and referral programmes: commission structure, partner tiers, attribution tracking and fraud prevention. Use when launching a referral programme or fixing one that attracts the...
- `ai-citation-strategist` — Audits brand visibility in ChatGPT, Claude, Gemini and Perplexity, and diagnoses why competitors get cited instead. Use when checking AI search presence. Not for groundwork - use aeo-foundations.
- `app-store-optimizer` — Optimises App Store and Play listings: keywords, screenshots, conversion rate and discoverability. Use when a listing underperforms or preparing an app launch.
- `book-co-author` — Turns voice notes, fragments and positioning into a structured thought-leadership book for founders and operators. Use when developing a book from scattered material. Not for fiction - use...
- `carousel-growth-engine` — Generates TikTok and Instagram carousels from a website URL, producing multi-slide viral formats. Use when producing carousel content at volume from existing site material.
- `cold-email-writer` — Writes cold outreach sequences with research-based hooks, value-first messaging, objection prehandling and follow-up cadence. Use when writing cold emails. Not for ICP strategy - use...
- `community-post-writer` — Writes forum posts and discussion prompts for Discord, Reddit, Slack and brand communities. Use when seeding a discussion or posting somewhere that punishes marketing tone.
- `competitor-analyser` — Analyses competitors on positioning, pricing, feature gaps, channels and content. Use when sizing up a rival or building a battlecard. Not for market trend scanning - use trend-researcher.
- `content-calendar-builder` — Builds content calendars with theme mapping, channel distribution, cadence and seasonal campaigns. Use when planning a publishing schedule. Not for a single launch week - use launch-week-planner.
- `content-repurposer` — Turns long-form articles, podcasts and webinars into channel-specific derivative assets. Use when maximising reach from existing material. Not for thread-to-article specifically - use...
- `conversion-rate-optimizer` — Analyses conversion funnels, forms A/B hypotheses and optimises landing pages and behavioural triggers. Use when a funnel leaks. Not for the statistics of the test - use a-b-test-designer.
- `cross-border-ecommerce-operator` — Runs Amazon, Shopee, Lazada, AliExpress, Temu and TikTok Shop operations plus international logistics. Use when managing cross-border e-commerce platforms and fulfillment.
- `email-strategist` — Designs lifecycle email programmes: segmentation, automation flows, cadence and deliverability. Use when planning an email programme. Not for cold outreach - use cold-email-writer.
- `growth-hacker` — Runs data-driven acquisition experiments: viral loops, funnel optimisation and channel testing. Use when hunting scalable acquisition. Not for the experiment log - use experiment-tracker.
- `hashtag-researcher` — Researches platform-specific hashtags by reach, competition, trending velocity and audience relevance. Use when choosing hashtags for a post or building a reusable tag set.
- `influencer-outreach-strategist` — Designs influencer programmes: creator identification, outreach templates, collaboration structures and ROI measurement. Use when running creator partnerships or pricing a collaboration.
- `instagram-curator` — Builds Instagram presence: visual storytelling, grid aesthetics, Reels and Stories formats and community building. Use when growing an Instagram account or planning its content mix.
- `instantly-campaign` — Configures and runs Instantly cold email campaigns: inbox warmup, sequence setup, sending limits and deliverability monitoring. Use when operating outreach inside Instantly.
- `landing-page-copywriter` — Writes landing page copy: above-the-fold hook, benefit-led body, social proof and friction-reducing CTAs. Use when writing a landing page. Not for ad copy - use paid-media-copywriter.
- `launch-week-planner` — Plans a launch week day by day: content schedule, press outreach, social amplification and community activation. Use when coordinating a launch moment. Not for ongoing cadence - use...
- `livestream-commerce-coach` — Coaches livestream selling: show structure, product sequencing, hook cadence and conversion moments. Use when running or improving a live shopping stream.
- `multi-platform-publisher` — Adapts and schedules one piece of content across multiple platforms, respecting each one's format and norms. Use when publishing the same message everywhere without it reading as copy-paste.
- `newsletter-writer` — Writes newsletters with subject lines that get opened, scannable structure and value-dense sections. Use when writing a recurring newsletter or improving open and retention rates.
- `paid-media-copywriter` — Writes direct-response ad copy, headlines and creative briefs for Google Ads, Meta and LinkedIn within platform limits. Use when writing ads. Not for landing pages - use landing-page-copywriter.
- `pinterest-strategist` — Builds Pinterest strategy: pin design, board architecture, keyword SEO, Idea Pins and shopping catalogue. Use when growing Pinterest traffic or setting up product pins.
- `podcast-pitch-writer` — Writes podcast guest pitches with show-specific angles, topic hooks and a one-sheet media kit. Use when pitching yourself as a guest. Not for running a show - use podcast-strategist.
- `podcast-strategist` — Develops podcast concepts, episode outlines, guest prep, show notes and distribution. Use when planning or improving a show. Not for pitching as a guest - use podcast-pitch-writer.
- `pr-and-communications-manager` — Handles media relations, press releases, crisis communications and executive thought leadership. Use when pitching press, announcing news, or responding to a reputational issue.
- `pricing-strategist` — Designs pricing models - freemium, tiered, usage-based, per-seat - with value metric and willingness-to-pay analysis. Use when structuring packaging. Not for a single price change - use...
- `private-domain-operator` — Builds WeCom private domain ecosystems: SCRM, segmented community operations and Mini Program integration. Use when running owned-audience operations on WeChat.
- `product-hunt-launcher` — Runs a Product Hunt launch: maker profile, hunter outreach, launch-day scheduling and community engagement. Use when launching on Product Hunt specifically.
- `reddit-community-builder` — Builds authentic Reddit presence with value-first contribution and subreddit-specific norms. Use when marketing on Reddit without getting removed or downvoted.
- `search-engine-optimizer` — Runs on-page, technical and off-page SEO: audits, keyword clustering and structured data. Use when diagnosing rankings or fixing technical SEO. Not for writing the article - use seo-article-writer.
- `seo-article-writer` — Writes long-form articles targeting search intent with keyword-led headings, internal links and schema. Use when writing an article to rank. Not for site-wide SEO - use search-engine-optimizer.
- `short-video-editing-coach` — Coaches short-video post-production across CapCut Pro, Premiere Pro, DaVinci Resolve and Final Cut. Use when editing short-form video or fixing pacing and retention in an edit.
- `social-content-creator` — Writes posts, threads and carousels for LinkedIn, X, Threads and Instagram. Use when creating individual social posts. Not for the overall plan - use social-media-strategist.
- `social-media-strategist` — Plans organic social strategy: channel mix, content calendars, engagement tactics and growth playbooks. Use when setting social direction. Not for writing individual posts - use...
- `testimonial-extractor` — Pulls testimonials out of reviews, surveys and interviews and sorts them by use case and objection handled. Use when building social proof from existing customer feedback.
- `tiktok-strategist` — Builds TikTok presence: hook patterns, algorithm behaviour, trend participation and community norms. Use when growing on TikTok or diagnosing why videos stall.
- `twitter-engager` — Builds X/Twitter presence through real-time engagement, replies and thought leadership. Use when growing an account by participating. Not for research - use x-twitter-intelligence-analyst.
- `video-optimizer` — Optimises YouTube performance: retention, chaptering, titles, thumbnails and cross-platform distribution. Use when videos underperform. Not for the script - use video-script-writer.
- `video-script-writer` — Writes scripts for YouTube, explainers, product demos, webinars and social video with hook-led structure. Use when scripting a video. Not for editing or optimisation - use video-optimizer.
- `viral-hook-generator` — Generates hook variations for a topic across platforms and psychological angles. Use when the opening line is the problem, or when testing multiple hooks before committing to one.
- `x-twitter-intelligence-analyst` — Researches X/Twitter for trends, account monitoring and evidence-backed audience insight from public signals. Use when researching a topic or account. Not for posting - use twitter-engager.
- `youtube-b-roll-maker` — Produces B-roll clips to cover narration and add visual variety to a video. Use when a talking segment needs visual support. Not for thumbnails or overlays - use youtube-thumbnail-maker.
- `youtube-clipper` — Finds the strongest moments in a long video and cuts them into short clips with hooks and timestamps. Use when repurposing long-form video into shorts. For original B-roll, use youtube-b-roll-maker.

## skills-specialized

- `accounts-payable-agent` — Executes vendor payments, contractor invoices and recurring bills across fiat, crypto and stablecoin rails. Use when automating accounts payable or reconciling outgoing payments across rails.
- `agentic-identity-and-trust-architect` — Designs identity, authentication and trust verification for autonomous agents in multi-agent systems. Use when agents must prove who they are or delegate authority safely.
- `agents-orchestrator` — Orchestrates a multi-agent development pipeline, sequencing agents and passing state between them. Use when coordinating several agents through an end-to-end workflow.
- `automation-governance-architect` — Audits business automations (n8n-first) for value, risk and maintainability before they are built. Use when deciding whether to automate something, or reviewing a sprawling automation estate.
- `business-strategist` — Runs management-consulting analysis: competitive positioning, market entry, business model design and growth strategy. Use when evaluating a strategic move or structuring a strategy review.
- `change-management-consultant` — Guides organisations through structural and process change: impact assessment, stakeholder planning and adoption tracking. Use when a change programme needs external structure. For AI rollouts,...
- `chief-of-staff` — Runs the operating cadence behind a leader: priority triage, meeting and decision hygiene, follow-through on commitments. Use when leadership throughput is the bottleneck rather than strategy.
- `civil-engineer` — Performs structural and civil analysis against Eurocode, ACI, AISC, ASCE, AS/NZS, CSA, GB, IS and DIN. Use when checking a structural approach or comparing code requirements. Name the code; a...
- `corporate-training-designer` — Designs enterprise training: needs analysis, curriculum structure, blended delivery and evaluation. Use when building a training programme. Not for individual study plans - use study-plan-builder.
- `cultural-intelligence-strategist` — Detects invisible exclusion and adapts product and content for global and intersectional audiences. Use when localising beyond translation, or checking whether something lands outside its origin...
- `customer-success-manager` — Owns the customer relationship after onboarding: adoption tracking, health reviews and escalation. Use when managing an account's ongoing success. Not for renewals - use renewal-strategist.
- `data-consolidation-agent` — Consolidates extracted sales data into live dashboards with territory, rep and pipeline summaries. Use when merging multiple sales exports into one reporting view.
- `data-privacy-officer` — Runs the privacy programme: data mapping, lawful basis, DSAR handling, retention and breach response. Use when standing up privacy operations or assessing a processing activity. Name the jurisdiction.
- `developer-advocate` — Builds developer community and content, improves developer experience and drives adoption. Use when launching to developers, writing technical content, or diagnosing why a DX funnel leaks.
- `document-generator` — Generates PDF, PPTX, DOCX and XLSX files from code with real formatting, charts and tables. Use when producing a document programmatically rather than by hand.
- `esg-sustainability-officer` — Builds ESG reporting and sustainability programmes: materiality assessment, metrics and disclosure frameworks. Use when preparing an ESG report or selecting a disclosure standard. Name the...
- `government-digital-presales-consultant` — Handles China government digital transformation presales: policy interpretation, solution design, bid documents and POC planning. Use when pursuing a ToG opportunity in that market.
- `grant-writer` — Writes grant applications for nonprofits, research institutions and social enterprises: prospect research, letters of inquiry and full proposals. Use when applying for funding or strengthening a...
- `hiring-plan-org-chart-builder` — Designs org charts, headcount plans, levelling frameworks and hiring priority matrices by growth stage. Use when planning a team's shape or sequencing hires against budget.
- `hr-onboarding` — Runs employee onboarding: orientation, documentation, compliance tracking, benefits enrolment and culture integration. Use when designing or fixing a new-hire process.
- `identity-graph-operator` — Operates a shared identity graph so every agent in a multi-agent system resolves 'who is this' the same way. Use when identity resolution is inconsistent across agents or data sources.
- `language-translator` — Translates text while preserving register, idiom and domain terminology, flagging what does not carry across. Use when translating content that must read natively rather than literally.
- `legal-practice-assistant` — Supports legal practice: document review, clause analysis, client intake and UTBMS/LEDES billing categorisation. Use when reviewing legal documents or structuring intake. A lawyer must review the...
- `loan-officer-assistant` — Supports loan origination: application intake, document checklists, eligibility screening and file preparation for underwriting. Use when processing a loan application. Name the jurisdiction and...
- `lsp-index-engineer` — Builds and tunes Language Server Protocol indexes for fast symbol resolution across large codebases. Use when code intelligence is slow or incomplete on a big repository.
- `m-and-a-integration-manager` — Plans post-merger integration: day-one readiness, systems and process consolidation, and synergy tracking. Use when integrating an acquisition or sequencing integration workstreams.
- `mcp-builder` — Designs, builds and tests Model Context Protocol servers exposing tools, resources and prompts to agents. Use when building an MCP server or debugging why a tool is not being called.
- `medical-billing-coder` — Assigns ICD-10, CPT and HCPCS codes, checks documentation support and reduces claim denials. Use when coding an encounter or investigating a denial. A certified coder must review the result.
- `model-qa-evaluator` — Audits ML and statistical models end to end: documentation review, data reconstruction, replication and calibration testing. Use when independently validating a model before it is relied on.
- `operations-manager` — Runs day-to-day operations: process ownership, capacity planning, exception handling and performance tracking. Use when operations are reactive. Not for redesigning the process - use...
- `organizational-psychologist` — Applies organisational psychology to team dynamics, motivation, conflict and structure. Use when diagnosing why a team underperforms for reasons that are not skill or process.
- `pricing-analyst` — Analyses pricing: willingness to pay, elasticity, packaging and margin impact of a price change. Use when setting or changing a price, or modelling a packaging change.
- `real-estate-advisor` — Writes property listings, runs comparative market analysis and guides buyer and seller transaction steps. Use when marketing a property or valuing one against comparables. Name the market.
- `regulatory-compliance-officer` — Maps regulatory requirements to controls across fintech, healthcare and data privacy, with gap analysis and audit preparation. Use when preparing for an audit. Name the regulation and jurisdiction.
- `report-distribution-agent` — Schedules, formats and distributes recurring reports to the right recipients across channels. Use when automating a reporting cadence or fixing inconsistent report delivery.
- `salesforce-architect` — Architects Salesforce solutions: multi-cloud design, integration patterns, governor limits, deployment strategy and data model governance. Use when designing or untangling a Salesforce implementation.
- `supply-chain-strategist` — Plans supply chain and procurement: strategic sourcing, supplier development, quality control and digitalisation. Use when reducing supply risk, sourcing a category, or diagnosing a fragile supply...
- `talent-acquisition-manager` — Runs recruitment operations: sourcing channels, assessment frameworks and hiring compliance, with depth on China's hiring platforms. Use when building a hiring process or improving candidate quality.
- `workflow-architect` — Maps complete workflow trees for a system or user journey: happy paths, branch conditions and failure states. Use when specifying behaviour exhaustively before building.
- `zk-steward` — Maintains a Zettelkasten knowledge base in Luhmann's method: atomic notes, dense linking and emergent structure. Use when curating a linked note archive rather than a folder hierarchy.

## skills-design

- `a-b-test-designer` — Designs statistically valid A/B tests: hypothesis, variants, sample size and success metric. Use when planning a conversion test or checking whether a result is significant. Not for running the...
- `animation-planner` — Plans UI animation: what moves, easing, duration and what it communicates, without harming usability. Use when specifying motion for an interface or fixing animation that feels sluggish or gratuitous.
- `brand-guardian` — Develops and enforces brand identity: positioning, voice, visual consistency and usage rules. Use when defining a brand system or auditing work for consistency. Not for logo design - use...
- `build-premium-website` — Designs and builds high-end marketing websites with considered typography, layout and motion. Use when building a polished site from scratch or lifting an existing one out of template territory.
- `color-palette-generator` — Builds accessible palettes using colour theory with WCAG contrast ratios and dark/light variants. Use when creating a palette or fixing contrast failures. Not for dark mode conversion - use...
- `component-namer` — Suggests semantic, consistent component names following design system conventions. Use when naming components, resolving naming disputes, or bringing a sprawling component library back to a...
- `dark-mode-adapter` — Maps a light palette to dark mode, preserving hierarchy and contrast and handling elevation and shadow. Use when adding dark mode. Not for creating the original palette - use color-palette-generator.
- `design-critique` — Critiques a design against heuristics: visual hierarchy, typography, spacing, colour, accessibility and interaction. Use when reviewing a design or wanting specific, structured feedback rather...
- `figma-to-copy` — Replaces Lorem Ipsum with real, contextual copy sized to the component. Use when filling a Figma mockup with realistic text. Not for interface microcopy in production - use ux-copy-writer.
- `frontend-design` — Builds distinctive, production-grade frontend interfaces with real working code, avoiding generic AI-template aesthetics. Use when implementing a UI that has to look considered rather than default.
- `heatmap-interpreter` — Reads click, scroll and attention heatmaps to find UX friction, missed CTAs and false affordances. Use when interpreting session data or diagnosing why a page underperforms.
- `icon-brief-writer` — Writes icon design briefs specifying metaphor, style, grid, stroke weight and usage context. Use when commissioning an icon set or documenting rules for an existing one.
- `image-prompt-engineer` — Writes detailed prompts for AI image generation, translating a visual concept into subject, lighting, lens, composition and style. Use when a generated image keeps missing the intent.
- `inclusive-visuals-designer` — Generates culturally accurate, non-stereotypical imagery, countering default biases in image models. Use when creating visuals representing people, or reviewing imagery for stereotype and exclusion.
- `logo-brand-mark-designer` — Develops logomarks, logotypes and adaptive logo systems with usage guidelines. Use when creating or refining a brand mark. Not for the wider brand system - use brand-guardian.
- `motion-graphics-producer` — Specifies motion graphics: keyframes, timing, audio sync points and export settings for video and web. Use when producing an animated sequence or handing a motion spec to an editor.
- `onboarding-flow-designer` — Designs onboarding: progressive disclosure, tooltip tours, empty states and activation milestones. Use when new users drop off before first value, or when designing a first-run experience.
- `print-packaging-designer` — Produces print-ready packaging with bleed, die lines, CMYK/Pantone profiles and material specs. Use when preparing packaging artwork or checking files before they go to a printer.
- `responsive-breakpoint-advisor` — Defines breakpoint strategy, fluid type scales and adaptive layout behaviour across devices. Use when setting breakpoints or fixing layouts that break between sizes.
- `typography-system-builder` — Builds type systems: scale, font pairing, hierarchy rules, line height and vertical rhythm. Use when establishing typography for a product or fixing inconsistent text styles.
- `ui-designer` — Designs visual systems, component libraries and precise interface layouts. Use when building a UI or component set. Not for research or flows - use ux-researcher or ux-architect.
- `user-persona-builder` — Builds research-backed personas with behaviours, goals, frustrations and journey-stage context. Use when synthesising research into personas, or replacing invented personas with evidenced ones.
- `ux-architect` — Provides implementation-ready UX foundations: information architecture, CSS system structure and developer handoff guidance. Use when bridging design and build, or structuring a frontend system.
- `ux-copy-writer` — Writes interface microcopy: button labels, error messages, empty states, tooltips, confirmation dialogs and accessible text. Use when writing production UI text. Not for mockup filler - use...
- `ux-researcher` — Plans and analyses user research: usability testing, behavioural analysis and turning findings into design decisions. Use when running a study or deciding what the evidence actually supports.
- `visual-storyteller` — Builds visual narratives and multimedia brand storytelling: sequence, pacing and message through design. Use when telling a story visually rather than presenting information.
- `whimsy-injector` — Adds personality and delight to an interface - microinteractions, copy moments, easter eggs - without harming usability. Use when a product feels correct but lifeless.
- `youtube-popup-graphic` — Creates YouTube popup and overlay graphics matched to a reference image or channel theme. Use when producing an on-screen graphic for a video. Not for thumbnails - use youtube-thumbnail-maker.
- `youtube-thumbnail-maker` — Designs YouTube thumbnails with high-contrast focal points and text legible at small sizes. Use when making a thumbnail for a video. Not for in-video overlays - use youtube-popup-graphic.

## skills-business

- `ai-governance-architect` — Designs AI governance: responsible AI policy, model risk assessment, bias auditing and human-in-the-loop oversight. Use when standing up AI governance, assessing model risk, or preparing for an AI...
- `board-deck-builder` — Drafts board decks: executive summary, financial dashboard, initiative updates and governance agenda. Use when preparing a board meeting. Not for fundraising decks - use investor-pitch-deck-writer.
- `business-plan-outliner` — Builds business plans with market analysis, value proposition, revenue model, competitive positioning, go-to-market and financial projections. Use when writing a business plan or pressure-testing...
- `change-management-leader` — Plans organisational change for technology and AI rollouts using ADKAR and Kotter: stakeholder alignment, training and adoption metrics. Use when a rollout meets resistance. For general process...
- `client-proposal-writer` — Drafts client proposals with scope, deliverable timeline, pricing, case-study evidence and engagement terms. Use when responding to a client brief. Not for formal RFPs - use proposal-strategist.
- `contract-clause-explainer` — Explains contract clauses in plain language, flags risk and suggests protective amendments. Use when reviewing an NDA, SaaS agreement or MSA. Name the jurisdiction; a lawyer must review the result.
- `decision-framework` — Applies structured decision frameworks - RACI, Eisenhower, weighted scoring, decision trees - to a business choice. Use when a multi-stakeholder decision is stuck. Not for thinking models - use...
- `experiment-tracker` — Designs and tracks A/B tests and feature experiments: hypothesis, sample size, guardrail metrics and readout. Use when running an experiment or judging whether a result is real. For test design...
- `feedback-giver` — Writes constructive feedback using Situation-Behavior-Impact for performance reviews, peer reviews and 360s. Use when delivering difficult feedback or writing a review that has to land without...
- `investor-pitch-deck-writer` — Builds investor decks: problem-solution narrative, TAM/SAM/SOM sizing, traction, business model and the ask. Use when raising a round. Not for board reporting - use board-deck-builder.
- `jira-workflow-steward` — Enforces Jira-linked Git workflow: traceable commits, structured pull requests and release-safe branching. Use when tightening delivery traceability or standardising PR and branch conventions.
- `job-description-writer` — Writes role-accurate job descriptions with responsibilities, required versus preferred qualifications, pay transparency and team context. Use when opening a role or fixing a JD that attracts the...
- `meeting-summariser` — Turns meeting notes or transcripts into decisions, action items with owners and deadlines, and a parking lot. Use when summarising a meeting or extracting commitments from a long transcript.
- `negotiation-strategist` — Prepares negotiations: BATNA assessment, concession planning and scripts for contracts, vendor terms and compensation. Use when preparing for a negotiation or when a deal has stalled on price.
- `notion-database-architect` — Designs Notion workspaces with linked databases, rollups, formula fields, views and templates. Use when building a Notion system or fixing a workspace that has outgrown its structure.
- `okr-designer` — Writes measurable objectives and key results with cascading alignment from company to team to individual. Use when setting quarterly OKRs or fixing key results that are really task lists.
- `product-manager` — Owns the product lifecycle: discovery, strategy, roadmap, stakeholder alignment, go-to-market and outcome measurement. Use for product direction. Not for sprint mechanics - use sprint-prioritizer.
- `productivity-audit` — Audits individual or team workflows for time sinks, context-switching cost and tool sprawl. Use when diagnosing where the week goes or consolidating an overgrown tool stack.
- `project-manager` — Converts a spec into scoped, sequenced tasks with realistic estimates and explicit dependencies. Use when turning requirements into a plan. Not for cross-team coordination - use project-shepherd.
- `project-shepherd` — Coordinates cross-functional projects: timeline management, dependency tracking and stakeholder alignment. Use when a project spans teams. Not for breaking a spec into tasks - use project-manager.
- `sop-writer` — Writes standard operating procedures anyone can follow: numbered steps, owners, inputs, outputs and escalation paths. Use when documenting a repeatable process or onboarding someone into an...
- `sprint-prioritizer` — Plans sprints: feature prioritisation, capacity allocation and scope trade-offs. Use when planning a sprint or cutting scope against a date. Not for product strategy - use product-manager.
- `studio-operations` — Runs day-to-day studio operations: process optimisation, resource coordination and throughput. Use when operations are ad hoc. Not for multi-project portfolio calls - use studio-producer.
- `studio-producer` — Orchestrates creative and technical projects across a portfolio: resource allocation and cross-project sequencing. Use when balancing multiple projects. Not for daily ops - use studio-operations.
- `trend-researcher` — Identifies emerging market trends, analyses competitors and sizes opportunities with sourced evidence. Use when evaluating a new market, tracking a competitor, or validating that a trend is real.
- `upwork` — Builds an Upwork freelance profile and positioning: specialism, proof points and rate strategy. Use when setting up a profile or repositioning to win better work. Not for individual bids - use...
- `upwork-proposal` — Writes a proposal for a specific Upwork job: mirrors the client's stated pain, gives targeted proof and a clear next step. Use when bidding on a posting. Not for profile setup - use upwork.
- `vendor-procurement-manager` — Runs vendor selection: RFI/RFP process, scoring matrices, contract negotiation and performance tracking. Use when choosing a SaaS vendor, negotiating renewal terms, or comparing bids.
- `workflow-redesign-consultant` — Maps current-state processes, finds bottlenecks and waste, and redesigns the workflow before any AI is added. Use when a process is broken or before automating something that should be fixed first.

## skills-gamedev

- `blender-add-on-engineer` — Builds Blender Python add-ons, asset validators, exporters and pipeline automation. Use when automating repetitive DCC work, writing a Blender exporter, or validating assets before they reach the...
- `game-audio-engineer` — Integrates FMOD and Wwise, builds adaptive music systems, spatial audio and audio performance budgets. Use when wiring audio middleware, designing adaptive music, or cutting audio memory and voice...
- `game-designer` — Designs game systems and mechanics: GDD authorship, gameplay loops, economy balancing and player psychology. Use when defining core mechanics, balancing an economy, or writing a design doc. Not...
- `game-monetization-designer` — Designs free-to-play economies, battle passes and cosmetic shops with anti-predatory guardrails. Use when planning monetisation, pricing virtual goods, or reviewing a store for dark patterns.
- `godot-gameplay-scripter` — Writes Godot 4 gameplay code: GDScript 2.0, C# interop, node composition and type-safe signals. Use when structuring Godot scenes or debugging signal wiring. Not for netcode - use...
- `godot-multiplayer-engineer` — Builds Godot 4 networking: MultiplayerAPI, scene replication, ENet/WebRTC transport, RPCs and authority models. Use when adding multiplayer to a Godot game or fixing replication and authority bugs.
- `godot-shader-developer` — Writes Godot 4 shaders: Godot Shading Language, VisualShader, CanvasItem and Spatial shaders, post-processing. Use when authoring a Godot shader or profiling shader cost on a target device.
- `level-designer` — Designs level layout, pacing, encounter placement and environmental narrative. Use when blocking out a level, fixing pacing, or planning encounters. Not for mechanics themselves - use game-designer.
- `narrative-designer` — Designs branching dialogue, lore architecture and environmental storytelling aligned to the GDD. Use when structuring a branching conversation, building a lore bible, or tying story to level...
- `playtest-feedback-analyzer` — Structures playtest sessions and sorts responses into UX friction, difficulty calibration, feature satisfaction and retention risk. Use when running a playtest or turning raw feedback into a...
- `roblox-avatar-creator` — Builds Roblox UGC and avatar items: accessory rigging, texture standards and Creator Marketplace submission. Use when creating a UGC item or getting an avatar asset through moderation.
- `roblox-experience-designer` — Designs Roblox engagement loops, DataStore-driven progression and monetisation (Passes, Developer Products). Use when planning retention or monetisation. Not for writing the Luau - use...
- `roblox-systems-scripter` — Writes Roblox Luau systems: client-server security, RemoteEvents/RemoteFunctions, DataStore and module architecture. Use when building Roblox gameplay code or closing an exploit. Not for game...
- `technical-artist` — Owns the art-to-engine pipeline: shaders, VFX, LOD chains, performance budgets and cross-engine asset optimisation. Use for engine-agnostic pipeline work. For UE5 specifically, use...
- `unity-architect` — Structures Unity projects with ScriptableObjects, decoupled systems and single-responsibility components. Use when a Unity codebase is tangled, or when planning architecture for a scaling project.
- `unity-editor-tool-developer` — Builds Unity editor tooling: EditorWindows, PropertyDrawers, AssetPostprocessors, ScriptedImporters and pipeline automation. Use when automating a repetitive Unity workflow or writing a custom...
- `unity-multiplayer-engineer` — Builds Unity netcode: Netcode for GameObjects, Relay and Lobby services, client-server authority, lag compensation and state sync. Use when adding multiplayer to a Unity game or debugging desync.
- `unity-shader-graph-artist` — Authors Unity materials and VFX with Shader Graph, HLSL and URP/HDRP custom passes. Use when building a Unity shader effect or porting materials between render pipelines.
- `unreal-multiplayer-architect` — Builds Unreal networking: Actor replication, GameMode/GameState architecture, server-authoritative gameplay, prediction and dedicated servers. Use when adding multiplayer to a UE project or fixing...
- `unreal-systems-engineer` — Works the Unreal C++/Blueprint continuum with Nanite, Lumen and the Gameplay Ability System. Use when writing UE5 gameplay systems or profiling performance. Not for materials - use...
- `unreal-technical-artist` — Owns the UE5 visual pipeline: Material Editor, Niagara VFX, Procedural Content Generation and art-to-engine flow. Use for UE5 materials and VFX. For engine-agnostic pipeline work, use...
- `unreal-world-builder` — Builds UE5 open worlds with World Partition, Landscape, procedural foliage, HLOD and level streaming. Use when assembling a large world or fixing streaming hitches and draw distance.

## skills-sales-support

- `account-strategist` — Runs post-sale accounts: land-and-expand plays, stakeholder mapping, QBR facilitation and net revenue retention. Use when growing an existing account or preparing a QBR. Not for renewals - use...
- `analytics-reporter` — Turns raw data into dashboards, KPI tracking and statistical analysis with a stated recommendation. Use when building a reporting dashboard, defining KPIs, or explaining what a metric movement means.
- `churn-analyst` — Finds churn patterns, scores account health from behavioural signals and designs retention interventions. Use when diagnosing why customers leave or building an at-risk model. Not for renewal...
- `cross-channel-support-agent` — Resolves support tickets, handles escalations and drafts service-recovery responses across e-commerce, SaaS and regulated sectors. Use when answering a support ticket, defusing an escalation, or...
- `customer-support` — Writes customer support replies that acknowledge the issue, explain what happened and state the next step. Use when drafting a response to a frustrated customer or standardising support reply tone.
- `discovery-coach` — Coaches sales discovery: question design, current-state mapping, gap quantification and call structure that surfaces real buying motivation. Use when preparing or reviewing a discovery call.
- `executive-summary-generator` — Compresses complex business input into a one-page executive summary with the recommendation first, then supporting evidence. Use when writing a summary for leadership or opening a strategy document.
- `finance-tracker` — Tracks business financial health: budget management, cash flow and performance against plan. Use when monitoring spend against budget or reporting business performance. Not for modelling - use...
- `legal-compliance-checker` — Checks operations, data handling and content against applicable law and industry standards. Use when reviewing a policy, checking a claim, or assessing data handling. Name the jurisdiction; a...
- `outbound-strategist` — Designs signal-based outbound: ICP definition, multi-channel sequences and research-driven personalisation over volume. Use when building an outbound motion or defining an ICP. Not for writing the...
- `pipeline-analyst` — Diagnoses pipeline health: deal velocity, stage conversion, forecast accuracy and CRM hygiene. Use when a forecast is unreliable or pipeline is stalling. Not for coaching reps - use sales-coach.
- `proposal-strategist` — Turns an RFP or opportunity into a win narrative with win themes, competitive positioning and an executive summary. Use when responding to an RFP or structuring a proposal.
- `renewal-strategist` — Plans renewals: timeline-based outreach, expansion opportunities and QBR preparation. Use when a renewal date is approaching or building a renewal playbook. Not for churn diagnosis - use...
- `sales-coach` — Coaches reps through call reviews, pipeline reviews, deal strategy and forecast discipline. Use when developing a rep or running a deal review. Not for diagnosing pipeline data - use pipeline-analyst.
- `sales-data-extraction-agent` — Extracts MTD, YTD and year-end sales metrics from Excel files for live internal reporting. Use when pulling figures out of spreadsheet exports or automating a recurring sales report.
- `sales-engineer` — Handles pre-sales technical work: discovery, demo engineering, POC scoping and competitive battlecards. Use when preparing a technical demo, scoping a POC, or answering a security questionnaire.
- `sales-outreach` — Writes consultative B2B outreach: cold prospecting, follow-up sequences, objection handling and proposal copy. Use when writing outreach emails or handling an objection. Not for ICP strategy - use...

## skills-education

- `citation-formatter` — Formats citations and bibliographies in APA 7th, MLA 9th, Chicago/Turabian, Harvard and IEEE, with matching in-text entries. Use when formatting a reference list, converting between citation...
- `concept-explainer` — Explains a complex concept in layers - ELI5, then intermediate, then expert - using analogies and worked examples. Use when explaining something technical to a non-expert or unpacking jargon. Not...
- `essay-structurer` — Structures essays: thesis statement, argument order, evidence placement, counterargument handling and conclusion. Use when planning an essay, fixing a weak argument, or reorganising a draft that...
- `exam-question-generator` — Writes exam questions across Bloom's levels with answer keys, grading rubrics and difficulty calibration. Use when building an assessment, writing a question bank, or checking that questions match...
- `flashcard-generator` — Creates spaced-repetition flashcards using minimal-information framing and interleaved topics. Use when turning notes into Anki cards or preparing recall practice. Not for scheduling study time -...
- `historian` — Analyses historical periods, material culture and historiography, and checks period detail for anachronism. Use when researching a period, grounding fiction in authentic detail, or checking...
- `interview-prep-coach` — Prepares candidates for interviews with role-specific question banks, STAR response frameworks, mock behavioural and technical rounds, and salary negotiation. Use when preparing for an interview...
- `mental-model-teacher` — Teaches and applies mental models - first principles, inversion, second-order thinking, circle of competence - to a real decision. Use when stuck on a decision or learning a thinking framework....
- `mentor-simulator` — Runs a mentoring conversation using Socratic questioning and the GROW coaching model. Use when you want to be questioned rather than answered, or when working through a career or professional...
- `reading-list-curator` — Builds reading lists with summaries, key takeaways, difficulty ratings and a suggested order. Use when starting on a new subject, planning a self-study path, or choosing what to read next on a topic.
- `research-paper-summariser` — Summarises academic papers into methodology, findings, limitations, statistical strength and practical implications. Use when reviewing literature, triaging papers, or extracting what a study...
- `researcher` — Runs structured research on a question: scopes it, gathers and cross-checks sources, and reports findings with confidence levels and gaps. Use when investigating an unfamiliar topic and you need...
- `skill-roadmap-builder` — Builds learning roadmaps with skill trees, milestone checkpoints, resources and time estimates. Use when planning how to learn a discipline. Not for scheduling the sessions themselves - use...
- `study-abroad-advisor` — Plans study-abroad applications for the US, UK, Canada, Australia, Europe, Hong Kong and Singapore across undergraduate, master's and PhD. Use when shortlisting universities, planning application...
- `study-plan-builder` — Designs study schedules with spaced repetition intervals, active recall sessions and weekly review cycles. Use when preparing for an exam by a date. Not for choosing what to learn - use...

## skills-finance

- `bookkeeper-and-controller` — Runs day-to-day accounting: reconciliations, month-end close, journal entries and internal controls under GAAP. Use when closing the books, reconciling accounts, or preparing for audit. Not for...
- `budget-expense-auditor` — Audits budgets and expense reports for anomalies, overspending, misclassified charges and savings opportunities using variance analysis. Use when reviewing a departmental budget, auditing expense...
- `cap-table-fundraising-modeler` — Models cap tables, dilution scenarios, waterfall distributions and round structures (SAFE, convertible notes, priced rounds). Use when modelling a funding round, checking founder dilution, or...
- `chief-financial-officer` — Sets finance strategy: capital allocation, treasury, M&A finance, investor relations and board reporting. Use for board decks, runway and funding decisions, or capital structure. Not for building...
- `crypto-tax-advisor` — Calculates crypto tax: capital gains, DeFi yield, NFT trades and cross-chain activity with FIFO/LIFO/HIFO cost basis. Use when preparing a crypto tax return, computing DeFi income, or planning...
- `financial-analyst` — Builds financial models, forecasts, valuations and scenario analyses from raw data. Use when building a model, valuing a business, or stress-testing projections. Not for budget-vs-actual variance...
- `financial-plan-starter` — Builds a personal budget and money plan from income, expenses, debts and savings using a 50/30/20 split. Use when planning personal finances, paying down debt, or setting savings goals. Not for...
- `fp-and-a-analyst` — Runs budgeting, rolling forecasts and budget-vs-actual variance analysis, tying the numbers to the business narrative. Use when building an annual plan, explaining a variance, or planning...
- `insurance-actuary-analyst` — Performs actuarial work: loss ratio analysis, premium pricing, reserve estimation and risk pool segmentation. Use when pricing an insurance product, setting loss reserves, or analysing claims...
- `investment-researcher` — Researches investments: market analysis, due diligence, valuation and portfolio review across public equities, private markets and alternatives. Use when evaluating an investment, running...
- `invoice-and-payment-writer` — Drafts invoices, payment schedules and receivables documents with tax lines, payment terms and late-fee policy. Use when invoicing a client, setting payment milestones, or chasing an overdue payment.
- `tax-strategist` — Plans tax strategy: entity structure, transfer pricing, credits and multi-jurisdiction compliance. Use when reducing effective tax rate, structuring cross-border operations, or preparing a tax...

## skills-personal

- `fitness-nutrition-planner` — Builds workout programmes and nutrition plans with macro targets, progressive overload, meal prep and recovery. Use when planning training, setting macros, or structuring a training block. General...
- `habit-tracker-designer` — Designs habit systems using habit stacking, cue-routine-reward loops, tracking methods and accountability structures. Use when building a new habit, breaking an existing one, or designing a streak...
- `know-me` — Captures and maintains a personal profile - preferences, working style, context and recurring constraints - so later work can be tailored to you. Use when onboarding an assistant to your context...
- `knowledge-management-architect` — Designs knowledge systems using Zettelkasten, PARA, MOC and progressive summarisation for research synthesis. Use when choosing a note-taking methodology or structuring a knowledge base. Not tool...
- `linkedin-profile-optimizer` — Rewrites LinkedIn profiles for recruiter search and positioning: keyword-rich headline, summary and skills. Use when job hunting, repositioning after a career change, or improving profile visibility.
- `periodic-review-system` — Structures weekly, monthly and annual reviews with goal tracking, OKRs and retrospectives. Use when setting up a review cadence, running a weekly review, or planning a quarter.
- `relationship-crm-builder` — Designs a personal CRM: contact metadata, interaction logs, follow-up reminders and relationship strength scoring. Use when building a personal network tracker or setting a follow-up cadence. Not...
- `resume-optimizer` — Tailors a resume to a specific job description with ATS-safe formatting, quantified achievement bullets and keyword alignment. Use when applying for a role, adapting a resume, or diagnosing why...
- `second-brain-architect` — Sets up note-taking tools (Obsidian, Notion, Logseq) with capture workflows, tag taxonomies and retrieval patterns. Use when configuring a specific tool. Not for choosing a methodology - use...
- `travel-planner` — Builds travel itineraries with daily schedules, accommodation and transport options, budget breakdowns and local recommendations. Use when planning a trip, sequencing a multi-city route, or...

## skills-writing

- `longform-book-author` — Develops book-length non-fiction and fiction: premise, chapter architecture, narrative voice and full draft revision. Use when outlining a book, drafting chapters, or revising a manuscript. Not...
- `marketing-copywriter` — Writes bios, press releases, case studies, lead magnets and story hooks. Use when authoring an executive bio, a news release, or a B2B case study. Not for ad or landing page copy - use...
- `screenplay-writer` — Writes screenplays in industry format (Final Draft/Fountain) with scene headings, action lines, dialogue and parentheticals. Use when writing a short film, spec script, web series, or converting...
- `technical-writer` — Writes API references, user guides, setup manuals and architecture docs with consistent terminology and layered detail. Use when documenting an API, writing a how-to guide, or explaining a system...
- `thread-to-blog-converter` — Expands a Twitter/X or LinkedIn thread into a structured blog article with added context, headings and links. Use when repurposing a thread into a post. Not for writing an article from scratch -...

## skills-meta

- `create-skill` — Scaffolds a new Agent Skill: frontmatter with a trigger-rich description under 250 chars, structured body and supporting files. Use when authoring a new skill. Not for reviewing one - use...
- `prompt-library-curator` — Maintains reusable prompt libraries: versioning, tagging, benchmarking and deduplication across teams. Use when organising a shared prompt collection, versioning a prompt, or comparing prompt...
- `skill-linter` — Checks a draft SKILL.md against house conventions: description under 250 chars with a real trigger, domain-appropriate checklist, no stub text. Use when writing or reviewing a skill before...
- `skill-router` — Finds the right skill for a described task across the 12 category repos and gives the install command. Use when you know the task but not the skill name, or when checking whether a skill already...
