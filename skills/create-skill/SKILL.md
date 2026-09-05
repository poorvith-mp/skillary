<!-- GENERATED MIRROR: Canonical source is skills-meta/skills/create-skill. Do not edit directly. -->
---
name: create-skill
description: >-
  Scaffolds a new Agent Skill: frontmatter with a trigger-rich description under 250 chars,
  structured body and supporting files. Use when authoring a new skill. Not for reviewing one -
  use skill-linter.
---

# Skill Creation Guide
You are an expert at creating Claude Code skills — reusable slash commands and auto-activating knowledge modules. Use this guide to create well-structured, effective skills that follow established conventions.
Read the detailed reference files for comprehensive details:
- [references/reference.md](references/reference.md) — Complete frontmatter field reference, variables, invocation control, permissions
- [references/examples.md](references/examples.md) — Real-world skill examples covering task, research, knowledge, and dynamic context patterns
## Skill Creation Workflow
### Step 1: Clarify Purpose and Type
Before writing anything, determine the skill type:
| Type | Purpose | Example |
|------|---------|---------|
| **Task** | Performs actions with side effects | deploy, commit, publish |
| **Research** | Gathers and synthesizes information | deep-research, audit |
| **Knowledge** | Provides reference context | api-conventions, style-guide |
| **Dynamic** | Injects live context via shell commands | pr-summary, env-check |
Ask the user if their intent is unclear. A skill that "deploys to production" is a Task. A skill that "explains our API patterns" is Knowledge.
### Step 2: Determine Scope
| Scope | Path | When to use |
|-------|------|-------------|
| **Personal** | `<USER_HOME>/.claude/skills/<name>/` | Workflows that apply across all your projects |
| **Project** | `.claude/skills/<name>/` | Project-specific conventions shared with the team |
Default to **project scope** unless the user explicitly wants it personal or the skill is clearly project-agnostic.
### Step 3: Choose Frontmatter Settings
Use this decision matrix:
**`name`** (required): Lowercase kebab-case. This becomes the `/slash-command` name.
**`description`** (required): Write a clear, action-oriented description. This is what Claude uses to decide whether to auto-activate the skill. Include trigger phrases the user might say.
- Good: "Build Trigger.dev background jobs, automations, and workflows in TypeScript. Use when the user wants to create tasks, scheduled jobs, AI agent workflows..."
- Bad: "Trigger.dev helper"
**`argument-hint`** (optional): Shown in autocomplete. Use square brackets: `[description of what to build]`
**Invocation control fields** — use only when needed:
- `user-invocable: false` — Skill is auto-activate only, no slash command. Use for pure knowledge/context skills.
- `auto-activate: false` — Slash command only, never auto-activates. Use for dangerous/destructive operations like deploy or delete.
- `allowed-tools` — Restrict which tools the skill can use. Use for safety-critical skills.
- `disallowed-tools` — Block specific tools. Use to prevent a skill from editing files when it should only read.
Most skills should leave invocation control at defaults (both user-invocable and auto-activate are true).
### Step 4: Write the SKILL.md
Follow this structure:
```markdown
---
name: skill-name
description: Clear description with trigger phrases...
argument-hint: [what the user provides]
---

# Title

Role statement — one sentence establishing expertise.

Reference supporting files (if any):
Read [references/reference.md](references/reference.md) for...

## Core Instructions
The main guidance. Be specific and actionable.

## Critical Rules
Numbered list of non-negotiable rules (max 10-12).

## Quick Templates
Minimal, copy-paste-ready examples for common patterns.

## Final Note
How to use arguments and any closing guidance.
```
### Step 5: Add Supporting Files (If Needed)
Use separate `.md` files in the `references/` directory for:
- Detailed API references too long for SKILL.md
- Multiple code examples that would bloat the main file
- Content that only needs to be read on-demand (not every invocation)
Reference them from SKILL.md using relative links:
```markdown
Read [references/reference.md](references/reference.md) for the complete API reference.
```
The agent will read these lazily — only when the skill is activated and the instructions tell it to.
**Do NOT use supporting files for:**
- Content under ~50 lines (just put it in SKILL.md)
- Content needed on every invocation (put it in SKILL.md)
## Critical Rules
1. **SKILL.md must be under 300 lines** — move detailed references to supporting files
2. **Use kebab-case for skill names** — `my-skill` not `mySkill` or `my_skill`
3. **Directory name must match the `name` field** — `skills/deploy/SKILL.md` with `name: deploy`
4. **Description must include trigger phrases** — agents use this for auto-activation matching
5. **Always reference supporting files via relative links** — never hardcode absolute paths
6. **Use prompt arguments for user input** — passes parameters from invocation
7. **Keep templates minimal** — show the pattern, not a complete application
8. **One skill per concern** — don't bundle unrelated functionality into one skill
9. **Test the description** — verify that realistic trigger phrases activate the skill
## Anti-Patterns to Avoid
- **Giant monolith SKILL.md** — If it's over 300 lines, split into supporting files
- **Vague descriptions** — "Helps with stuff" won't auto-activate reliably
- **Hardcoded paths** — Use relative markdown links for supporting files
- **Over-engineering frontmatter** — Most skills only need name + description
- **Duplicating built-in behavior** — Don't create a skill for things the model already does well
## Quick Templates
### Minimal Task Skill
```markdown
---
name: deploy
description: Deploy the application to production. Use when the user wants to deploy, ship, or push to prod.
argument-hint: [environment or options]
auto-activate: false
---

# Deploy Skill

You are an expert at deploying this application safely.

## Process
1. Run pre-deploy checks
2. Build the application
3. Deploy to the target environment
4. Verify the deployment

## Critical Rules
1. Always run tests before deploying
2. Never deploy with uncommitted changes
3. Confirm with the user before deploying to production

Use `$ARGUMENTS` to determine the target environment. Default to staging if not specified.
```
### Minimal Knowledge Skill
```markdown
---
name: api-conventions
description: API design conventions and patterns for this project. Use when writing new API endpoints, reviewing API code, or asking about API patterns.
user-invocable: false
---

# API Conventions

## URL Structure
- Use plural nouns: `/users`, `/orders`
- Nest for relationships: ``

## Response Format
Always return `{ data, error, meta }` envelope.

## Error Handling
Use standard HTTP status codes. Include error codes for client handling.
```
See [references/examples.md](references/examples.md) for a dynamic context skill example.
When the user describes a skill to create, use arguments as context for what they want. Follow this guide to build the complete skill: SKILL.md, supporting files if needed, and verify the directory structure is correct.
---


## Output format
- Lead with the result the user asked for.
- Use clear headings and bullet lists where helpful.
- Call out assumptions and open questions at the end.
- Stay specific to the Create Skill workflow; avoid generic filler.

## Verification & Quality Checklist

- [ ] Trigger clause names phrases a user would actually type, not the skill's own name.
- [ ] Every file the body tells the model to read exists in the skill folder.
- [ ] Instructions were run once end-to-end against a real request before shipping.
- [ ] Description states what the skill is NOT for, naming the sibling that is.

## Anti-Patterns & Constraints

- NEVER ship a skill whose referenced files do not exist.
- NEVER write a description whose trigger only fires on the skill's own name.
- NEVER pad a skill body to look substantial; a thin skill should be deleted, not inflated.
