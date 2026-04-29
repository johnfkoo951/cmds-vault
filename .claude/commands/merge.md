---
description: Synthesize multiple inbox/Theme notes into ONE integrated 200 Literature note (Concept, Framework, Literature Review, or Personal Insight). N→1 fan-in workflow with multi-dialog checkpoints — purpose gate, candidate confirmation, angle selection, draft review.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, mcp__qmd__query, mcp__qmd__get
---

# /merge — CMDS Merge Stage (Synthesize → 200 Literature)

Take N candidate notes (from inbox, 100 Themes, daily notes, GenAI chats) and weave them into **one** integrated note in `📖 200 Literature`. This is the heaviest CMDS Process command — multiple user checkpoints because synthesis involves information loss.

> **🧭 Prerequisite**: `CMDS.md` for category context. Output destination: `30. Permanent Notes/` (physical home for evergreen Literature notes). Frontmatter per 🏛 CMDS Guide:
> - `CMDS: "[[📚 2NN {Subcategory}]]"` — specific 📚 subcategory (201/202/210/220/240…), NOT the 📖 top-level
> - `index: "[[🏷 {Index Note}]]"` — a 🏷 Index note (e.g., `🏷 Research Notes` for reviews/insights, `🏷 Books` for book notes, `🏷 References` for reference literature)

## Input

`$ARGUMENTS`

- A **theme name / topic / keyword** (semantic — qmd will find candidates)
- A **scope path** (e.g., `02. Clippings`, or `30. Permanent Notes` for Theme-only merge)
- A **comma-separated file list** for explicit candidate selection
- **Blank**: invoke `/inbox` first

## 200 Literature Subcategory Routing

| Output type | Frontmatter `CMDS:` | Suggested `index:` | When |
|------------|----------------------|--------------------|------|
| **Concept** | `"[[📚 201 Concepts]]"` | `"[[🏷 Research Notes]]"` | Single conceptual idea, abstract framing |
| **Framework** | `"[[📚 202 Frameworks]]"` | `"[[🏷 Research Notes]]"` | Structured model with components/relations |
| **Theory** | `"[[📚 204 Theories]]"` | `"[[🏷 Research Notes]]"` | Established or proposed theory |
| **Literature Review** | `"[[📚 210 Literature Reviews]]"` | `"[[🏷 Research Notes]]"` | Synthesis of multiple sources on a topic |
| **Personal Insight** | `"[[📚 220 Personal Insights]]"` | `"[[🏷 Research Notes]]"` | User's original interpretation/connection |
| **Book Note** | `"[[📚 240 Books]]"` | `"[[🏷 Books]]"` | Synthesized notes from book reading |

## Process

### Step 0: Purpose Gate (Gold In Gold Out) — MANDATORY

**Before doing anything else**, ask via AskUserQuestion:

```
Q1: "이 합성 노트가 어디에 쓰일 예정인가요? (재활용 축)"
Header: "Reuse axis"
multiSelect: false
Options:
  - "PhD 연구 / 학술 출판" — 821/801 카테고리 자료로
  - "강의·강연 / 컨설팅" — 840/831 자료로 (Recommended if recent activity in 840)
  - "에세이·뉴스레터" — 802 자료로 (본인 시그니처 뉴스레터 등)
  - "CMDS 시스템 / 제품" — 600/501/630 시스템 강화용
```

If user picks "Other", record verbatim. Save the answer as `mergePurpose` in the output frontmatter.

**Why this matters**: synthesis angle, depth, and tone all depend on the downstream use. Same source set → different merge for "PhD review" vs "newsletter".

### Step 1: Auto-Discover Candidates

Based on `$ARGUMENTS`:

**If keyword/topic given**: run qmd vec search across mothership + (optionally) LLM Wiki:

```
mcp__qmd__query(
  searches=[
    {type: "vec", query: "<topic + purpose keywords>"},
    {type: "lex", query: "<topic exact>"},
  ],
  intent="<one-line: what user wants to merge + purpose>",
  limit=15
)
```

Also Grep over mothership inbox folders for keyword hits:
```
Grep(pattern="<topic>", path="00. Inbox", ...)
Grep(pattern="<topic>", path="30. Permanent Notes", ...)
```

**If folder scope given**: glob all `.md` in that folder, score by recency + (optionally) keyword match.

**If file list given**: skip discovery, use list as-is.

Compile a candidate set (typically 5~15). For each: title, source folder, 1-line gist (read frontmatter `description` if present, else first 2 lines).

