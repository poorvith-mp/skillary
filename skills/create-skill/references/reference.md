# Agent Skill Specification & Frontmatter Reference

Comprehensive reference for authoring portable Agent Skills compatible with Claude Code, Codex, Cursor, Gemini CLI, and `npx skills`.

## Frontmatter Fields

### Universal Standard Fields
- `name` (required, string): Clean kebab-case identifier (max 64 characters). Must match folder name.
- `description` (required, string): What the skill does and when to activate. Include verbatim trigger phrases in the first 200 characters followed by negative disambiguation ("Not for X — use Y"). Max 1024 characters.

### Optional & Agent-Specific Fields
- `argument-hint` (optional, string): Displayed in CLI completion prompts to indicate parameter expectations (e.g. `"[issue-number]"`).
- `disable-model-invocation` (optional, boolean): Set to `true` to require explicit invocation by the user (prevents background model auto-activation).
- `license` (optional, string): SPDX license identifier (e.g. `MIT`, `Apache-2.0`).

## Directory Structure
```plain text
skills/<skill-name>/
├── SKILL.md                 # Primary instructions & procedure
├── <skill-name>.skill       # Generated zip bundle for drag-and-drop
├── references/              # Detailed guides loaded on demand
│   ├── reference.md
│   └── examples.md
└── scripts/                 # Optional non-network helper scripts
```

## Security & Privacy Invariants
- Zero network egress outside explicitly declared user workflows.
- No credential harvesting or reads outside the working directory.
- Standard library first before external dependencies.
