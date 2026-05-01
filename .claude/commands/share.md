---
description: "Orchestrate output creation by auto-delegating to existing skills (tone-writer, markdown-slides, pptx-cmds, write-post, social-media-content-adapter, business-docs, etc.) based on target format. Picks the right skill from source notes + user-specified format. Adapt the routing map to whatever skills you have installed."
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, mcp__qmd__query
---

# /share — CMDS Share Stage (Orchestrate Output Skills)

The Share stage takes accumulated knowledge (200 Literature, 600 Specialties) and produces external-facing artifacts. **This command does NOT write content directly** — it picks the right specialized skill from the mothership skill library and delegates with the right inputs.

> **🧭 Prerequisite**: `CMDS.md` for category context. The 800 Outputs categories (801 PhD, 802 Articles, 840 Lectures, 831 Consulting, etc.) are the typical destinations.

## Input

`$ARGUMENTS`

- A **source note name / topic** + optional format hint (e.g., "Schema as Harness 뉴스레터로", "지식관리 강의 슬라이드")
- **Blank**: ask via AskUserQuestion

## Skill Routing Map

| User intent / target format | Skill to delegate | 800 destination |
|----------------------------|------------------|-----------------|
| 시그니처 뉴스레터 (본인 스타일) | `<your-newsletter-skill>` (e.g. `thebetter-writer`) | 802 Articles |
| 일반 콘텐츠 (3가지 톤 중 선택) | `tone-writer` | 802 Articles |
| AI 활용 사례 / 개발 게시글 | `write-post` | 802 Articles |
| 다편 시리즈 / 통합편 | `series-writer` | 802 Articles |
| 슬라이드 (Marp/Deckset) | `markdown-slides` | 840 Lectures, 822 Conferences |
| pptx 발표 자료 | `pptx-cmds` | 840 Lectures |
| Keynote 네이티브 | `keynote` | 840 Lectures |
| 강의 모듈 / 커리큘럼 설계 | `course-designer` | 841 Curriculum |
| 슬라이드 → 영상 (TTS 나레이션) | `markdown-video` | 701 YouTube |
| TTS 오디오만 | `audio-generator` | 701 YouTube |
| SNS 멀티플랫폼 게시 | `social-media-content-adapter` | 710 SNS |
| 에세이 / 인터랙티브 글쓰기 | `interactive-writing-assistant` | 802 Articles |
| 에세이 리뷰·개선 | `essay-reviewer-korean` | (review only) |
| 견적서 · 인보이스 · 제안서 | `business-docs` | 831 Consulting |
| Markdown → PDF | `md-to-pdf` | (any) |
| 웹 페이지 / 랜딩 페이지 | `cmdspace-web-builder` 또는 `minimal-homepage` | 806 Webpages |
| Docusaurus 사이트 | `obsidian-docusaurus-builder` | 806 Webpages |
| Vercel 배포 | `vercel-deployer` | (deployment) |

## Process

### Step 1: Identify Source Notes

If `$ARGUMENTS` mentions a topic/title, find source notes:

```
mcp__qmd__query(
  searches=[
    {type: "vec", query: "<topic>"},
    {type: "lex", query: "<exact title>"},
  ],
  intent="Find source notes (200 Literature, 600 Specialty, 220 Personal Insights) for share"
)
```

Also Grep `30. Permanent Notes/` for the topic. Prefer 200/220/600 notes (they are synthesis-grade).

If user provided exact note name, just resolve the path.

### Step 2: Determine Target Format (Dialog 1 — only if not in $ARGUMENTS)

If `$ARGUMENTS` already contains a clear format hint (뉴스레터, 슬라이드, 영상, SNS 등), skip this dialog.

Otherwise:

```
AskUserQuestion (single):
  Q: "어떤 형태로 만들까요?"
  Header: "Output format"
  Options:
    - "시그니처 뉴스레터" (your newsletter skill, if installed)
    - "강의 슬라이드" (markdown-slides 또는 pptx-cmds)
    - "AI 활용 사례 게시글" (write-post)
    - "SNS 멀티플랫폼" (social-media-content-adapter)
    (Recommended 옵션은 source note의 frontmatter / 최근 활동 패턴으로 동적 결정)
```

### Step 3: Determine Audience & Tone (Dialog 2 — when ambiguous)

For skills that have audience/tone parameters:

- `tone-writer` → 유머 / 통찰 / 진지
- 본인 시그니처 newsletter skill (예: `thebetter-writer`) → 자동 (스타일 고정)
- `pptx-cmds` / `markdown-slides` → 청중 (학생 / 임원 / 일반 / 전문가)
- `social-media-content-adapter` → 어느 플랫폼 (Threads / X / LinkedIn / Instagram / YouTube)

Skip if format itself implies the answer (예: 본인 시그니처 newsletter → 톤 고정).

```
AskUserQuestion (single, when needed):
  Q: "{format}의 톤/청중을 선택해주세요"
  Header: "Tone/audience"
  Options: ...
```

