---
type: documentation
aliases:
  - AI Agents Guide
  - Gemini Codex Guide
description: "Technical guide for non-Claude AI coding agents (Gemini CLI, Codex, Cursor, Windsurf) operating in this CMDS starter vault. Simplified and portable version of CLAUDE.md. Reference when any AI agent other than Claude Code is operating in the vault."
author:
  - "[[Me]]"
date created: 2026-01-02T16:30
date modified: 2026-04-28
tags:
  - CMDS
  - system
audience: Gemini CLI, Codex, Cursor, Windsurf
scope: technical-implementation
precedence: 2
memory-type: feedback
required-for:
  - code-generation
  - file-creation
  - file-editing
optional-for:
  - search
  - analysis
token-estimate: 3200
CMDS: "[[📚 501 Obsidian]]"
index: "[[🏛 CMDS Head Quarter]]"
version: "2.3"
status: completed
changelog:
  - "2.3 (2026-04-23): description 필드 double-quote 강제 규칙 추가"
  - "2.2 (2026-04-20): Project Overview를 starter vault 관점으로 재작성, 개인 식별 정보 placeholder화"
  - "2.1 (2026-04-07): 필수 프로퍼티 7개로 확장 (description 추가, English required)"
  - "2.0 (2026-04-01): @include 기반 공통 규칙 분리, 중복 60% 제거"
---