### Step 2: Candidate Confirmation (Dialog 1)

Show the candidate table:

```
🔍 후보 노트 ({N}개) — purpose: {mergePurpose 요약}
─────────────────────────────────────────
 #  Folder           Title                          Gist
 1  02. Clippings    {title}                        {gist}
 2  30. Permanent    {title}                        {gist}
 ...
```

Use AskUserQuestion:

```
Q: "이 후보들로 진행할까요?"
Header: "Candidates"
multiSelect: false
Options:
  - "전부 사용 (Recommended)" — 모든 후보 포함
  - "선택만 사용" — 사용자가 번호로 지정
  - "추가 후보 검색" — 키워드 보강해서 다시 탐색
  - "취소" — 합성 안 함
```

For "선택만" or "추가": follow up with free-text input.

### Step 3: Read Candidates Deeply

Once the candidate set is final, **read each file in full** (Read tool, batch in parallel). Extract per file:

- Main claims (1~3 per source)
- Concepts/entities mentioned
- Method/context (when relevant)
- Quotable lines (1~2 per source, for direct citation)
- Connections to other candidates (if any)

### Step 4: Auto-Generate Angle Proposals

Based on the candidates + `mergePurpose`, propose **2~3 synthesis angles**. Examples:

- (a) **Theoretical synthesis** — extract the underlying framework that organizes all sources
- (b) **Comparison/dialectic** — surface where sources agree/disagree
- (c) **Evolutionary** — chronicle how the idea developed across sources
- (d) **Application-driven** — focus on practical implications for `mergePurpose`
- (e) **Personal insight** — user's original interpretation as the spine, sources as evidence

Use AskUserQuestion:

```
Q: "어떤 합성 각도로 갈까요?"
Header: "Angle"
multiSelect: false
Options:
  - "{Recommended angle based on purpose} (Recommended)" — {one-line why}
  - "{Alternative 1}" — {one-line}
  - "{Alternative 2}" — {one-line}
```

If user picks Other, accept free text and use as angle.

### Step 5: Determine Output Type & Title

Based on chosen angle:

- Theoretical/framework angle → 201 Concepts or 202 Frameworks
- Comparison angle → 210 Literature Reviews
- Personal angle → 220 Personal Insights
- Theory-building → 204 Theories

Auto-propose a title (한글 OK). Use AskUserQuestion only if confidence is low:

```
Q: "출력 노트 제목과 카테고리"
Header: "Output"
multiSelect: false
Options:
  - "{Auto title} → 220 Personal Insights (Recommended)"
  - "제목 다시 짓기" — 자유 입력
  - "다른 200 카테고리로" — 자유 입력
```

### Step 6: Cross-Vault Hook (Auto, no dialog)

Search for related notes that should appear in `related:` frontmatter:

1. **Mothership related**: qmd vec or Grep on permanent notes & MOCs for the synthesis topic.
2. **LLM Wiki related**: qmd vec on `wiki` collection (satellite) — if there's a relevant Karpathy/wiki concept page.
3. **CMDS category fit**: identify best `CMDS:` value — the specific 📚 2NN subcategory (201/202/210/220/240) that matches the output type — and pick an `index:` 🏷 Index note (default `[[🏷 Research Notes]]`, or `[[🏷 Books]]` for 240).

### Step 7: Draft Synthesis

Generate the synthesized note in memory (do not write yet). Structure depends on output type:

**For Concept / Framework**:
```markdown
# {Title}

> **TL;DR**: {1-2 sentence essence}

## What it is

{Definition + scope}

## Components / Mechanisms

{Structural breakdown}

## Sources synthesized

| Source | Contribution |
|--------|--------------|
| [[A]] | ... |
| [[B]] | ... |

## Connections

- [[Mothership related note 1]] — {how related}
- → LLM Wiki: {wiki page name} — {how related} (cross-vault text reference)

## Open questions

{Unresolved tensions discovered during merge}
```

**For Literature Review**:
```markdown
# {Title} — Literature Review

## Scope

{What was reviewed, period covered, exclusions}

## Themes

### {Theme A}
{Synthesized claim} ([[Source 1]], [[Source 2]])

### {Theme B}
...

## Where sources converge / diverge

{Dialectic surfacing}

## Implications for {mergePurpose}

{Action-oriented takeaways}
```

**For Personal Insight**:
```markdown
# {Title}

> **My take**: {Spine claim in user's voice}

## What I'm seeing

{User-authored interpretation, with sources as supporting evidence}

## Sources that shape this

- [[Source A]] — {what it gave me}
- [[Source B]] — {what it gave me}

## Where this goes next

{User's intended next move — ties back to mergePurpose}
```

