---
description: Apply methods to data, build artifacts (code/prompts/curriculum/specialty deepening). Auto-detects input type and proposes appropriate output. Outputs first to 00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/ per file-creation-rules.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, mcp__qmd__query, Skill
---

# /develop — CMDS Develop Stage (Apply Methods, Build Artifacts)

Take methodologies (`📖 400`), data (`📖 300`), and accumulated expertise (`📖 600`) and produce **executable or reusable artifacts**: code, prompts, curriculum modules, tool docs, deepened specialty notes.

> **🧭 Prerequisite**: `CMDS.md` for category context. **All code/script outputs MUST land in `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/` first** per `.claude/rules/file-creation-rules.md`. After user validation, they may be promoted to permanent locations.

## Input

`$ARGUMENTS`

- A **method + data combination** (e.g., "regression on consulting feedback survey")
- A **specialty topic** to deepen (e.g., "Knowledge Management 600")
- A **reusable artifact request** (e.g., "프롬프트 만들어줘 — 회의록 자동 분류")
- **Blank**: ask via AskUserQuestion which artifact type

## Artifact Type Routing

| Artifact | Output destination | Frontmatter `CMDS:` | Suggested `index:` |
|----------|-------------------|----------------------|--------------------|
| **Code/Script (analysis)** | `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/YYYY-MM-DD-{name}.{ext}` | `"[[📚 491 Codes]]"` | `"[[🏷 Syntax and Codes]]"` |
| **Reusable Prompt** | Same inbox path → after review, move to `50. Assets/51. Prompt/` | `"[[📚 492 Prompts]]"` | `"[[🏷 Prompts]]"` |
| **Specialty Deepening** | `30. Permanent Notes/{title}.md` (update/create) | `"[[📚 6XX]]"` (per topic) | `"[[🏷 Research Notes]]"` |
| **Tool Doc / How-to** | `40. Docs/46. My Docs/` | `"[[📚 5XX Product]]"` | `"[[🏷 Guideline]]"` |
| **Curriculum Module** | `70. Outputs/73. Courses/` | `"[[📚 841 Curriculum]]"` | `"[[🏷 Lecture Notes]]"` |
| **Automation Script** | `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/{project-folder}/` | `"[[📚 493 Scripts]]"` | `"[[🏷 Syntax and Codes]]"` |

Per 🏛 CMDS Guide: `CMDS:` = 📚 specific subcategory · `index:` = 🏷 Index note.

## Process

### Step 1: Detect Artifact Type (Auto + Confirm)

LLM-infer artifact type from `$ARGUMENTS`. Confidence rules:

- Mentions data + method (regression, t-test, ML model) → **Code/Script (analysis)**
- Mentions "프롬프트", "GPT", "AI 명령" → **Reusable Prompt**
- Mentions "정리", "딥다이브", specialty topic name → **Specialty Deepening**
- Mentions tool name (Obsidian, ChatGPT, Claude, etc.) + how-to → **Tool Doc**
- Mentions "강의", "수업", "모듈" → **Curriculum Module**
- Mentions "자동화", "스크립트", "n8n" → **Automation Script**

If high confidence, skip dialog. Otherwise:

```
AskUserQuestion (single):
  Q: "어떤 종류의 산출물을 만들까요?"
  Header: "Artifact"
  Options:
    - "{Auto-detected} (Recommended)" — {one-line reason}
    - "Code / 분석 스크립트"
    - "재사용 프롬프트"
    - "Specialty 노트 보강"
    (max 4 — show top 3 options + Other)
```

### Step 2: Gather Inputs

Based on artifact type, search for the necessary inputs:

**Code/Script**:
- Search 400 method notes for the technique
- Search 300 data notes for the dataset reference
- If both not found, ask user to provide

**Reusable Prompt**:
- Search 220 Personal Insights + 600 Specialty for the underlying pattern being prompted
- Use `mcp__qmd__query` for similar existing prompts in `50. Assets/51. Prompt/`

**Specialty Deepening**:
- Find the existing 600 specialty note (qmd vec or Grep)
- Find new 200 Literature notes that should feed into it (recent merges)

**Tool Doc**:
- Find the 500 Product hub note
- Find user's actual usage notes for that tool

**Curriculum Module**:
- Find existing 841 Curriculum hub
- Find 200/600 source materials for the module topic

