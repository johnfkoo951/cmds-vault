---
title: "Daily Research Briefing (DRB)"
abbreviation: DRB
category: batch
created: "2026-05-14"
tags:
  - prompt
  - briefing
  - research
  - web-search
  - daily
when_to_use: "능동적으로 추적 중인 주제·프로젝트의 최신 논문·뉴스·블로그를 매일 한 장으로 받고 싶을 때"
---

능동적으로 작업 중인 주제(`📚 102 Topics`)와 활성 프로젝트 노트의 최근 수정 이력을 자동 스캔해, 그 주제들에 대한 최신 자료(논문·뉴스·블로그)를 매일 한 장의 브리핑으로 만든다. 원작 [DRB (ai4pkm-vault)](https://github.com/jykim/ai4pkm-vault/blob/main/_Settings_/Prompts/Daily%20Research%20Briefing%20(DRB).md) 를 CMDS 볼트에 맞게 개조 — 토픽 소스를 단일 `Topics/` 폴더가 아니라 CMDS 의 다중 소스(102 Topics, 활성 챕터, 진행 중인 프로젝트)로 일반화.

## Input

- **Default source**: 최근 `lookback_days` (기본 7) 일 내에 수정된 노트 중 다음에 해당하는 것:
	- `30. Permanent Notes/` 의 `CMDS: "[[📚 102 Topics]]"` 노트
	- `📖 100 Themes` 계열 (`📚 101 Interests`, `📚 103 Variables`, `📚 104 Terminologies`)
	- 명시적 `status: inProgress` 가 붙은 진행 중 노트
- **Optional `scope`**: 토픽 소스를 좁힘
	- `topics` (기본): 위 default
	- `book`: `70. Outputs/Book/Ch*/` 의 최근 수정 챕터 + `My Book Outline.md` 의 `core_question`
	- `project:<name>`: 특정 프로젝트 폴더 (예: `70. Outputs/74. Projects/<name>`)
	- `paths:<comma-separated paths>`: 임의의 폴더 목록
- **Optional params**:
	- `max_topics`: 기본 5 (한 번에 다룰 토픽 최대 개수)
	- `lookback_days`: 기본 7
	- `language`: 검색은 영어, 요약 언어 (기본 ko)

## Output

- **File**: `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/{{YYYY-MM-DD}}-DRB.md`
	- `.claude/rules/file-creation-rules.md` — 모든 AI 산출물은 `03. AI Agent/{env}/` 에 먼저 착륙
- **CMDS 7-field frontmatter** 준수 (`.claude/rules/frontmatter-standard.md`)
- 토픽당 2–3건의 큐레이트된 자료 + 한 줄 "Implication" (이 자료가 어디에 영향을 주는지)
- 'Topics to Develop': 자료에서 부각된 신규 토픽 후보 (자동 생성하지 않고 후보로만 기록)

## Main Process

```
1. ACTIVE TOPIC DETECTION
   - scope 에 따라 후보 노트 집합 결정 (default: 102 Topics + 100 Themes + status:inProgress)
   - 최근 lookback_days 일 수정 파일만 추출 (mtime 기준)
   - status 가 'completed' / 'archived' 면 제외
   - 수정 시점 desc 정렬, 상위 max_topics 개만 선택

2. KEYWORD EXTRACTION (per topic note)
   - 노트 제목 (filename 의 emoji prefix 는 검색어에서 제외)
   - H2/H3 헤더 텍스트
   - frontmatter 의 'aliases', 'tags', 그리고 (있다면) 'keywords'
   - scope=book 인 경우: My Book Outline 의 'core_question' 의 핵심 명사 prepend
   - 결과 예시:
     {
       topic: "LLM Evaluation",
       keywords: ["LLM-as-a-judge", "model evaluation 2026"],
       context_note: "최근 'JudgeBench' 인용 추가됨"
     }

3. WEBSEARCH (per topic, 2–3 queries)
   - 영어로 검색:
     "[keyword]" 2026 site:arxiv.org OR site:scholar.google.com
     "[keyword]" 2026 (news | release | announcement)
     "[keyword]" tutorial guide 2026
   - 한국어 도메인이 필요하면 ko query 1개 추가
   - 현재 년도 우선, 권위 있는 소스 우선

4. DEDUP & RANK
   - 본 vault 에 이미 들어온 자료 제외:
     - 20. Literature Notes/ 에 같은 URL/제목이 있는지
     - 00. Inbox/02. Clippings/ 에 같은 URL/제목이 있는지
   - 토픽당 top 2–3건 선정
   - 우선순위:
     High   : 새 논문, 주요 모델/제품 릴리스, 권위 있는 분석 — 추적 중 토픽에 직접 영향 가능
     Medium : 튜토리얼·실전 적용 사례
     Low    : 일반 기사·오피니언

5. DEEP FETCH (선택, high 항목만)
   - WebFetch 로 상위 결과 1–2건의 본문 가져와 핵심 인용 1–2 문장 추출

6. WRITE BRIEFING
   - 아래 Output Format 으로 파일 생성
   - 각 항목 끝에 'Implication' 한 줄 — 어느 노트/프로젝트/챕터에 어떤 영향을 주는지
   - 'Topics to Develop' 섹션: 새 토픽 후보 (102 Topics 에 아직 없음)

7. CROSS-LINKING
   - 본 vault 의 기존 토픽 노트로 위키링크 (emoji prefix 포함 필수, `.claude/rules/wikilink-rules.md`)
   - 새 토픽 노트를 자동 생성하지 않음 — `/connect` 로 사용자가 결정
   - 일일 로그가 있는 모드면 (scope=book 등) 해당 로그에 한 줄 항목 append
```

## Constraints

- **검색은 영어, 요약은 한국어** (기본; `language` 로 변경 가능)
- **dedup 필수**: vault 에 이미 들어온 자료 (URL 또는 제목 일치) 는 제외
- **위키링크 emoji prefix 규칙 준수** — `[[📚 102 Topics]]` (O), `[[102 Topics]]` (X — `.claude/rules/wikilink-rules.md`)
- **새 토픽 노트를 자동 생성하지 않음** — 'Topics to Develop' 후보로만 기록
- **frontmatter v2**: 출력 파일은 CMDS 7-field 준수, `description` 은 영문·double-quoted
- **vault 본문에 직접 머지하지 않음** — 브리핑은 inbox 자료. 본문 머지는 사용자가 결정 (책쓰기 모드면 OTP/AAV 활용)

## Output Format

```markdown
---
type: note
aliases: []
description: "Daily research briefing — surfaces fresh papers, news, and blogs for currently active topics in the vault. Scope: {{scope}}. Generated YYYY-MM-DD."
author:
	- "[[Me]]"
date created: YYYY-MM-DD
date modified: YYYY-MM-DD
tags:
	- briefing
	- research
	- daily
CMDS: "[[📚 102 Topics]]"
status: unread
topics_covered:
	- "[[Topic 1]]"
	- "[[Topic 2]]"
---

# {{YYYY-MM-DD}} Daily Research Briefing

> Scope: **{{scope}}** · Lookback: {{lookback_days}}d · Topics: {{N}}

## Summary

오늘의 브리핑: 활성 토픽 {{N}}개 — {{Topic 1, Topic 2, ...}}. 주목할 한 건: **{{top_story_title}}**.

## Topic Updates

### 1. [[📚 102 Topics|Topic Name]]
**최근 작업 컨텍스트**: {{recent_focus_or_section}}
**검색 키워드**: keyword 1, keyword 2

#### 자료

- **"{{Paper Title}}"** — arXiv ({{YYYY-MM}})
	{{1–2 문장 요약, 한국어}}
	→ [Paper](https://arxiv.org/abs/...)
	**Implication**: {{어느 노트/챕터/프로젝트에 어떤 영향}}

- **"{{Blog Post Title}}"** — Google AI Blog
	{{1–2 문장 요약}}
	→ [Blog](https://...)
	**Implication**: {{...}}

---

### 2. [[Topic 2]]
...

## Topics to Develop

> 오늘 자료에서 부각된 신규 토픽 후보. 실제 노트 생성은 `/connect` 로 직접 결정.

- "evals as code" — 평가 자동화 패러다임. 분석 워크플로우 노트에 들어갈 후보.
- ...

## Quick Reference

| Topic | Top Update | Action |
|-------|------------|--------|
| Topic 1 | {{1줄 요약}} | Read / Save / Skip |
| Topic 2 | {{1줄 요약}} | Read / Save / Skip |

## Sources

- [Paper Title](URL) — Topic 1
- [Blog Title](URL) — Topic 2

## Coverage Report

- 활성 토픽: {{N}} 개 탐지 (scope={{scope}}, lookback={{lookback_days}}일)
- 검색 쿼리: {{Q}} 개 실행
- dedup 으로 제외: {{D}} 건 (이미 vault 에 있음)
- 신규 자료: {{F}} 건 채택
```

## Mode: Book Writing (선택)

`scope=book` 일 때:

- 토픽 소스를 `70. Outputs/Book/Ch*/*.md` 와 `My Book Outline.md` 로 전환
- 키워드 추출 시 `core_question` 의 핵심 명사를 prepend
- 'Implication' 라인을 "Book-side Implication" 으로 작성 — 어느 챕터/섹션에 영향
- `70. Outputs/Book/Daily Update Log.md` 에 한 줄 항목 append
- 사후 처리는 [[Outline → Paragraph (OTP)]] / [[Add-Author-Voice (AAV)]] 와 짝

## Post-processing (사람이 한다)

1. 브리핑 파일 검토 — Read / Save / Skip 결정
2. **Save** 항목:
	- 풀 텍스트가 필요하면 `00. Inbox/02. Clippings/` 로 클리핑
	- 노트/챕터 본문에 인용으로 머지 (책 모드면 OTP/AAV 활용)
	- 발견이 전략적이면 해당 토픽 노트의 본문 또는 frontmatter 업데이트
3. **Topics to Develop** 항목 중 채택할 후보는 `/connect` 로 `📚 102 Topics` 에 등록
4. 다 처리하면 frontmatter `status: completed`, 며칠 안 본 채로 쌓이면 `archived`

## Configuration

```yaml
# orchestrator.yaml 예시 — daily cron
- type: agent
	name: Daily Research Briefing (DRB)
	cron: 0 7 * * *  # 매일 오전 7시
	output_path: "00. Inbox/03. AI Agent/03-1. Claude Code (MBP)"
	agent_params:
		scope: topics            # topics | book | project:<name> | paths:<a,b>
		max_topics: 5
		lookback_days: 7
		language: ko
		search_in: en
		include_voice: false
```

## Differences from Source

원작 [DRB (ai4pkm-vault)](https://github.com/jykim/ai4pkm-vault/blob/main/_Settings_/Prompts/Daily%20Research%20Briefing%20(DRB).md) 와의 차이:

| 항목 | 원작 DRB | 본 버전 (CMDS) |
|------|---------|-------------|
| 토픽 소스 | `Topics/` 단일 폴더 | `102 Topics` + `100 Themes` + `status:inProgress` (scope 로 확장) |
| 출력 위치 | `AI/Briefing/` | `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/` (CMDS 룰) |
| 위키링크 | 일반 | emoji prefix 강제 (`📚 102 Topics`) |
| frontmatter | 최소 (`title, created, ...`) | CMDS 7-field (`description` 영문 double-quoted) |
| dedup | 일반 | vault 의 20. Literature Notes / 02. Clippings 와 cross-check |
| 신규 토픽 | 자동 생성 가능성 | 자동 생성 금지, `/connect` 로 사용자 결정 |
| 모드 | 단일 | `scope` 로 책쓰기/프로젝트/임의 경로 확장 |

## Related

- `/connect` — 'Topics to Develop' 후보를 실제 `📚 102 Topics` 노트로 등록
- `/query {topic}` — 브리핑 전에 vault 내부에 이미 있는 자료 먼저 확인
- [[Generate Daily Roundup (GDR)]] — 하루의 vault 내부 활동 정리 (외부 자료는 다루지 않음). DRB 와 짝.
- 책쓰기 모드 사후: [[Outline → Paragraph (OTP)]], [[Add-Author-Voice (AAV)]]
- 원작: [DRB on ai4pkm-vault](https://github.com/jykim/ai4pkm-vault/blob/main/_Settings_/Prompts/Daily%20Research%20Briefing%20(DRB).md)