### Step 8: Draft Review (Dialog 2)

Show the draft to the user (full content, not just summary). Ask:

```
Q: "초안 어떠세요? 어떻게 진행할까요?"
Header: "Draft review"
multiSelect: false
Options:
  - "이대로 저장 (Recommended if draft is solid)"
  - "톤·구조 수정 후 저장" — 자유 텍스트로 피드백
  - "특정 섹션만 다시" — 어느 섹션
  - "취소 — 저장 안 함"
```

If feedback given, regenerate the draft incorporating feedback. Loop max 2 times (third feedback → save with changes anyway, log remaining concern).

### Step 9: Save

Write the final note to `30. Permanent Notes/{title}.md` with frontmatter:

```yaml
---
type: note
aliases:
  - {alternative names if any}
description: {English 1-2 sentences — what this note synthesizes + when to reference}
author:
  - "[[Me]]"
date created: {today YYYY-MM-DD}
date modified: {today YYYY-MM-DD}
tags:
  - merged
  - {topic tags}
  - {output-type tag: literature-review | concept | personal-insight | etc.}
CMDS: "[[📚 {2NN Subcategory}]]"        # specific 📚 subcategory (201/202/210/220/240)
index: "[[🏷 Research Notes]]"           # 🏷 Index note (`🏷 Books` for 240)
status: completed
mergePurpose: {user's answer from Step 0 — verbatim}
sourceNotes:
  - "[[Source A]]"
  - "[[Source B]]"
  ...
related:
  - "[[Mothership related 1]]"
  - "[[Mothership related 2]]"
mainVaultRelated:
  - "→ LLM Wiki: {satellite page name}"  # cross-vault text refs
---
```

**Pre-flight check** (per CLAUDE.md rules):
- [ ] YAML 2 spaces, body TAB
- [ ] All wikilinks in YAML quoted
- [ ] Emoji prefixes preserved in `[[]]`
- [ ] All 7 required properties present
- [ ] `description` is English

### Step 10: Update Source Notes (Back-link)

For each `sourceNotes` entry, append at the bottom (do not modify body):

```markdown
---

> 🔗 **Merged into**: [[{new synthesis note}]] on {today} via /merge
```

This preserves N→1 traceability.

### Step 11: Report

```
✅ /merge — Synthesis complete
─────────────────────────────────────
Output:       [[{title}]]
Path:         30. Permanent Notes/{title}.md
Type:         {output type} → {2NN category}
Sources:      {N} notes merged
Purpose:      {mergePurpose}
Angle:        {chosen angle}
Cross-vault:  {N} mothership related, {N} LLM Wiki refs

Open questions surfaced (if any):
- {q1}
- {q2}

Next suggestion:
  - 이 합성 결과를 강의/뉴스레터/논문으로 → /share {title}
  - 이 합성에서 발견된 새 도구/방법 적용 → /develop {topic}
```

## Anti-patterns

- ❌ **Skipping the purpose gate** — synthesis without purpose drifts into generic summary. Always ask Step 0 first.
- ❌ **Reading all candidates without confirmation** — token-expensive if user wanted to drop half. Always do Step 2 dialog first.
- ❌ **Writing draft + saving in one step** — sacrifices the most valuable user input moment. Step 8 dialog is non-negotiable.
- ❌ **Treating sources as equals** — some sources are the spine, others are evidence. The angle in Step 4 determines weight.
- ❌ **Forgetting to back-link sources** — Step 10 is what makes the synthesis traceable / re-discoverable.
- ❌ **Auto-selecting 220 Personal Insights when sources dominate** — if 90% comes from external sources, it's a Literature Review (210), not a Personal Insight.

## Notes

- **Dialog count**: 0 (purpose) + 2 (candidates) + 4 (angle) + 5 (output) + 8 (draft review) = up to 5 AskUserQuestion calls. Keep each one focused (max 4 options).
- **Token economy**: Step 3 (deep read) is the expensive step. Keep candidate set ≤ 12 to avoid blowing context.
- **Iteration**: if a single `/merge` produces 2~3 distinct synthesis-worthy notes (e.g., one Concept + one Personal Insight), it's OK to run /merge twice with different angles on the same candidate set.
- **When NOT to /merge**: if input is one note + light annotation, that's `/connect` update, not `/merge`. Merge requires N≥3 substantive sources.
