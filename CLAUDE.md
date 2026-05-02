---
type: documentation
aliases:
  - Claude Code Guide
  - CC System File
description: "Claude Code specific technical implementation guide for the CMDS starter vault. Defines file creation/editing rules, YAML/Markdown indentation rules, vault commands, and code output paths. Reference when Claude Code is writing or modifying code in this vault."
author:
  - "[[구요한]]"
date created: 2025-09-27T17:53
date modified: 2026-04-28
tags:
  - CMDS
  - system
audience: Claude Code
scope: technical-implementation
precedence: 1
memory-type: feedback
required-for:
  - code-generation
  - file-creation
  - file-editing
optional-for:
  - search
  - analysis
  - reading
token-estimate: 5800
CMDS: "[[📚 501 Obsidian]]"
index: "[[🏛 CMDS Head Quarter]]"
version: "3.3"
status: completed
changelog:
  - "3.3 (2026-04-23): description 필드 double-quote 강제 규칙 추가 — YAML plain scalar의 ': ' 금지로 Obsidian Properties 렌더 깨짐 방지."
  - "3.2 (2026-04-20): Project Overview를 starter vault 관점으로 재작성, 개인 식별 정보 placeholder화."
  - "3.1 (2026-04-07): 필수 프로퍼티 7개로 확장 (description 추가, English required for LLMs)"
  - "3.0 (2026-04-01): @include 기반 공통 규칙 분리, 9개 아키텍처 패턴 적용"
---