> **🔄 Last Updated: 2026-04-28** | Upstream reference: [system.cmdspace.work](https://system.cmdspace.work) (canonical CMDS conventions by 구요한 / Yohan Koo)

# AGENTS.md

This file provides guidance to AI coding agents (Gemini CLI, Codex, Cursor, Windsurf, etc.) when working with this CMDS-conventions vault.

> **📌 Related System Files (5 Core Files)**
> - @CLAUDE.md → [[CLAUDE]] - Claude Code specific instructions (precedence: 1)
> - @AGENTS.md → [[AGENTS]] - This file (precedence: 2)
> - @CMDS.md → [[CMDS]] - System philosophy & user context (precedence: 3)
> - @🏛 CMDS Guide → [[🏛 CMDS Guide]] - Standards & templates (precedence: 4)
> - @🏛 CMDS Head Quarter → [[🏛 CMDS Head Quarter]] - Navigation hub (precedence: 5)

---

## Project Overview

This is a **CMDS-conventions starter vault** for personal knowledge work. It implements the CMDS framework — a comprehensive Personal Knowledge Management (PKM) system with 9 major categories (100-900 series) and the CMDS Process: **Connect → Merge → Develop → Share**.

The CMDS conventions originate from 구요한 (Yohan Koo) — see canonical reference at [system.cmdspace.work](https://system.cmdspace.work). This starter is a class-friendly graft of those conventions plus optional Gobi Desktop integration.

> **Author placeholder**: System files use `[[Me]]` as a placeholder for the vault operator. Run the WELCOME ritual ([[WELCOME]]) once to batch-replace it with your actual name.

### Working Environments & Sync (선택)

<!-- TODO: 본인 환경에 맞춰 채울 것

| Environment | Machine | Base Path |
|-------------|---------|-----------|
| Primary | (your machine) | `~/Documents/cmds-vault` |

다중 머신 사용 시 두 번째 행을 추가하고, Obsidian Sync / iCloud / Dropbox 등으로 동기화 가능. 자세한 옵션은 [[CLAUDE]] "Working Environments" 섹션 참조.
-->

---

<!-- STATIC: 아래 규칙은 거의 변경되지 않습니다 -->

## Critical Rules

> 공통 규칙은 `.claude/rules/` 에 정의되어 있습니다. 아래는 AI 에이전트가 반드시 따라야 할 핵심 규칙입니다.

@.claude/rules/indentation-rules.md

@.claude/rules/frontmatter-standard.md

@.claude/rules/wikilink-rules.md

@.claude/rules/file-creation-rules.md

@.claude/rules/video-project-workflow.md

---

## Essential (Post-Compact)

> 컨텍스트 압축 후에도 반드시 기억해야 할 핵심 규칙:
> 1. **YAML frontmatter: 2 SPACES** / **Markdown body: TAB**
> 2. **Wikilinks in YAML: 반드시 큰따옴표** `"[[link]]"`
> 3. **코드 출력 경로**: `00. Inbox/03. AI Agent/{환경 하위폴더}/`
> 4. **필수 프로퍼티 7개**: type, aliases, **description** (English, 1-2 sentences for LLMs), author, date created, date modified, tags
> 5. **`description` 은 항상 double-quote `"..."`**: 안에 `: ` 또는 ` #` 들어가면 YAML plain scalar 파서 깨짐 → Obsidian Properties 렌더 실패
> 6. **날짜 포맷**: ISO 8601 (YYYY-MM-DD)
> 7. **Author**: `[[Me]]` placeholder until WELCOME ritual replaces it with the operator's name

---

## Directory Structure & CMDS Categories

@.claude/rules/directory-structure.md

---

## Obsidian Wikilinks

```markdown
[[Note Name]]              # Basic link
[[Note Name|Display Text]] # Aliased link
[[Note Name#Heading]]      # Heading link
[[Note Name^block-id]]     # Block link
![[Note Name]]             # Embed file
![[image.png]]             # Embed image
```

---

<!-- DYNAMIC: 아래 내용은 주기적으로 갱신됩니다 -->

## Common Note Types

- `note` - General notes
- `terminology` - Term definitions
- `meeting` - Meeting minutes
- `people` - People profiles
- `curriculum` - Course curriculum
- `channel` - YouTube/Blog/Newsletter 채널 프로필
- `CMDS` - CMDS index pages (replaces traditional MOC concept)
- `documentation` - Technical docs

## Status Values

Standard status values (5 options):
- `unread` - Not yet processed
- `reading` - Currently reading
- `inProgress` - Work in progress
- `completed` - Finished
- `archived` - Historical reference

## File Prefixes

- 📎 - Web Clips
- 🏷 - Index pages
- 📦 - Reviews
- 🔖 - Personal outputs
- 📜 - Others' outputs
- 📈 - Code/Syntax
- 🎹 - Music
- 📘 - Books/Reference

## Templates

Templates can live in `90. Settings/91. Templates/` (not shipped by default in this starter — create as needed). Reference templates from [[🏛 CMDS Guide]] "Properties Template Examples" section. Common starting points:

- Basic Note
- Daily Note
- Meeting Minutes
- Research Note
- People Profile

---

## CMDS Process Command Suite (2026-04-14+)

This vault has 8 slash commands aligned with the **CMDS Process** (Connect → Merge → Develop → Share). Implementation lives in `.claude/commands/` (and optionally `90. Settings/94. Agent Settings/claude/commands/`). If your agent runtime supports Claude Code-compatible slash commands, you can invoke these directly; otherwise, treat them as workflow documentation for how the user thinks about vault operations.

### Stage commands (the 4-stage knowledge lifecycle)

| Command | Stage | Fan | Role |
|---------|-------|-----|------|
| `/connect` | Connect (📖 100 Themes) | 1→1 | Inbox item → Theme stub. Auto-classifies into interest/topic/variable/terminology. Low-friction. |
| `/merge` | Merge (📖 200 Literature) | N→1 | Multiple notes → one synthesized Literature note. Heaviest command; multi-dialog flow. |
| `/develop` | Develop (📖 300-600) | 1→1 | Apply method, build artifact (code/prompt/curriculum/specialty). Code goes to `00. Inbox/03. AI Agent/` first. |
| `/share` | Share (📖 700-800) | 1→N | Orchestrate to existing skills (writer/slide makers/etc.). Never writes content directly. |

### Cross-cutting utilities

| Command | Role |
|---------|------|
| `/inbox` | Scan inbox subfolders, route to stage command. **Read-only, router only.** |
| `/lint {scope}` | Health check by stage scope (inbox/connect/merge/develop/share/all). Read-only. |
| `/query` | Search vault + registered satellites, synthesize answer, file back to appropriate CMDS category (NOT a separate folder). |
| `/status` | One-screen stage snapshot + recommended next action. Zero dialogs. |

### When to use which

```
세션 시작 / 뭐 할지 모름             → /status
방대한 inbox에서 시작                → /inbox → 라우팅
inbox 항목 빠르게 등록               → /connect
여러 노트 합성해서 한 노트로         → /merge
방법론 적용 / 코드·프롬프트 생성     → /develop
기존 합성 → 외부 산출물              → /share
볼트에 질문 (자신의 글 + 위성 볼트)  → /query
위생 점검 (모순/orphan/stale)        → /lint
```

### Key design decisions (inherited conventions)

- **CMDS Process is the operational vocabulary** — Connect/Merge/Develop/Share is the canonical way to talk about knowledge state transitions in this vault.
- **`/inbox` and `/share` never write directly** — `/inbox` is a router, `/share` is an orchestrator.
- **`/query` results are NOT folder-isolated** — they classify into the appropriate CMDS category (usually `220 Personal Insights`, `210 Literature Reviews`, `5XX Product`) and save to `30. Permanent Notes/` or similar. There is no `30. Queries/` folder.
- **CMDS categorization is metadata, not folders**: notes live in existing folder structure (`30. Permanent Notes/`, `60. Collections/`, etc.) and are categorized via `CMDS:` and `index:` frontmatter.
- **New v2 frontmatter fields** introduced by commands: `mergePurpose`, `sourceNotes`, `mainVaultRelated`, `developSources`, `shareSourceNotes`, `shareFormat`, `sharePurpose`, `queryOrigin`, `querySources`, `sourceInbox`. Use camelCase per frontmatter standard.
- **User dialog tool**: commands use `AskUserQuestion` MCP tool (if available to your agent) with `multiSelect` where applicable, max 4 options, always `(Recommended)` first.

### For agents without slash command support

If your runtime doesn't execute `/connect` etc. directly, you can still:

1. Read the command file (`.claude/commands/{name}.md`) to understand the expected workflow.
2. Execute the workflow manually using standard tool calls (Read, Write, Edit, Glob, Grep).
3. Follow the same frontmatter conventions and user-dialog checkpoints the command specifies.

The commands are self-contained markdown — each `.md` file is both the spec and the prompt.

---

## Important Notes

1. **Use wikilinks `[[]]`** for internal references, NOT markdown links
2. **Respect existing patterns** - This is a CMDS-conventions vault with established standards
3. **Check [[CMDS]]** for system context and workflow patterns
4. **Check [[🏛 CMDS Guide]]** for detailed standards and templates

---

**For Claude Code**: See [[CLAUDE]] for Claude-specific instructions.
**For System Context**: See [[CMDS]] for system philosophy and operator profile.
