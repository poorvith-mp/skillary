<!-- GENERATED MIRROR: Canonical source is skills-meta/skills/prompt-library-curator. Do not edit directly. -->
---
name: prompt-library-curator
description: >-
  Maintains reusable prompt libraries: versioning, tagging, benchmarking and deduplication across
  teams. Use when organising a shared prompt collection, versioning a prompt, or comparing prompt
  variants on a benchmark.
---

# Prompt Library Curator

Manages enterprise prompt libraries as versioned, tested, and discoverable assets that maintain consistency and quality across team AI workflows.

## Phased Workflow

### Phase 1: Library Architecture & Taxonomy
1. Define category taxonomy: by function (summarization, analysis, generation, classification, extraction), domain, and output format.
2. Establish prompt template schema: name, description, version, author, input variables, expected output format, example I/O pairs, eval criteria.
3. Set up version control: semantic versioning (major.minor.patch) with changelogs for every prompt update.

### Phase 2: Quality Assurance & Testing
1. Create evaluation datasets for each prompt template (minimum 5 test cases with expected outputs).
2. Run A/B comparisons when updating prompts: old version vs new version scored on rubric.
3. Tag prompts with model compatibility (GPT-4, Claude, Gemini) and tested model versions.

### Phase 3: Discovery & Governance
1. Build searchable catalog with tags, descriptions, and usage examples.
2. Track usage analytics: which prompts are most/least used, which have highest satisfaction scores.
3. Establish review cadence: quarterly audit of all prompts for staleness, accuracy, and relevance.

## Verification & Quality Checklist
- [ ] Every prompt has at least 3 annotated example I/O pairs.
- [ ] Version history maintained with clear rationale for each change.
- [ ] Prompts tagged with compatible model versions and last-tested date.
- [ ] Library searchable by function, domain, and output format.

## Anti-Patterns & Constraints
- NEVER deploy untested prompt changes to production workflows.
- NEVER maintain prompts without version control and changelogs.
- NEVER assume a prompt works across all model versions without explicit testing.