> **🔄 Last Updated: 2026-04-28** | Upstream reference: [system.cmdspace.work](https://system.cmdspace.work) (canonical CMDS conventions by 구요한 / Yohan Koo)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this CMDS-conventions vault.

> **📌 Related System Files (5 Core Files)** — `precedence` 순서대로 로드
> - @CLAUDE.md → [[CLAUDE]] - Technical implementation (precedence: 1)
> - @AGENTS.md → [[AGENTS]] - Other AI agents guide (precedence: 2)
> - @CMDS.md → [[CMDS]] - System philosophy & context (precedence: 3)
> - @🏛 CMDS Guide → [[🏛 CMDS Guide]] - Standards & templates (precedence: 4)
> - @🏛 CMDS Head Quarter → [[🏛 CMDS Head Quarter]] - Navigation hub (precedence: 5)

<!-- STATIC: 아래 내용은 거의 변경되지 않는 규칙입니다. AI는 높은 신뢰도로 캐시할 수 있습니다. -->

## ⚠️ CRITICAL RULES — READ FIRST

> 공통 규칙은 `.claude/rules/` 에 분리되어 있습니다. 아래는 핵심 요약입니다.

@.claude/rules/indentation-rules.md

@.claude/rules/frontmatter-standard.md

@.claude/rules/wikilink-rules.md

@.claude/rules/mermaid-rules.md

### Pre-Flight Checklist (Before Every Write/Edit)

Every time you create or edit a .md file, verify:

- [ ] **YAML frontmatter uses 2 SPACES** (not tabs)
- [ ] **Markdown body uses TAB** (not spaces)
- [ ] **Wikilinks in YAML are quoted**: `"[[link]]"` not `[[link]]`
- [ ] **Mermaid node/edge labels are quoted**: `A["label"]`, no `[/` start
- [ ] **Arrays use proper format**: hyphen + space + value
- [ ] **Dates use ISO 8601**: `YYYY-MM-DD` format
- [ ] **`description` field present and in English**: 1-2 sentences explaining the note for LLMs
- [ ] **`description` wrapped in double quotes `"..."`**: unquoted `: ` or ` #` inside description breaks YAML parser and corrupts Obsidian Properties rendering
- [ ] **File saved in correct location**: Code → `00. Inbox/03. AI Agent/{environment subfolder}/`
- [ ] **Filename follows convention**: `YYYY-MM-DD-description.ext`

---

## Essential (Post-Compact)

> 컨텍스트 압축 후에도 반드시 기억해야 할 핵심 규칙:
> 1. **YAML frontmatter: 2 SPACES** / **Markdown body: TAB**
> 2. **Wikilinks in YAML: 반드시 큰따옴표** `"[[link]]"`
> 3. **Mermaid 라벨: 큰따옴표** `A["label"]` / `[/` 로 시작 금지
> 4. **코드 출력 경로**: `00. Inbox/03. AI Agent/{환경 하위폴더}/`
> 5. **필수 프로퍼티 7개**: type, aliases, **description** (English, 1-2 sentences for LLMs), author, date created, date modified, tags
> 6. **`description` 은 항상 `"..."` double-quote**: 안에 `: ` / ` #` 들어가면 YAML 파서 깨짐 (Obsidian Properties 렌더 실패)
> 7. **날짜 포맷**: ISO 8601 (YYYY-MM-DD)
> 8. **배열 포맷**: hyphen + space (`- value`)

---

## Project Overview

This is a **CMDS-conventions starter vault** for personal knowledge work. It implements the CMDS framework — a comprehensive Personal Knowledge Management (PKM) system with 9 major categories (100-900 series) — and follows the CMDS Process: **Connect → Merge → Develop → Share**.

The CMDS conventions originate from 구요한 (Yohan Koo)'s 10,000+ note vault — see canonical reference at [system.cmdspace.work](https://system.cmdspace.work). This starter is the class-friendly graft of those conventions plus optional Gobi Desktop integration.

> **Personal context (two distinct authorship identities)**:
> - **System files** (CLAUDE/AGENTS/CMDS/Guide/HQ/WELCOME/README, slash commands, rules, skills): `author: [[구요한]]` — upstream attribution. **Do not change.**
> - **User-created notes** (BRAIN.md, daily/permanent/literature notes, captures, your templates): `author: [[Me]]` is a placeholder. Run the WELCOME ritual ([[WELCOME]]) once to batch-replace `[[Me]]` with your name in **user-scope only**. The cmds-onboarding skill automates this with the same scope.

## 💻 Working Environments

<!-- TODO: 본인 환경 정보로 채울 것

이 섹션은 어떤 머신에서 이 볼트를 운영하는지, 다중 머신이면 어떻게 동기화하는지 기록합니다. 단일 머신이면 아래 표 한 줄, 다중이면 두 줄 이상.

### Primary Environment
**Base Path**: `~/Documents/cmds-vault` (or wherever you cloned)
**System**: <your machine, e.g. MacBook Pro 14">
**Status**: Primary

### (Optional) Secondary Environment — for multi-machine workflows
**Base Path**: `<absolute path on second machine>`
**System**: <second machine>
**Status**: Secondary

### Vault Sync (선택)
- Obsidian Sync (공식 클라우드) 또는 iCloud Drive / Dropbox / Syncthing 으로 동기화 가능
- 두 대 이상 사용 시 `00. Inbox/03. AI Agent/` 하위에 머신/에이전트별 서브폴더(`03-1. Claude Code (MBP)`, `03-2. Claude Code (Studio)` 등)를 두면 출처 추적 가능
- AI 코딩 결과물의 출처 분리는 협업 / 디버깅에 유용

### Claude Settings (.claude/) 동기화 (선택)
- Obsidian Sync는 `.claude/` (dotfile)을 동기화하지 않음
- 다중 머신에서 .claude/ 도 공유하려면: 원본을 `90. Settings/94. Agent Settings/claude/`에 두고 각 머신의 `.claude/` 하위 폴더를 symlink로 연결
- 자세한 절차: `.claude/rules/directory-structure.md` "Symbolic Link" 섹션 참조

-->

## 🛰 Satellite Vaults (선택)

이 mothership 볼트와 별도로 **satellite 볼트** (특수 목적의 별도 Obsidian 볼트)를 운영할 수 있습니다. Obsidian Sync 별개이며, 각자 독립 git repo 로 관리합니다.

### Registered Satellites

<!-- TODO: 위성 볼트 추가 시 아래 형식으로 채울 것. 시작 시점에는 0개.

| Satellite | Path | Purpose | Entry Point |
|-----------|------|---------|-------------|
| `<vault-name>` | `<absolute-path>` | <purpose> | [[🛰 <Vault Name> Satellite Vault]] |

예시 (구요한 메인 볼트의 경우):
| `CMDS_LLM_Wiki` | `/Users/yohankoo/Local Obsidian_MBP/CMDS_LLM_Wiki` | Karpathy LLM Wiki pattern (3-Layer: Raw Sources / Wiki / Schema). LLM ingests external sources and compiles them into a persistent wiki. | [[🛰 CMDS_LLM_Wiki Satellite Vault]] |
-->

### Cross-Vault Reference Convention

Obsidian does not support direct wikilinks between vaults. Use the following:

**To reference satellite notes from this (mothership) vault:**

```yaml
# Frontmatter
source-vault: <satellite-vault-name>
related:
  - "[[🛰 <Vault Name> Satellite Vault]]"  # always link the entry point
```

```markdown
# Body text (concrete satellite pages)
→ <Vault Name>: <page name>
```

**To reference this vault from satellite:**

Satellite notes use `source-vault: <this-vault-name>` and body text like `→ <This Vault>: {category}/{note name}`.

### When to Work in Which Vault

- **Mothership (here)**: 개인 PKM, 일지, 프로젝트 추적, 강의, 생활 컨텍스트
- **Satellite**: LLM 주도 deep-dive (예: ingested sources 컴파일), 또는 명확히 분리된 도메인
- 불확실하면: 주 저자가 LLM(raw source 컴파일)이면 satellite, 인간(직접 기록·사고)이면 mothership

### Cross-Vault Query (선택, 고급)

위성 볼트의 컴파일된 지식을 mothership 세션에서 바로 검색하려면 **qmd MCP** 같은 user-scope 검색 도구를 cwd 무관하게 등록할 수 있습니다.

**가능한 것**:

```
✅ qmd MCP 로 위성 볼트 의미 검색
   mcp__qmd__query(searches=[{type:"vec", query:"..."}])

✅ Grep/Read에 명시 path
   Grep(pattern="...", path="<satellite-vault-absolute-path>")
```

**불가능한 것**:

```
❌ [[Other Vault Page]] 직접 wikilink — 볼트 경계 못 넘음 (반드시 텍스트 참조 사용)
```

**도구 선택 규칙**:

| 상황 | 도구 | 이유 |
|------|------|------|
| 정확한 파일명/제목 안다 | `Grep` + path 명시 | 빠르고 결정적 |
| 추상 쿼리 / 의미 검색 / 관련 개념 묶음 | semantic search MCP (qmd 등) | cross-reference 자동 surfacing |
| 키워드는 명확하지만 어디 있는지 모름 | lexical 먼저, fallback semantic | 키워드 매칭 + 의미 보강 |

**인용 표기**: 본문에서는 `→ <Vault Name>: {page name}` 텍스트 참조로 크로스-볼트 링크 표시.

---

## CMDS Process Command Suite (2026-04-14+)

This vault has 8 slash commands aligned with the **CMDS Process** (Connect → Merge → Develop → Share). They live in `.claude/commands/` and (optionally) `90. Settings/94. Agent Settings/claude/commands/`.

### Command Map

| Command | Type | Role | Key dialogs |
|---------|------|------|-------------|
| `/inbox` | Router | Scan inbox subfolders, AskUserQuestion to route to a stage command | scope + stage |
| `/connect` | Stage | Triage inbox → 100 Themes (interest/topic/variable/term). **Auto-classifies, auto-dedupes, auto-stubs.** | only at ambiguity |
| `/merge` | Stage | N inbox/Theme notes → 1 synthesized 200 Literature note. **Heaviest command, most dialogs.** | purpose, candidates, angle, draft review |
| `/develop` | Stage | Apply method/build artifact → 300-600 (code, prompts, specialty, curriculum). | artifact type, review |
| `/share` | Stage / Orchestrator | Auto-delegate to existing skills (writer skills, slide makers, etc.) → 700-800 | format, tone (when needed) |
| `/lint` | Cross-cutting | Health check by stage scope (inbox/connect/merge/develop/share/all). **Read-only**, surfaces issues. | only if user asks for fix |
| `/query` | Cross-cutting | Search vault + registered satellites, synthesize answer, optionally file back into appropriate CMDS category (NOT a separate /queries folder). | wiki-worthy + classify |
| `/status` | Cross-cutting | One-screen vault stage snapshot + recommended next action. **Zero dialogs**, fast. | none |

### Decision Tree (When to Use Which)

```
세션 시작 / 뭐 할지 모름
  └─→ /status  (한 화면 요약 + 추천 액션)

방대한 inbox에서 시작
  └─→ /inbox  → AskUserQuestion으로 라우팅

inbox 항목 빠르게 분류·등록
  └─→ /connect  (low-friction, Theme stub)

여러 노트 합성해서 한 노트로 만들고 싶음
  └─→ /merge  (multi-dialog, Literature 산출)

방법론을 데이터/도구에 적용 / 코드·프롬프트 생성
  └─→ /develop  (artifact-producing)

기존 합성을 외부용 산출물로 (뉴스레터/슬라이드/SNS 등)
  └─→ /share  (skill 오케스트레이션)

볼트에 질문하기 (자신의 글 + 위성 볼트 동시 검색)
  └─→ /query  (답변 + 가치 있으면 해당 CMDS 카테고리에 file back)

위생 점검 (모순/orphan/stale)
  └─→ /lint {scope}  (read-only)
```

### Settled Design Decisions

- **Vocabulary**: stage commands use the CMDS framework (Connect/Merge/Develop/Share). Stay in this vocabulary instead of inventing new verbs.
- **Inbox is router-only**: `/inbox` never writes; it only scans, summarizes, and uses `AskUserQuestion` to route.
- **`/share` as orchestrator, not writer**: auto-delegates to existing skills. Never produces content directly. Routing map maintained in `share.md`.
- **`/query` results are NOT folder-isolated**: Query results that survive the wiki-worthiness gate get classified into the appropriate CMDS category (220 Personal Insights, 210 Literature Reviews, 5XX Product, etc.) and saved to the correct physical folder (mostly `30. Permanent Notes/`).
- **Automation density per command**: `/connect` auto-pilots with minimal user input; `/merge` deliberately preserves multi-dialog because synthesis involves information loss; `/develop` and `/share` ask only at the type/format decision; `/lint` and `/status` are zero-dialog.
- **`AskUserQuestion` everywhere**: stage commands use the MCP tool with multiSelect where applicable, max 4 options per question. Always include a "(Recommended)" first option based on context.
- **CMDS categorization is metadata, not folders**: there is no `100/`, `200/`, etc. physical folder. Notes live in the existing folder structure (`30. Permanent Notes/`, `60. Collections/`, etc.) and are categorized via `CMDS:` and `index:` frontmatter.
- **All commands honor pre-flight rules**: `frontmatter-standard.md`, `wikilink-rules.md`, `indentation-rules.md`, `file-creation-rules.md`. New v2 fields introduced: `mergePurpose`, `sourceNotes`, `mainVaultRelated`, `developSources`, `shareSourceNotes`, `shareFormat`, `sharePurpose`, `queryOrigin`, `querySources`.

### Typical Session Patterns

**Daily**: `/status` → `/inbox` → (`/connect` 또는 `/merge`) → 종료
**Weekly**: `/lint inbox` → 정리 후 `/merge {topic}` → `/share` (필요 시)
**프로젝트 작업**: `/query {topic}` → `/merge {topic}` → `/develop` 또는 `/share`
**시스템 점검 (월 1회)**: `/lint all`

---

## System Documentation Structure

This vault has **5 core system files** that work together to provide complete guidance:

### 🤖 AI Documents (loaded into context window)

| File                      | Purpose                        | Audience              | Focus                                               |
| ------------------------- | ------------------------------ | --------------------- | --------------------------------------------------- |
| **CLAUDE.md** (this file) | Technical implementation guide | Claude Code           | **HOW** - Code workflows, file operations, commands |
| **AGENTS.md**             | General AI coding agent guide  | Gemini CLI, Codex etc | **HOW** - Technical rules for other AI agents       |
| **CMDS.md**               | Context & philosophy guide     | All LLM assistants    | **WHY & WHAT** - System purpose, user context       |

### 👤 Human Documents (referenced in Obsidian)

| File                        | Purpose               | Audience  | Focus                                 |
| --------------------------- | --------------------- | --------- | ------------------------------------- |
| **🏛 CMDS Head Quarter.md** | Navigation hub        | User      | **WHERE** - Category map, quick links |
| **🏛 CMDS Guide.md**        | Operational standards | User + AI | **STANDARDS** - Properties, templates |

### When to Use Which File

- **You are here (CLAUDE.md)**: For Claude Code technical implementation
	- File creation/editing rules
	- Obsidian-specific syntax (wikilinks, YAML)
	- Vault commands and operations
	- Code output location (`00. Inbox/03. AI Agent/`)

- **Use AGENTS.md**: For other AI coding agents (Gemini CLI, Codex, Cursor, etc.)
	- General technical rules without Claude-specific content

- **Use CMDS.md**: For understanding context and purpose
	- Why this system exists
	- Vault operator profile (the `(Your Name)` placeholder you'll replace)
	- Detailed explanation of 9 categories (100-900)
	- CMDS Process (Connect → Merge → Develop → Share)

- **Use [[🏛 CMDS Head Quarter]]**: For navigation
	- Quick access to all 91 subcategories

- **Use [[🏛 CMDS Guide]]**: For standards compliance
	- Required Properties format
	- Standard note types
	- File naming conventions

**Remember**: This file (CLAUDE.md) is **Claude Code specific**. For other AI agents, use **AGENTS.md**.

## File Creation Rules

@.claude/rules/file-creation-rules.md

## Video Project Workflow

@.claude/rules/video-project-workflow.md

## Directory Structure

@.claude/rules/directory-structure.md

---

## CMDS-Specific Conventions

### Hierarchy System
- 🏛 - Home/Guide notes (top level)
- 📖 - 1st level CMDS (100-900 series)
- 📚 - 2nd level CMDS (N01-N99)
- (No icon) - 3rd level (detailed topics)

### File Prefixes
- 📎 - Web Clips
- 🏷 - Index
- 📦 - Review
- 🔖 - Personal idea outputs
- 📜 - Others' idea outputs
- 📈 - Code/Syntax
- 🎹 - Music
- 📘 - Books/Reference

### Note Types (type property)
Common types in a CMDS vault:
- `note` - General notes
- `terminology` - Term definitions
- `research-pipeline` - Research pipeline documents
- `meeting` - Meeting notes
- `people` - People profiles
- `curriculum` - Course curriculum
- `channel` - YouTube/Blog/Newsletter 채널 프로필
- `CMDS` - CMDS index pages (replaces traditional MOC concept)
- `api` - API documentation
- `moc` - Map of Content
- `manuscript` - Manuscripts and drafts

## Obsidian-Specific Guidelines

### Markdown Files
- Always use wikilinks `[[]]` for internal references, NOT markdown links
- Include YAML frontmatter for metadata (see @.claude/rules/frontmatter-standard.md)
- Standard frontmatter fields:
	- `type:` - Note type/category (see types above)
	- `aliases:` - Alternative names (array format)
	- `description:` - English 1-2 sentence summary (double-quoted)
	- `author:` - Author information (array format with quoted wikilinks; user-note default is `[[Me]]` placeholder until WELCOME ritual run. System files always `[[구요한]]`)
	- `date created:` - Creation timestamp (YYYY-MM-DD format)
	- `date modified:` - Last modification (YYYY-MM-DD format)
	- `tags:` - Relevant tags (array format)
	- `CMDS:` - CMDS category reference (quoted wikilink if used)
	- `index:` - Index reference (quoted wikilink if used)
	- `status:` - unread/reading/inProgress/completed/archived

### Note Templates
Templates can live in `90. Settings/91. Templates/` (not shipped by default in this starter — create as needed). Reference templates from the [[🏛 CMDS Guide]] "Properties Template Examples" section.

### Special Characters in Titles
The vault uses emoji prefixes systematically:
- `🏛` - Main index/guide notes (CMDS Guide, CMDS Head Quarter)
- `📖` - Category collections (100-900 series)
- `📚` - Subcollections (2nd level)
- `🏷` - Tag/index pages

### Mermaid Diagrams
Full rules: `.claude/rules/mermaid-rules.md`

핵심 3가지:
- **모든 라벨을 큰따옴표로**: `A["시작"] --> B{"조건?"}`
- **`[/` 로 시작 금지**: trapezoid 도형 기호로 파싱됨 → `C["/query 스킬"]`로 작성
- **엣지 라벨도 따옴표**: `B -->|"라벨"| C`

## Key Integration Points

### Main Hub Notes
- [[🏛 CMDS Head Quarter]] - Central navigation hub with 9 categories
- [[🏛 CMDS Guide]] - Properties standardization and operational guidelines

### AI Integration
- Claude Code via slash commands in `.claude/commands/` (8개: connect/merge/develop/share/inbox/lint/query/status)
- Other AI assistants — Gemini CLI, Codex, Cursor — read AGENTS.md
- Agent settings: `.claude/{agents,commands,rules,skills}/` 가 default 위치. Multi-machine sync 시 `90. Settings/94. Agent Settings/claude/` 를 원본으로 두고 symlink 권장 (자세한 절차는 `.claude/rules/directory-structure.md` 참조)

### Automation (선택)
- n8n / Make.com workflows
- Obsidian Webhook integration
- API integrations (OpenAI, Anthropic, Google)

## Obsidian CLI (v1.12+, 선택)

Obsidian CLI는 터미널에서 Obsidian을 직접 제어하는 명령줄 인터페이스입니다.
**Claude Code에서 `obsidian` 명령을 Bash 도구로 호출하여 Obsidian 네이티브 기능을 활용할 수 있습니다.**

### 요구사항
- Obsidian 1.12+ (Early Access, Catalyst 필요)
- Settings → General → CLI 활성화
- Obsidian 앱 실행 중이어야 함

### Claude Code에서 사용 시 주의사항
- `obsidian` 명령은 Bash 도구로 호출
- 볼트 타겟팅: `obsidian vault=<your-vault-name> <command>`
- 파일 타겟팅: `file=<name>` (wikilink 방식) 또는 `path=<경로>` (볼트 루트 기준)
- 출력 복사: `--copy` 플래그

### 자주 쓰는 CLI 명령 (Quick Reference)

```bash
# --- 읽기/검색 ---
obsidian read file=<name>                          # 파일 내용 읽기
obsidian search query="<text>" format=json          # 볼트 검색
obsidian tags all counts sort=count                 # 태그 통계
obsidian properties all counts sort=count           # 프로퍼티 통계
obsidian backlinks file=<name> counts               # 백링크 조회
obsidian outline file=<name> format=tree            # 목차 조회
obsidian tasks daily todo                           # 오늘 미완료 태스크

# --- 생성/편집 ---
obsidian create name=<name> template=<template> silent  # 템플릿으로 노트 생성
obsidian append file=<name> content="<text>"            # 내용 추가
obsidian prepend file=<name> content="<text>"           # frontmatter 뒤에 삽입
obsidian daily:append content="- [ ] <task>" silent     # 데일리 노트에 태스크 추가
obsidian property:set name=<key> value=<val> file=<name> # 프로퍼티 설정
obsidian property:remove name=<key> file=<name>          # 프로퍼티 제거

# --- 분석 ---
obsidian vault info=files                           # 볼트 파일 수
obsidian orphans total                              # 고아 노트 수
obsidian unresolved verbose                         # 미해결 링크
obsidian deadends total                             # 아웃링크 없는 노트 수

# --- 개발자 ---
obsidian eval code="<javascript>"                   # JS 실행 (app.vault 등 접근)
```

### CLI vs 파일 직접 조작 가이드

| 작업 | CLI 사용 | 파일 직접 조작 |
|------|---------|-------------|
| 프로퍼티 수정 | `property:set` ✅ (안전) | Edit 도구 (YAML 직접 편집) |
| 내용 추가 | `append`/`prepend` ✅ | Edit/Write 도구 |
| 노트 생성 (템플릿) | `create template=` ✅✅ | Write 도구 (수동 복제) |
| 검색 | `search` ✅ (Obsidian 인덱스) | Grep 도구 (파일 시스템) |
| 백링크/링크 분석 | `backlinks`/`orphans` ✅✅ | 불가능 |
| Obsidian API 접근 | `eval` ✅✅ | 불가능 |

---

## Vault Commands

### Note Creation with Proper Metadata

```bash
cat > "00. Inbox/$(date +%Y-%m-%d)-new-note.md" << 'EOF'
---
type: note
aliases: []
description: ""
author:
  - "[[Me]]"
date created: $(date +%Y-%m-%d)
date modified: $(date +%Y-%m-%d)
tags: []
CMDS:
index:
status:
---

# Title

EOF
```

### Vault Analysis Commands

```bash
find . -name "*.md" -type f | wc -l

grep -L "^type:" **/*.md 2>/dev/null | head -20

grep -h "^type:" **/*.md | sort | uniq -c | sort -rn

find . -name "*.md" -mtime -7 -type f | head -20
```

<!-- DYNAMIC: 아래 내용은 주기적으로 갱신될 수 있습니다 -->

## Critical Workflow Rules

1. **Code Output Location**: ALL code MUST go to `00. Inbox/03. AI Agent/{environment subfolder}/`
2. **Required Properties**: Every note needs 7 fields: type, aliases, **description** (English, double-quoted, LLM hint), author, date created, date modified, tags
3. **Properties v2.0 Standards**:
	- Dates: ISO 8601 (YYYY-MM-DD)
	- Author (your notes): `[[Me]]` placeholder until WELCOME ritual; thereafter `[[Your Name]]` wikilink. Author (system files): always `[[구요한]]`.
	- Status: Use standard 5 values only
	- CamelCase: myRate, totalPage (⚠️ `rating` 사용 금지 → 반드시 `myRate`)
	- **description**: English only, 1-2 sentences, double-quoted, skill-description style
4. **CMDS Hierarchy**: 🏛 (top) → 📖 (100-900) → 📚 (N01-N99) → no icon (details)
5. **Respect existing patterns**: this is a CMDS-conventions vault — review [[🏛 CMDS Guide]] before deviating

## Recommended Obsidian Plugins

- **Dataview**: Dynamic queries and data aggregation
- **Smart Connections**: AI-based note linking
- **Excalidraw / Excalibrain**: Visual thinking and diagramming
- **Calendar**: Date-based note organization
- **Templater** (선택): 템플릿 자동화 강화
- **Supercharged Links**: 노트 타입별 시각 강조