### Step 4: Pre-flight Source Read

Read the resolved source note(s) in full. Extract:
- Core thesis (1~2 sentences)
- Key supporting points (3~5)
- Cited sources / wikilinks (for back-reference)
- User's voice signals (if any author commentary)

This becomes the briefing material passed to the delegated skill.

### Step 5: Delegate via Skill

Invoke the chosen skill via the `Skill` tool:

```
Skill(skill: "<your-newsletter-skill>", args: "<source content + briefing>")  # e.g., thebetter-writer
Skill(skill: "markdown-slides", args: "<source + audience hint>")
Skill(skill: "tone-writer", args: "<source + tone choice>")
...
```

The delegated skill handles its own internal flow. `/share` waits for completion and returns the result location.

For multi-skill chains (예: 노트 → 슬라이드 → 영상), do them sequentially:
1. `markdown-slides` to build slides
2. `markdown-video` to convert to video with TTS

### Step 6: Save Location

Most output skills handle their own save location. `/share` confirms:

- 802 Articles → check skill output ended up in `70. Outputs/71. Published/` or similar
- 840 Lectures → `70. Outputs/72. Presentations/` or `70. Outputs/73. Courses/`
- 706/710 SNS → `70. Outputs/71. Published/` with platform tag
- 806 Webpages → check `70. Outputs/74. Projects/` or DEV folder

If the delegated skill doesn't save to the right CMDS-aligned location, **propose the move** but don't auto-move (let user decide).

### Step 7: Frontmatter Patch (if delegated skill produced a note)

If the output is a note, ensure CMDS frontmatter is correctly stamped:

```yaml
CMDS: "[[📚 8XX {Subcategory}]]"        # e.g., [[📚 802 Articles]], [[📚 840 Lectures]], [[📚 831 Consulting]]
index: "[[🏷 {Index Note}]]"            # e.g., [[🏷 Draft Article]] / [[🏷 Lecture Notes]] / [[🏷 Project Notes]] / [[🏷 Outcomes]]
shareSourceNotes:
  - "[[Source synthesis 1]]"
shareFormat: "{format}"
sharePurpose: "{briefly why this share happened — e.g., 4월 LG CNS 강의용}"
```

If the skill already wrote frontmatter, add only the missing `shareSourceNotes` / `shareFormat` / `sharePurpose` fields (don't overwrite existing properties).

### Step 8: Back-link Source Notes

Append to each source note:

```markdown
---

> 📤 **Shared as {format}**: [[{output note/file}]] on {today} via /share
```

### Step 9: Report

```
📤 /share — Output produced
─────────────────────────────────────
Source(s):     {list of 200/220/600 notes}
Format:        {chosen format}
Skill used:    {skill name}
Output:        {file path}
CMDS dest:     {800 subcategory}

Promotion path:
  - {next manual step if any: 게시 / PDF 변환 / 영상화 등}
  - 또는 다중 형식 변환 → /share 같은 source로 다른 format 호출

Next suggestion:
  - 발행 후 인사이트가 새로 생기면 → /connect 으로 캡처
  - 발표 후 청중 피드백 → /merge 로 새 Personal Insight 합성
```

## Multi-format Chains (Common Patterns)

**Pattern A: 합성 → 강의 → 영상**
```
/merge "지식관리 강의 자료"
  → /share "강의 슬라이드"  (markdown-slides)
  → /share "영상화"        (markdown-video)
```

**Pattern B: 합성 → 뉴스레터 → SNS 분배**
```
/merge "이번 주 통찰"
  → /share "<your newsletter format>"  (your newsletter skill)
  → /share "SNS 멀티플랫폼"        (social-media-content-adapter, 같은 source)
```

**Pattern C: 합성 → 컨설팅 결과물**
```
/merge "고객 피드백 분석"
  → /share "제안서"                (business-docs)
```

## Anti-patterns

- ❌ Writing share content directly in `/share` — always delegate to a specialized skill. `/share` is an orchestrator, not a writer.
- ❌ Skipping Step 1 (source resolution) — sharing without identified source notes loses traceability and back-link.
- ❌ Forcing the user through Dialog 1 when format is already specified in `$ARGUMENTS` — respect explicit user input.
- ❌ Auto-moving the output to a different CMDS folder — propose, don't move. User controls final placement.
- ❌ Choosing the wrong skill (e.g., a generic `tone-writer` when a specific signature-newsletter skill exists for the user's voice).

## Notes

- The skill registry is dynamic — new skills added to `90. Settings/94. Agent Settings/claude/skills/` should be folded into the routing map. When unsure, AskUserQuestion offers "Other" → user can name a skill explicitly.
- For 700 Creatives outputs (YouTube, music, digital art), the chain often starts with `markdown-slides` or `image-generation-skill`.
- Always honor the source note's `mergePurpose` (set in `/merge`) when picking format — if mergePurpose was "강의·강연", default the format to slides/curriculum.
