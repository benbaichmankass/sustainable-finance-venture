# Skills library

Task-specific working procedures for this project. Each skill encodes a workflow that's easy to get subtly wrong — the field standards for a literature row, the boundary between the repo and the Vault, the difference between "answered" and "the reading is done".

Claude loads these automatically when a task matches the skill's `description`. You can also invoke one by name.

| Skill | Use it when |
|---|---|
| `add-literature` | Logging a paper, report or link into the literature matrix |
| `sync-drive` | Moving content between Google Drive and the repo, or filing an artifact in the Vault |
| `resolve-open-question` | Bringing evidence to bear on an unresolved decision in `data/open-questions.csv` |
| `partner-outreach` | Drafting or logging contact with partners, funders or PhD supervisors |
| `update-dashboard` | Regenerating or extending the dashboard after a content change |

## Adding a skill

Create `.claude/skills/<name>/SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: What it does and — critically — when to use it. The description is how the skill gets found, so name the trigger phrases and situations explicitly.
---
```

Then the procedure itself in markdown. Keep it to what a competent person would still get wrong without being told: the conventions, the ordering, the propagation steps, the failure mode. Don't restate general good practice.

Add a row to the table above.

## What belongs here vs. in CLAUDE.md

`CLAUDE.md` holds the standing rules — structure, conventions, standards — that apply to every session. Skills hold procedures for specific recurring tasks. If you find yourself writing "when doing X, first do Y then Z", that's a skill.
