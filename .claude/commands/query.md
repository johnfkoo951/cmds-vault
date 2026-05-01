---
description: Search the mothership (and optionally LLM Wiki satellite) for an answer using qmd. Synthesize the answer in conversation. If the answer is wiki-worthy, propose to file it back into the appropriate CMDS category (NOT a separate /queries folder — every note can be both source and result).
allowed-tools: Read, Glob, Grep, AskUserQuestion, mcp__qmd__query, mcp__qmd__get
---

# /query — CMDS Vault Query (search + synthesize + optional file-back)

Ask the vault a question. Get an answer synthesized from existing notes. If the answer is substantive enough to be a new note, **classify it into the right CMDS category and propose to save it there** — NOT into a separate "queries" folder.

> **🧭 Prerequisite**: `CMDS.md` for category context. The principle (per user, 2026-04-14): "내 모든 노트가 쿼리의 소재이고 결과이기 때문에 구분하지 않고. cmds 지식분류 체계에 따라서 분류하고 각 용도에 맞는 폴더로 이동하는 게 좋을듯."

## Input

`$ARGUMENTS`

- A natural-language question (Korean OK, English OK)
- A keyword + intent ("RAG 컴파일드 위키 비교 — 팀 적용 관점")
- **Blank**: ask via AskUserQuestion

## Process

### Step 1: Determine Search Scope (Auto)

Decide which collections to query based on the question:

| Question type | Collections | Reason |
|---------------|------------|--------|
| Mothership-only (자신의 글, 회의록, 강의 등) | mothership notes via Grep + qmd if mothership-indexed | personal context |
| LLM Wiki concepts (LLM, RAG, agents 등) | qmd `wiki` collection | per existing memory rule |
| Mixed (자신의 적용 + 이론적 배경) | both | union |

If unclear, default to both.

### Step 2: Run Search

```
mcp__qmd__query(
  searches=[
    {type: "vec", query: "<rephrased as natural-language question>"},
    {type: "lex", query: "<exact keywords>"},
    (optional) {type: "hyde", query: "<50-word hypothetical answer>"}
  ],
  intent="<one-line: what user really wants>",
  collections=[appropriate scope],
  limit=10
)
```

For mothership: also Grep for keyword hits in `30. Permanent Notes/`, `60. Collections/`, `70. Outputs/` — qmd may not index these depending on configuration.

### Step 3: Read Top Results

Read top 5~8 results in full. Extract:
- Direct answers / claims
- Conflicting positions (if any)
- Adjacent concepts that enrich the answer

### Step 4: Synthesize Answer

Compose the answer in the conversation (NOT yet a file). Structure:

```
🔎 Query: {original question}
─────────────────────────────────────

## Direct answer

{2~4 sentence essence}

## Supporting evidence

- [[Source A]] — {what it contributes}
- [[Source B]] — {what it contributes}
- → LLM Wiki: {satellite page} — {what it contributes}

## Caveats / Open questions

- {if any contradictions, gaps, or staleness flagged}

## What I didn't find

{what would have helped but isn't in the vault — useful for next /connect or /merge target}
```

### Step 5: Wiki-worthiness Decision (Dialog)

After delivering the answer, judge if it's **substantive enough to file back as a new note**:

- ✅ Wiki-worthy if: synthesized 3+ sources, surfaces a non-obvious connection, answers a question likely to recur
- ❌ Skip if: answer was directly retrievable from one note, fact lookup, casual question

If wiki-worthy, ask:

```
AskUserQuestion (single):
  Q: "이 답변이 새로운 노트로 가치 있어 보입니다. 저장할까요?"
  Header: "File back?"
  Options:
    - "저장 — 자동 분류 (Recommended)" — CMDS 카테고리 자동 추천 후 저장
    - "저장 — 수동 분류" — 사용자가 카테고리/위치 지정
    - "저장 안 함" — 답변만 받고 끝
```

### Step 6: Auto-Classify (if user chose auto file-back)

Determine the best CMDS category based on answer content:

| Answer character | Suggested category | Physical destination |
|------------------|-------------------|---------------------|
| Original interpretation / personal take | `[[📚 220 Personal Insights]]` | `30. Permanent Notes/` |
| Cross-source synthesis on a topic | `[[📚 210 Literature Reviews]]` | `30. Permanent Notes/` |
| New concept definition | `[[📚 201 Concepts]]` or `[[📚 104 Terminologies]]` | `30. Permanent Notes/` |
| Tool how-to insight | `[[📚 5XX Product]]` | `30. Permanent Notes/` or `40. Docs/46. My Docs/` |
| Domain expertise update | `[[📚 6XX Specialties]]` | `30. Permanent Notes/` |
| Prompt pattern discovered | `[[📚 492 Prompts]]` | `50. Assets/51. Prompt/` |

Show the proposed classification briefly:

```
📂 제안 분류:
  CMDS:        [[📚 220 Personal Insights]]
  Path:        30. Permanent Notes/{title}.md
  Title:       {auto-generated}
```

If user objects ("Other" or text feedback), accept manual override.

### Step 7: Save

Write the synthesized answer as a new note with frontmatter:

```yaml
---
type: note
aliases: []
description: {English 1-2 sentences — what this note answers + when to reference}
author:
  - "[[Me]]"
date created: {today}
date modified: {today}
tags:
  - {topic tags}
  - query-result
CMDS: "[[📚 {NNN Subcategory}]]"        # specific 📚 subcategory (e.g., 210/220/201/492/6XX)
index: "[[🏷 {Index Note}]]"            # 🏷 Index note (default [[🏷 Research Notes]]; [[🏷 Prompts]] for 492)
status: completed
queryOrigin: "{original question verbatim}"
querySources:
  - "[[Source A]]"
  - "[[Source B]]"
related:
  - "[[Related note 1]]"
mainVaultRelated:
  - "→ LLM Wiki: {satellite page}"
---
```

### Step 8: Back-link Sources

For each `querySources`, append:

```markdown
---

> 🔎 **Cited in query**: [[{new note}]] on {today} ("{question}")
```

### Step 9: Report

```
✅ /query — Done
─────────────────────────────────
Q:           {original question}
Sources:     {N} notes consulted (mothership: M, LLM Wiki: L)
Action:      {Answer only | Saved to [[{path}]] | Saved + back-linked}

Next suggestion:
  - "What I didn't find" 항목을 채우려면 → /connect 으로 새 자료 캡처
  - 답변을 콘텐츠로 → /share {topic}
```

## Anti-patterns

- ❌ **Creating a `30. Queries/` or similar dedicated folder** — explicitly against user policy. Every query result classifies into existing CMDS structure.
- ❌ **Saving every answer** — fact lookups and casual questions don't deserve a note. Apply Wiki-worthiness judgment.
- ❌ **Skipping LLM Wiki when topic warrants it** — per memory rule, LLM/agent/KM topics should hit qmd `wiki` collection by default.
- ❌ **Fake citations** — only list `querySources` for notes actually read in Step 3.

## Notes

- The user's principle is essential: **vault is the substrate**, not a query log. Notes that emerge from `/query` are first-class — they live wherever they best belong by topic, not by origin.
- For repeated questions on the same topic, the saved answer becomes a source for next time → query results compound.
- If `/query` consistently surfaces the same gaps (`What I didn't find`), that's a signal to run `/connect` on related external sources.
