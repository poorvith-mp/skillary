# Agent Skill Authoring Examples

Real-world patterns across Task, Knowledge, and Dynamic skills.

## 1. Task Skill Example
A task skill that performs focused, atomic modifications.

```markdown
---
name: sk-format-changelog
description: >-
  Formats and categorizes git commits into a clean CHANGELOG release section.
  Use when preparing release notes, or when the user says 'format changelog,'
  'generate release notes,' or 'update changelog.'
---

# Format Changelog

1. Ask for the target release version tag if not provided.
2. Run `git log <previous-tag>..HEAD --oneline` to inspect commit subjects.
3. Group commits by Conventional Commits type (`feat`, `fix`, `perf`, `docs`).
4. Output the categorized markdown block ready for commit.
```

## 2. Knowledge Skill with References Example
A skill providing deep architectural guidance via on-demand references.

```markdown
---
name: sk-api-guidelines
description: >-
  Applies internal REST API standards: error envelopes, pagination, and versioning.
  Use when designing endpoints, reviewing API PRs, or defining route schemas.
---

# API Guidelines

Consult [references/envelope-spec.md](references/envelope-spec.md) for JSON response structures.
Always validate query parameters before database queries.
```
