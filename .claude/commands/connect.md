---
description: Capture & triage inbox items into 100 Themes (interest/topic/variable/terminology). Auto-classifies via LLM inference, auto-dedupes via qmd, auto-creates lightweight stub notes. Low-friction — only asks the user at decision points.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, mcp__qmd__query
---

# /connect — CMDS Connect Stage (Capture & Triage to 100 Themes)

Convert raw inbox items into structured Theme entries (`📖 100 Themes`). This is the **Connect** stage of the CMDS Process — fast capture, low ceremony.

> **🧭 Prerequisite**: Read `CMDS.md` once per session for category context. Output goes to `30. Permanent Notes/` with:
> - `CMDS: "[[📚 10N {Subcategory}]]"` — the specific 📚 subcategory (101/102/103/104), NOT the 📖 top-level
> - `index: "[[🏷 Research Notes]]"` — a 🏷 Index note under `90. Settings/96. Index/`
>
> Per 🏛 CMDS Guide: `CMDS:` = 📚 subcategory · `index:` = 🏷 Index note. (CMDS uses metadata-based categorization, not physical 100/200 folders.)

## Input

`$ARGUMENTS`

- A **subfolder name** (e.g. `02. Clippings`, `06. GenAI Chats`, `Root`)
- A **specific filename** to triage one item
- **Blank**: invoke `/inbox` first to determine scope

## Theme Type Routing

| Theme type | When | Frontmatter `CMDS:` | Typical output filename |
|------------|------|---------------------|------------------------|
| **interest** | 호기심·관심사 (개인적 끌림) | `"[[📚 101 Interests]]"` | `🔖 {topic}.md` |
| **topic** | 탐구 대상 (연구·집필 가능성) | `"[[📚 102 Topics]]"` | `{topic}.md` |
| **variable** | 측정·조작화 가능한 개념 | `"[[📚 103 Variables]]"` | `{variable name}.md` |
| **terminology** | 용어·정의 | `"[[📚 104 Terminologies]]"` | `{term}.md` |

All four Theme types share the same `index:` default: `"[[🏷 Research Notes]]"` (matches existing topic-note convention in the vault, e.g., `내재역량.md`). Use a more specific 🏷 (e.g., `🏷 Web Clips`, `🏷 References`) only if the content is clearly that kind of artifact.

## Process (auto-pilot with minimal user intervention)

### Step 1: Load Candidates

Glob the input scope. For each `.md` file:
- Read frontmatter + first 50 lines (no full content yet — token economy)
- Extract: title, gist (1~2 sentences), candidate keywords (3~5)

If candidates > 20, ask **once**:

```
AskUserQuestion (single):
  Q: "{N}개 후보가 있습니다. 어떻게 처리할까요?"
  Header: "Batch size"
  Options:
    - "전부 (자동 분류 후 결과만 보여드림)" — Recommended
    - "10개씩 배치로"
    - "사용자가 직접 선택"
```

### Step 2: Auto-Classify Each Candidate

For each candidate, **LLM-infer** the Theme type using these heuristics:

- Single concept term (예: "ZettelKasten", "Synaptic Plasticity") → **terminology**
- Measurable/operationalizable construct (예: "지식 연결성", "인지 부하") → **variable**
- Subject worth exploring with multiple sub-questions → **topic**
- Personal pull / ongoing fascination → **interest**

If classification confidence is **low (uncertain between 2+ types)** → flag for user review (Step 4 batch question).

### Step 3: Auto-Dedupe via qmd

For each candidate, run:

```
mcp__qmd__query(
  searches=[
    {type: "vec", query: "<candidate gist>"},
    {type: "lex", query: "<candidate title>"},
  ],
  intent="Check if a Theme note already exists in the mothership for this candidate",
  collections=["wiki"]  // qmd may not be configured for mothership; fall back to Grep
)
```

Fallback if qmd lacks mothership index:

```
Grep(
  pattern="<key term>",
  path="30. Permanent Notes",
  glob="*.md",
  output_mode="files_with_matches",
  head_limit=10
)
```

For each candidate, classify into:

- **NEW** — no existing match. Auto-create a stub.
- **UPDATE** — strong existing match (>0.7 vec score or exact title hit). Append to existing.
- **AMBIGUOUS** — partial overlap. Defer to Step 4.

### Step 4: User Decision Batch (only for AMBIGUOUS + low-confidence classifications)

Build a single AskUserQuestion call covering all flagged candidates (max 4 questions per call):

