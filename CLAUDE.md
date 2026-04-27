---
type: documentation
aliases:
  - Claude Code Guide
  - CC System File
description: Claude Code specific technical implementation guide. Defines file creation/editing rules, YAML/Markdown indentation rules, vault commands, and code output paths. Reference when Claude Code is writing or modifying code in the CMDS vault.
author:
  - "[[구요한]]"
date created: 2025-09-27T17:53
date modified: 2026-04-18T15:40
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
version: "3.1"
status: completed
changelog:
  - "3.1 (2026-04-07): 필수 프로퍼티 7개로 확장 (description 추가, English required for LLMs)"
  - "3.0 (2026-04-01): @include 기반 공통 규칙 분리, 9개 아키텍처 패턴 적용"
  - "2.1 (2026-03-30): frontmatter 표준 추가, 백업 경로 이동"
  - "2.0 (2026-03-15): 전면 리뷰, 통계 갱신, GitHub/Web 링크"
---
> **🔄 Last Updated: 2026-04-18** | Backup: `40. Docs/47. CMDS Docs/cmds-system-files/CLAUDE_backup.md` | GitHub: [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) (코드 히스토리, 자동 배포 아님) | Web: [system.cmdspace.work](https://system.cmdspace.work) (Vercel `cmds-system-files-v2`)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **📌 Related System Files (5 Core Files)** — `precedence` 순서대로 로드
> - @CLAUDE.md → [[CLAUDE.md]] - Technical implementation (precedence: 1)
> - @AGENTS.md → [[AGENTS.md]] - Other AI agents guide (precedence: 2)
> - @CMDS.md → [[CMDS.md]] - System philosophy & context (precedence: 3)
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
> 6. **날짜 포맷**: ISO 8601 (YYYY-MM-DD)
> 7. **배열 포맷**: hyphen + space (`- value`)

---

## Project Overview

This is an Obsidian vault for the CMDSPACE knowledge management system created by Yohan Koo. It implements the CMDS framework - a comprehensive Personal Knowledge Management (PKM) system with 9 major categories (100-900 series) and follows the CMDS Process: Connect → Merge → Develop → Share.

## 💻 Working Environments

This vault is accessed from two different Mac environments:

### Primary Environment (MacBook Pro) ✅
**Base Path**: `/Users/yohankoo/Local Obsidian_MBP/CMDSPACE_Local_MBP`

**System**: MacBook Pro (16-inch)
**Status**: Primary (Most Frequently Used)
**Usage**: Main development and knowledge management workstation

### Secondary Environment (Mac Studio)
**Base Path**: `/Users/yohankoo/Obsidian_Local/CMDSPACE_Studio_Local_Org`

**System**: Mac Studio
**Status**: Secondary
**Usage**: Desktop workstation for heavy processing tasks

### Vault Sync
- Two machines are synced via **Obsidian Sync** (official Obsidian cloud server)
- The vault structure and all files/subfolders remain identical across both environments
- Sync is automatic and continuous — changes on one machine propagate to the other

### Claude Settings Sync (Symlink Strategy) — 결정 로그 (2026-04-14)

Obsidian Sync 는 dotfile (`.claude/`) 을 동기화하지 않기 때문에, Claude 설정/스킬/룰을 두 Mac 간 공유하려면 **볼트 내 경로** 에 원본을 둬야 한다.

**결정**: `90. Settings/94. Agent Settings/claude/` 를 **원본** 으로 두고, 각 Mac 의 `.claude/` 하위 폴더 4개를 이 원본으로 향하는 심볼릭 링크로 연결한다.

```
.claude/
├── agents   → ../90. Settings/94. Agent Settings/claude/agents    (symlink)
├── commands → ../90. Settings/94. Agent Settings/claude/commands  (symlink)
├── rules    → ../90. Settings/94. Agent Settings/claude/rules     (symlink)
├── skills   → ../90. Settings/94. Agent Settings/claude/skills    (symlink)
├── settings.json         (머신 로컬 전용 — symlink 안 함)
├── settings.local.json   (머신 로컬 전용 — symlink 안 함)
└── sessions/             (머신 로컬 전용 — symlink 안 함)
```

**이유**:
- 두 Mac 이 동일한 유저명/볼트명/경로 구조를 쓰므로, 상대 경로 symlink (`../90. Settings/...`) 가 양쪽에서 동일하게 resolve 된다.
- `settings.json`, `sessions/` 같은 머신 로컬 상태는 공유되면 충돌하므로 symlink 대상에서 제외.
- 새 Mac 에서 수동 설정하는 법은 `.claude/rules/directory-structure.md` 의 "Symbolic Link" 섹션 참조.

**주의**: Obsidian Sync 가 symlink 자체를 실체 폴더로 복제해버리는 경우가 있다. 새 Mac 에서 처음 볼트를 받으면 `.claude/` 가 일반 폴더일 수 있으니, **각 Mac 마다 symlink 를 수동으로 재설정** 해야 한다.

### 📦 System Files Deployment (system.cmdspace.work)

**5개 시스템 파일(CLAUDE, AGENTS, CMDS, HQ, Guide)** 은 `system.cmdspace.work` 에 공개 배포됩니다. 배포 스택/경로/명령은 아래와 같습니다.

#### 배포 스택

| 레이어 | 서비스 | 설정 |
|--------|--------|------|
| **DNS** | Cloudflare | `cmdspace.work` (Free tier) · Account: `Cmdspace.contact@gmail.com` |
| **DNS Record** | Cloudflare | `system` → A `76.76.21.21` · Proxy **OFF** (DNS only) |
| **Hosting** | Vercel | Team: `johnfkoo951's projects` (Hobby) · Project: **`cmds-system-files-v2`** |
| **Project ID** | Vercel | `prj_CDfy1Qhc2WmxI2nj76w0EJv3zq8h` |
| **Domain binding** | Vercel | `system.cmdspace.work` + `files.cmdspace.work` (같은 프로젝트) |
| **Git Integration** | — | ❌ 없음 (CLI 수동 배포만) |

> **왜 `-v2`?**: Vercel 프로젝트 이름의 일련번호. 1차 시도 프로젝트 `cmds-system-files` 는 도메인 미연결 상태로 orphaned. 2차로 생성한 `cmds-system-files-v2` 가 현행. **시스템 파일 콘텐츠 버전(v4.2)과는 무관**.

#### 배포 소스 폴더 (DEV)

**`/Users/yohankoo/DEV/cmds-system-files/`** 가 배포 소스입니다. 구조:

```
/Users/yohankoo/DEV/cmds-system-files/
├── index.html                    ← 메인 웹페이지 (Brutalist Edition)
├── README.md                     ← GitHub 리드미
├── CHANGELOG.md                  ← 버전 이력
├── .vercel/project.json          ← Vercel 링크 (gitignored)
├── files/                        ← 다운로드 배포본
│   ├── CLAUDE.md, AGENTS.md, CMDS.md, CMDS-Guide.md, CMDS-Head-Quarter.md
│   ├── CMDS-System-Files.zip     ← 위 5개 + rules/ 번들
│   └── rules/ (7개 .md)          ← .claude/rules/ 미러
└── rules/ (7개 .md)              ← 레포 루트에도 복사본
```

#### 동기화 플로우 (볼트 → 프로덕션)

```
[볼트 원본]                                         [GitHub]
 CLAUDE.md              ┐                           johnfkoo951/cmds-system-files
 AGENTS.md              │                                    ↑
 CMDS.md                │ system-docs-updater 스킬     git push (선택, 백업용)
 🏛 CMDS Guide.md       │ (복사 + ZIP 재생성)                │
 🏛 CMDS Head Quarter.md│                                    │
 .claude/rules/*.md (7) │                            [DEV]   │
                        └─→ /Users/yohankoo/DEV/cmds-system-files/
                                    │
                                    │ vercel deploy --prod --yes
                                    ↓
                             [Vercel] cmds-system-files-v2
                                    │
                                    │ 도메인 바인딩
                                    ↓
                             system.cmdspace.work  (Cloudflare DNS A → Vercel IP)
```

#### 배포 명령 (최소)

```bash
cd /Users/yohankoo/DEV/cmds-system-files
vercel deploy --prod --yes
```

→ `system.cmdspace.work` 에 즉시 반영 (캐시 갱신 포함).

#### 새 Mac 에서 배포 권한 확보

DEV 폴더가 Vercel 프로젝트에 링크돼 있지 않다면 (`.vercel/` 없음) 한 번만 실행:

```bash
cd /Users/yohankoo/DEV/cmds-system-files
vercel link --project cmds-system-files-v2 --yes
```

#### 전체 흐름 자동화 (system-docs-updater 스킬)

```
볼트 파일 수정
  ↓
"sync system files 배포" 또는 skill 호출
  ↓
스킬이 5개 MD + 7개 rules 을 DEV/ 에 복사
  ↓
ZIP 재생성 (DEV/files/CMDS-System-Files.zip)
  ↓
vercel deploy --prod  (수동으로 실행)
```

자세한 스킬 동작은 `system-docs-updater` 참조.

### Important Notes:
- All relative paths in this document (e.g., `00. Inbox/03. AI Agent/`) are relative to the base path above
- When switching between environments, Claude Code will automatically use the appropriate base path
- AI coding outputs are separated by environment subfolder (`03-1` ~ `03-4`) to track which machine/agent created each file

## 🛰 Satellite Vaults

This mothership vault has companion **satellite vaults** — separate Obsidian vaults with specialized purposes. Not part of Obsidian Sync; each has its own git repo.

### Registered Satellites

| Satellite | Path | Purpose | Entry Point |
|-----------|------|---------|-------------|
| `CMDS_LLM_Wiki` | `/Users/yohankoo/Local Obsidian_MBP/CMDS_LLM_Wiki` | Karpathy LLM Wiki pattern implementation (3-Layer: Raw Sources / Wiki / Schema). LLM ingests external sources (articles, papers, transcripts) and compiles them into a persistent wiki. | [[🛰 CMDS_LLM_Wiki Satellite Vault]] |

### Cross-Vault Reference Convention

Obsidian does not support direct wikilinks between vaults. Use the following:

**To reference satellite notes from this (mothership) vault:**

```yaml
# Frontmatter
source-vault: CMDS_LLM_Wiki
related:
  - "[[🛰 CMDS_LLM_Wiki Satellite Vault]]"  # always link the entry point
```

```markdown
# Body text (concrete satellite pages)
→ LLM Wiki: LLM Wiki Pattern (Concepts)
→ LLM Wiki: MOC-Knowledge Management
```

**To reference this vault from satellite:**

Satellite notes use `source-vault: CMDSPACE_Local_MBP` and body text like `→ CMDSPACE: {category}/{note name}`.

### When to Work in Which Vault

- **Mothership (here)**: personal PKM, journals, project tracking, lectures, life context
- **Satellite LLM Wiki**: LLM-driven deep-dive into an external topic via ingested sources
- When uncertain: if the primary author is the LLM compiling raw sources, it belongs in the satellite; if the primary author is the human recording/thinking, it belongs here.

### Cross-Vault Query from Mothership

메인 볼트 세션에서도 **`CMDS_LLM_Wiki` 볼트의 컴파일된 지식을 바로 검색/인용 가능**하다. Obsidian wikilink는 볼트 경계를 넘지 못하지만, qmd MCP는 user-scope로 등록되어 cwd 무관하게 satellite vault를 인덱싱한다.

**가능한 것**:

```
✅ qmd로 LLM Wiki 검색 (자동 — cwd 무관)
   mcp__qmd__query(searches=[{type:"vec", query:"..."}])

✅ Grep/Read에 명시 path
   Grep(pattern="...", path="/Users/yohankoo/Local Obsidian_MBP/CMDS_LLM_Wiki")
   Read(file_path="/Users/yohankoo/Local Obsidian_MBP/CMDS_LLM_Wiki/20. Wiki/...")
```

**불가능한 것**:

```
❌ /query 스킬 — index.md를 cwd 기준으로 읽으므로 LLM Wiki 안에서만 동작
❌ cwd만 믿는 기본 Grep — path 명시 안 하면 메인 볼트만 스캔
❌ [[LLM Wiki 페이지]] 직접 wikilink — 볼트 경계 넘지 못함
```

**메커니즘**:
- qmd config: `~/.config/qmd/index.yml` — absolute path로 `CMDS_LLM_Wiki/20. Wiki` 등 하드코딩
- qmd MCP: `~/.claude.json` user-scope 등록 (모든 Claude Code 세션에서 사용 가능)
- qmd 인덱스 DB: `~/.cache/qmd/index.sqlite` (cwd 독립)

**기본 동작 (Default Trigger)**: 사용자 질문/작성 주제가 아래 카테고리에 닿으면 **답변 전에 `mcp__qmd__query` 를 먼저 한 번 돌린다** — 사용자가 명시적으로 "wiki 검색해줘"라고 안 해도 default behavior. LLM Wiki는 컴파일된 cross-reference 와 관련 개념 묶음을 이미 보유하고 있어서, Grep 만으로는 구조적 연결을 놓친다.

**qmd 트리거 카테고리**:
- LLM/AI 아키텍처 개념 (RAG, Compiled Wiki, Context Engineering, Persistent Knowledge Base 등)
- 멀티에이전트 패턴 (Orchestrator-Subagent, Agent Teams, Shared State, Message Bus, Generator-Verifier)
- Karpathy / kepano / Anthropic 등 wiki 에 등록된 entity 가 등장하는 토픽
- Knowledge Management 이론 (Memex, Zettelkasten 의 LLM 시대 변용, Ingest-Query-Lint Cycle 등)
- "내가 LLM Wiki 에 정리해뒀던 X" 같은 사용자의 self-reference

**도구 선택 규칙**:

| 상황 | 도구 | 이유 |
|------|------|------|
| 정확한 파일명/제목 안다 | `Grep` + path 명시 | 빠르고 결정적 |
| 추상 쿼리 / 의미 검색 / 관련 개념 묶음 | `mcp__qmd__query` (vec/hyde) | cross-reference 자동 surfacing |
| 키워드는 명확하지만 어디 있는지 모름 | qmd `lex` 먼저, fallback 으로 Grep | 키워드 매칭 + 의미 보강 |
| 답변 풍부하게 / 관점 다층화 | qmd `vec` 또는 `hyde` (intent 명시) | "사용자가 묻지 않았지만 관련 있는 것" 발굴 |

**Anti-pattern (이번 세션의 실수)**: 정확한 제목(`RAG vs Compiled Wiki`)을 알아서 Grep + Read 로 직행했더니, 같은 주제에 묶여있던 `Shared State Pattern`, `Choosing Multi-Agent Patterns` 페이지를 놓침 → 팀 멀티 저자 시나리오에서 결정적인 통찰 누락. 정확한 페이지를 안다고 해서 qmd 를 건너뛰면 안 됨 — **확장 검색 (관련 개념 1-hop) 의 비용이 매우 낮다**.

**인용 표기**: 본문에서는 `→ LLM Wiki: {page name}` 텍스트 참조로 크로스-볼트 링크를 표시한다 (Obsidian wikilink 는 볼트 경계 못 넘음).

---

## CMDS Process Command Suite (2026-04-14+)

The mothership has 8 slash commands aligned with the **CMDS Process** (Connect → Merge → Develop → Share). They live in `90. Settings/94. Agent Settings/claude/commands/` (symlinked from `.claude/commands/`).

### Command Map

| Command | Type | Role | Key dialogs |
|---------|------|------|-------------|
| `/inbox` | Router | Scan 9 inbox subfolders, AskUserQuestion to route to a stage command | scope + stage |
| `/connect` | Stage | Triage inbox → 100 Themes (interest/topic/variable/term). **Auto-classifies, auto-dedupes, auto-stubs.** | only at ambiguity |
| `/merge` | Stage | N inbox/Theme notes → 1 synthesized 200 Literature note. **Heaviest command, most dialogs.** | purpose, candidates, angle, draft review |
| `/develop` | Stage | Apply method/build artifact → 300-600 (code, prompts, specialty, curriculum). | artifact type, review |
| `/share` | Stage / Orchestrator | Auto-delegate to existing skills (`thebetter-writer`, `markdown-slides`, `tone-writer`, etc.) → 700-800 | format, tone (when needed) |
| `/lint` | Cross-cutting | Health check by stage scope (inbox/connect/merge/develop/share/all). **Read-only**, surfaces issues. | only if user asks for fix |
| `/query` | Cross-cutting | Search vault + LLM Wiki, synthesize answer, optionally file back into appropriate CMDS category (NOT a separate /queries folder). | wiki-worthy + classify |
| `/status` | Cross-cutting | One-screen vault stage snapshot + recommended next action. **Zero dialogs**, fast. | none |

### Decision Tree (When to Use Which)

```
세션 시작 / 뭐 할지 모름
  └─→ /status  (한 화면 요약 + 추천 액션)

방대한 inbox에서 시작
  └─→ /inbox  → AskUserQuestion으로 라우팅

inbox 항목 빠르게 분류·등록
  └─→ /connect  (low-friction, Theme stub)

여러 노트 합성해서 한 노트로 만들고 싶음 (사용자의 핵심 워크플로)
  └─→ /merge  (multi-dialog, Literature 산출)

방법론을 데이터/도구에 적용 / 코드·프롬프트 생성
  └─→ /develop  (artifact-producing)

기존 합성을 외부용 산출물로 (뉴스레터/슬라이드/SNS 등)
  └─→ /share  (skill 오케스트레이션)

볼트에 질문하기 (자신의 글 + LLM Wiki 동시 검색)
  └─→ /query  (답변 + 가치 있으면 해당 CMDS 카테고리에 file back)

위생 점검 (모순/orphan/stale)
  └─→ /lint {scope}  (read-only)
```

### Settled Design Decisions (record of intent)

- **Vocabulary**: stage commands use the user's own framework (CMDS Process) instead of LLM Wiki's `ingest/query/lint` triad. The LLM Wiki vocabulary stays satellite-side; mothership uses Connect/Merge/Develop/Share.
- **Inbox is router-only**: `/inbox` never writes; it only scans, summarizes, and uses `AskUserQuestion` to route. This matches the user's mental model of inbox as triage zone.
- **`/share` as orchestrator, not writer**: auto-delegates to existing skills (`thebetter-writer`, `markdown-slides`, `tone-writer`, `pptx-cmds`, `series-writer`, `social-media-content-adapter`, `course-designer`, `markdown-video`, `business-docs`, etc.). Never produces content directly. Routing map maintained in `share.md`.
- **`/query` results are NOT folder-isolated**: per user policy "내 모든 노트가 쿼리의 소재이고 결과이기 때문에 구분하지 않고 — CMDS 지식분류 체계에 따라 분류". Query results that survive the wiki-worthiness gate get classified into the appropriate CMDS category (220 Personal Insights, 210 Literature Reviews, 5XX Product, etc.) and saved to the correct physical folder (mostly `30. Permanent Notes/`).
- **Automation density per command**: `/connect` auto-pilots with minimal user input; `/merge` deliberately preserves multi-dialog because synthesis involves information loss; `/develop` and `/share` ask only at the type/format decision; `/lint` and `/status` are zero-dialog.
- **`AskUserQuestion` everywhere it's used**: stage commands use the MCP tool with multiSelect where applicable, max 4 options per question. Always include a "(Recommended)" first option based on context.
- **CMDS categorization is metadata, not folders**: there is no `100/`, `200/`, etc. physical folder. Notes live in the existing folder structure (`30. Permanent Notes/`, `60. Collections/`, etc.) and are categorized via `CMDS:` and `index:` frontmatter.
- **All commands honor pre-flight rules**: `frontmatter-standard.md`, `wikilink-rules.md`, `indentation-rules.md`, `file-creation-rules.md`. New v2 fields introduced: `mergePurpose`, `sourceNotes`, `mainVaultRelated`, `developSources`, `shareSourceNotes`, `shareFormat`, `sharePurpose`, `queryOrigin`, `querySources`.

### Typical Session Patterns

**Daily**: `/status` → `/inbox` → (`/connect` 또는 `/merge`) → 종료
**Weekly**: `/lint inbox` → 정리 후 `/merge {topic}` → `/share` (필요 시)
**프로젝트 작업**: `/query {topic}` → `/merge {topic}` → `/develop` 또는 `/share`
**시스템 점검 (월 1회)**: `/lint all` → `/refresh-context` (TBD)

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
	- Simpler, more portable structure

- **Use CMDS.md**: For understanding context and purpose
	- Why this system exists
	- User's professional background and workflow
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
Most common types in the vault:
- `note` - General notes (459+)
- `terminology` - Term definitions (130+)
- `research-pipeline` - Research pipeline documents (124+)
- `meeting` - Meeting notes (160+)
- `people` - People profiles (93+)
- `curriculum` - Course curriculum (82+)
- `channel` - YouTube/Blog/Newsletter 채널 프로필 (101+)
- `CMDS` - CMDS index pages (replaces traditional MOC concept)
- `api` - API documentation (97+)
- `moc` - Map of Content (85+)
- `manuscript` - Manuscripts and drafts (66+)

## Obsidian-Specific Guidelines

### Markdown Files
- Always use wikilinks `[[]]` for internal references, NOT markdown links
- Include YAML frontmatter for metadata (see @.claude/rules/frontmatter-standard.md)
- Standard frontmatter fields:
	- `type:` - Note type/category (see types above)
	- `aliases:` - Alternative names (array format)
	- `author:` - Author information (array format with quoted wikilinks)
	- `date created:` - Creation timestamp (YYYY-MM-DD format)
	- `date modified:` - Last modification (YYYY-MM-DD format)
	- `tags:` - Relevant tags (array format)
	- `CMDS:` - CMDS category reference (quoted wikilink if used)
	- `index:` - Index reference (quoted wikilink if used)
	- `status:` - unread/reading/inProgress/completed/archived

### Note Templates
Templates are located in `90. Settings/91. Templates/`
Key templates include:
- `Template_00. Basic Note.md` - Basic note structure
- `Template_01. Daily Note.md` - Daily journal
- `Template_05. Meeting Minutes.md` - Meeting notes
- `Template_20. Research Note.md` - Research documentation
- `Template_51. People.md` - People profiles
- `Template_80. AI Summary.md` - AI-generated summaries
- `Template_90. CMDS MOC.md` - Map of Content

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
- ChatGPT custom GPTs linked in CMDS Head Quarter
- Claude integration via Claude Code directory
- Agent settings: `90. Settings/94. Agent Settings/claude/` 이 **원본** (Obsidian Sync 대상). `.claude/{agents,commands,rules,skills}` 는 이 원본으로 향하는 **심볼릭 링크**. `.claude/settings.json`, `.claude/sessions/` 등은 머신 로컬 전용 (symlink 안 함). 새 MBP 에서 재설정 방법은 `.claude/rules/directory-structure.md` 참조.

### Automation
- n8n workflows for automation
- Obsidian Webhook integration
- Various API integrations (OpenAI, Anthropic, Google)

## Obsidian CLI (v1.12+)

> **📖 Full Reference**: [[Obsidian CLI]] | **📘 실전 가이드**: [[Obsidian CLI 사용 가이드 (CMDS)]]

Obsidian CLI는 터미널에서 Obsidian을 직접 제어하는 명령줄 인터페이스입니다.
**Claude Code에서 `obsidian` 명령을 Bash 도구로 호출하여 Obsidian 네이티브 기능을 활용할 수 있습니다.**

### 요구사항
- Obsidian 1.12+ (Early Access, Catalyst 필요)
- Settings → General → CLI 활성화
- Obsidian 앱 실행 중이어야 함

### Claude Code에서 사용 시 주의사항
- `obsidian` 명령은 Bash 도구로 호출
- 볼트 타겟팅: `obsidian vault=CMDSPACE_Local_MBP <command>`
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

# --- 플러그인 ---
obsidian plugins filter=community versions          # 커뮤니티 플러그인 목록
obsidian plugin:reload id=<plugin-id>               # 플러그인 리로드

# --- 개발자 ---
obsidian eval code="<javascript>"                   # JS 실행 (app.vault 등 접근)
obsidian dev:screenshot path=<filename>             # 스크린샷
obsidian dev:console level=error                    # 콘솔 에러 확인
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
author:
  - "[[구요한]]"
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

<!-- DYNAMIC: 아래 내용은 주기적으로 갱신됩니다. 검증이 필요할 수 있습니다. -->

## Critical Workflow Rules

1. **Code Output Location**: ALL code MUST go to `00. Inbox/03. AI Agent/{environment subfolder}/`
2. **Required Properties**: Every note needs 7 fields: type, aliases, **description** (English, LLM hint), author, date created, date modified, tags
3. **Properties v2.0 Standards**:
	- Dates: ISO 8601 (YYYY-MM-DD)
	- Author: `[[구요한]]` wikilink format
	- Status: Use standard 5 values only
	- CamelCase: myRate, totalPage (⚠️ `rating` 사용 금지 → 반드시 `myRate`)
	- **description**: English only, 1-2 sentences, skill-description style (what + when to reference)
4. **CMDS Hierarchy**: 🏛 (top) → 📖 (100-900) → 📚 (N01-N99) → no icon (details)
5. **Vault Scale**: 10,000+ notes with established patterns - respect existing conventions

## Key Obsidian Plugins

The vault uses 120+ plugins. Most important ones:
- **Dataview**: Dynamic queries and data aggregation
- **Copilot**: AI-powered writing assistance
- **Smart Connections**: AI-based note linking
- **Excalidraw/Excalibrain**: Visual thinking and diagramming
- **Chronology**: Timeline visualization
- **Calendar**: Date-based note organization
