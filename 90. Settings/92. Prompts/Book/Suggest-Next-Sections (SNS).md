---
title: "Suggest Next Sections (SNS)"
abbreviation: SNS
category: book-writing
created: "2026-05-02"
tags:
  - prompt/book
  - living-book
when_to_use: "한 섹션을 끝낸 뒤 다음에 무엇을 써야 할지 막혔을 때"
---

지금까지 쓴 챕터 본문을 입력으로 받아, **다음 섹션 후보 3개**를 제안한다. 책쓰기의 막힘 지점을 푸는 도구.

## Input
- **Required**: 현재 챕터 본문 전체 (`70. Outputs/Book/<chapter>.md`)
- **Optional**: `core_question` (My Book Outline.md frontmatter)
- **Optional**: 이미 쓴 다른 챕터 헤더들 (중복 회피용)

## Output
- 옵션 A/B/C — 헤더 + 2줄 설명
- 마지막 줄: 추천 1개 + 이유

## Main Process

```
0. READ
   - 챕터 본문 전체 읽기
   - 마지막 섹션의 hook 문장 파악 (단락 마지막 문장)
   - core_question 과의 거리 측정 — 너무 멀어졌으면 끌어올 후보 제안

1. GAP ANALYSIS
   - "독자가 지금 시점에 던질 질문 3개"를 추론
   - 그 질문에 답하는 섹션 후보 만들기

2. CONSTRAIN
   - 각 후보 헤더는 구체적 (X "Discussion" / "Implications", O "비즈니스 출신과 엔지니어 출신이 같은 챕터를 읽을 때")
   - 각 후보는 본인의 다른 챕터 헤더와 중복되지 않음

3. RECOMMEND
   - 3개 중 1개 추천 + 한 줄 이유
   - 만약 셋 다 약하면: "이 챕터는 끝났을 가능성. 다음 챕터로 넘어가는 것을 고려" 한 줄 출력
```

## Constraints
- 정확히 3개 (더 적거나 많지 않음)
- 헤더는 5–10 단어 (한국어 기준)
- 추상명사 헤더 금지: "분석", "고찰", "전망" 등

## Output Format

```markdown
- **A — <header>**: <2 lines>
- **B — <header>**: <2 lines>
- **C — <header>**: <2 lines>

**추천**: <A/B/C> — <한 줄 이유>
```

## Post-processing

- 추천을 무조건 따르지 않음 — 본인 `core_question` 과 가장 가까운 것을 고른다
- 셋 다 약하면 챕터 종료 신호로 받아들이기

## Cohort Context

W2 이후 챕터 작업 중 막힘 지점에서 사용. W3 매일 자동 업데이트 워크플로우는 이 프롬프트를 호출하지 않는다 (사람의 판단 영역).