```
AskUserQuestion (single, multiSelect: false):
  For each ambiguous candidate (up to 4):
    Q: "{title} → 어떻게 처리할까요?"
    Header: "Decide"
    Options:
      - "신규 Theme 생성 ({inferred type})" — Recommended
      - "기존 [[{best match}]] 업데이트"
      - "스킵 (이번 배치에서 제외)"
      - "타입 변경" (자유 텍스트로 받아 처리)
```

If more than 4 ambiguous, process the first 4 and report the rest at the end ("나머지 {N}개는 후속 배치로 진행").

### Step 5: Auto-Create Stubs (for NEW)

For each NEW candidate, create a stub note in `30. Permanent Notes/` with:

```yaml
---
type: note
aliases:
  - {short alias if applicable}
description: {1-2 sentence English summary — what the theme is + when to reference}
author:
  - "[[Me]]"
date created: {today YYYY-MM-DD}
date modified: {today YYYY-MM-DD}
tags:
  - theme
  - {topic tag from candidate}
CMDS: "[[📚 10{N} {Subcategory Name}]]"  # 101/102/103/104 per Theme type — CMDS points to 📚 subcategory
index: "[[🏷 Research Notes]]"               # default 🏷 index for Theme stubs
status: unread
sourceInbox:
  - "[[{original inbox file}]]"
---

# {Theme title}

> **Captured from**: [[{inbox file}]] on {today}

## Gist

{1-2 sentence summary in user's voice}

## Why this matters

(✏️ TODO — 사용자가 채울 부분. 왜 이게 의미 있는지 한 줄.)

## Related captures

- (auto-populated as more inbox items connect to this theme)

## Open questions

- {Optional — if the auto-extraction surfaced any}
```

**Pre-flight checklist** (per file-creation-rules.md, indentation-rules.md, frontmatter-standard.md):

- [ ] YAML uses 2 SPACES, body uses TAB
- [ ] Wikilinks in YAML are quoted: `"[[...]]"`
- [ ] All 7 required properties present (type, aliases, description, author, date created/modified, tags)
- [ ] `description` is in English, 1-2 sentences
- [ ] `CMDS:` points to 📚 subcategory (101/102/103/104) — NOT 📖 top-level
- [ ] `index:` points to a 🏷 Index note (default `[[🏷 Research Notes]]`) — NOT a 📚
- [ ] Filename follows existing conventions (emoji prefix per file-prefix rules if applicable)

### Step 6: Auto-Update for UPDATE candidates

Append to existing Theme note:

```markdown
## Related captures

- [[{new inbox file}]] — captured {today}: {1-line gist}
```

Update `date modified`. Add new tags if any. Do not overwrite existing description/why-this-matters.

### Step 7: Back-link Inbox Sources

For each processed inbox file, append **at the bottom** (do not modify existing content):

```markdown
---

> 🔗 **Connected as Theme**: [[{theme note name}]] on {today} via /connect
```

This preserves the inbox file as evidence and creates traceability.

### Step 8: Report

Output a summary:

```
✅ /connect — Summary
────────────────────────────────────
Scope:        {input scope}
Candidates:   {N total}

📥 Created (NEW):     {n}
  - [[Theme A]] (interest)
  - [[Theme B]] (topic)
  ...

🔄 Updated (existing): {n}
  - [[Existing Theme]] ← [[inbox file]]

⏭ Skipped:            {n}
  - {file} — reason

⚠ Deferred (>4 ambiguous): {n} — run /connect again with same scope to continue

Next suggestion:
  - 충분히 무르익은 Theme이 있다면 → /merge {theme} 으로 합성
  - Theme 정리 후 인박스 검사 → /lint inbox
```

## Anti-patterns

- ❌ Don't ask the user a question per candidate — batch ambiguous ones (max 4) into one AskUserQuestion call.
- ❌ Don't create a Theme for content that's already mature (full essays, research notes) — those go to `/merge` directly.
- ❌ Don't move/delete inbox files in this command — only append back-link. Cleanup is a separate explicit step.
- ❌ Don't skip the dedupe check — duplicate Themes are the #1 inbox-bloat failure mode.
- ❌ Don't overwrite the user's existing "Why this matters" prose.

## Notes

- Connect is **shallow & fast**. Synthesis happens in `/merge`. If you find yourself wanting to write a 500-word note, that's a `/merge` signal, not `/connect`.
- A Theme note can have 0 substantive content beyond gist — that's fine. It's a placeholder + gathering point.
- Themes ripen over time (more `Related captures` accumulate) → eventually trigger `/merge` to synthesize them into Literature.
