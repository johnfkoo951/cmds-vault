# Frontmatter Standard (Required Properties)

Every note in this vault MUST include these 7 required properties:

```yaml
---
type:           # Note type (note, meeting, people, terminology, curriculum, channel, CMDS, etc.)
aliases: []     # Alternative names (array format)
description:    # 1-2 sentence English summary for LLMs (see rule #6)
author:
  - "[[구요한]]"  # Author as quoted wikilink array
date created:   # YYYY-MM-DD or YYYY-MM-DDTHH:mm (ISO 8601)
date modified:  # YYYY-MM-DD or YYYY-MM-DDTHH:mm (ISO 8601)
tags: []        # Relevant tags (array format)
---
```

## Rules

1. **Wikilinks in YAML must be quoted**: `"[[link]]"` not `[[link]]`
2. **Date format**: Always ISO 8601 — `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm`
3. **Array format**: Use hyphen + space for arrays (author, tags, aliases)
4. **CamelCase for compound words**: `myRate`, `totalPage`, `startReadDate` (⚠️ `rating` 사용 금지 → 반드시 `myRate`)
5. **Status values** (5 options): `unread` / `reading` / `inProgress` / `completed` / `archived`
6. **`description` must be in English**: 1-2 sentences describing what the note contains and when an LLM should reference it. This is a machine-readable hint for AI agents (Claude Code, Gemini CLI, ChatGPT, etc.) to decide relevance in future sessions. Write it as a skill/tool description — specific, action-oriented, no fluff.
	- ✅ Good: `"Meeting minutes from 2026-04-07 LG AX camp retrospective. Contains CEO feedback summary and next-action items."`
	- ❌ Bad: `"회의록입니다"` (Korean, non-descriptive)
	- ❌ Bad: `"This is a note"` (no signal for relevance)

## Optional Properties

- `CMDS:` — CMDS category reference (quoted wikilink)
- `index:` — Index reference (quoted wikilink)
- `status:` — One of 5 standard values above