### Step 3: Build the Artifact

**For Code/Script**: Generate the file with executable code, inline comments only where invariant is non-obvious, and a **header docstring** explaining purpose + how to run. Follow language-appropriate conventions.

**For Reusable Prompt**: Build a prompt with:
- Clear role assignment
- Input schema
- Output schema
- 1~2 examples (few-shot)
- Failure mode notes ("Don't do X")

**For Specialty Deepening**: Update existing note OR create new sub-note. Add new sources to `related:`, add new sections under existing structure.

**For Tool Doc**: Step-by-step how-to. Screenshots placeholders if needed. Frontmatter links to `📚 5XX Product` hub.

**For Curriculum Module**: Module outline with: learning objectives, prerequisites, content sections, exercises, assessment.

**For Automation Script**: For multi-file projects, follow the multi-file project folder rule (create intermediate folder `YYYY-MM-DD-project-name/`).

### Step 4: Frontmatter (for note-based artifacts)

```yaml
---
type: {note | curriculum | api | etc.}
aliases: []
description: {English 1-2 sentences}
author:
  - "[[Me]]"
date created: {today}
date modified: {today}
tags:
  - {topic tags}
  - {artifact-type tag: code | prompt | curriculum | tool-doc}
CMDS: "[[📚 {NNN Subcategory}]]"       # specific 📚 subcategory (e.g., 491/492/630/841)
index: "[[🏷 {Index Note}]]"           # 🏷 Index note per artifact (see table above)
status: inProgress  # promote to completed after testing
developSources:
  - "[[Method note]]"
  - "[[Data note]]"
  - "[[Specialty note]]"
---
```

For Code/Script (non-md), put metadata in a header comment block instead.

### Step 5: User Review (Dialog)

Show the artifact's path + a preview (first 30 lines or full if short). Ask:

```
AskUserQuestion (single):
  Q: "산출물 어떠세요?"
  Header: "Review"
  Options:
    - "이대로 진행 (Recommended)" — 검증 후 정식 위치로 이동
    - "수정 후 진행" — 자유 텍스트 피드백
    - "다른 형태로 다시" — 예: 코드 → 노트로
    - "취소"
```

### Step 6: Promotion (for ready artifacts)

If user confirms and artifact is ready (e.g., code tested, prompt validated):

- Code/Script → optionally promote from inbox to relevant final location (e.g., a Permanent Notes companion `🔖 코드 설명.md` linking to the script)
- Reusable Prompt → move from inbox to `50. Assets/51. Prompt/{name}.md`
- Specialty Deepening, Tool Doc, Curriculum Module → these are already at their destination

If artifact needs more iteration (e.g., user said "테스트 후 결정"), leave in inbox and report the status.

### Step 7: Connect

- Add wikilinks back to source method/data/specialty notes (in their `related:` if appropriate, or just in the new artifact's `developSources:`)
- For prompts, register in the prompts index/MOC if one exists

### Step 8: Report

```
🛠 /develop — Artifact built
─────────────────────────────────────
Type:        {artifact type}
Path:        {final or inbox path}
Sources:     {list}
Status:      {inProgress | ready-to-promote | promoted}

Validation needed:
  - {if code: how to run}
  - {if prompt: where to test}
  - {if curriculum: what to review}

Next suggestion:
  - 결과를 강의/세미나/콘텐츠로 → /share
  - 결과 검증 후 메모리/룰로 → /reflect (TBD)
```

## Anti-patterns

- ❌ Writing code directly to `30. Permanent Notes/` or other CMDS categories — must go through `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/` first.
- ❌ Skipping the artifact-type dialog when confidence is mixed — wrong type means wrong output destination.
- ❌ Bundling unrelated artifacts in one /develop call — split into multiple calls if user request mixes types.
- ❌ For multi-file code projects, scattering files in inbox root — always create a `YYYY-MM-DD-project-name/` subfolder.

## Notes

- `/develop` is **artifact-producing**, not knowledge-synthesizing. If user wants synthesis, route to `/merge` first.
- Generated code is provisional until user validates. The status `inProgress` reflects this.
- Reusable prompts are the most compounding output — each successful prompt becomes a tool for future sessions. Prioritize quality + few-shot examples.
- Tool docs are highest ROI when written immediately after a tool aha moment — capture the discovery while it's fresh.
