---
title: "Add Author Voice (AAV)"
abbreviation: AAV
category: book-writing
created: "2026-05-02"
tags:
  - prompt/book
  - living-book
when_to_use: "AI가 만든 단락이 generic할 때 본인 보이스를 덧입힌다"
---

AI가 생성한 단락 위에 본인 보이스를 강제로 덧입힌다. **W2 실습 3단계의 의무 도구** — AI 단락은 이 프롬프트를 거치지 않은 채로 챕터에 들어가지 않는다.

## Input
- **Required**: 수정할 AI 생성 단락
- **Required**: 본인 보이스 cue (vault 루트의 `BRAIN_PROMPT.md` 에서)
- **Optional**: 본인의 과거 글 1-2 단락 (스타일 참조용)

## Output
- 수정된 단락 1개 (원본 길이 ±20% 이내)
- `[my-anecdote]` placeholder 표시 (본인이 채워야 할 자리)

## Main Process

```
0. READ
   - BRAIN_PROMPT.md 의 voice cue 흡수
   - 원본 단락의 주장 구조 파악 (변경 금지)

1. REWRITE
   - 첫 문장: 명백하게 본인 — 구체적, 의견 있음, "It is widely known" 류 금지
   - 본문 중 최소 1문장: 본인의 실제 경험 참조 (없으면 [my-anecdote] placeholder)
   - 호흡 (cadence): voice cue 와 일치
   - 길이: 원본 ±20%

2. MARK
   - [my-anecdote] placeholder 위치 표시
   - 원본의 사실/주장은 보존
```

## Constraints
- **Output only the revised paragraph.** preamble 없음.
- 원본의 사실관계·논리 변경 금지 — 보이스만 입힘
- placeholder 형식: `[my-anecdote: <짧은 hint>]` (사람이 무엇을 채울지 힌트)

## Post-processing (사람이 한다)

- `[my-anecdote: ...]` placeholder 를 실제 본인 일화로 교체
  - 음성 모드 (Gobi Desktop) 사용 권장 — 일화는 음성으로 더 자연스럽게 나온다
- placeholder가 채워지지 않은 단락은 챕터에 머지하지 않는다 (룰)
- 결과를 `70. Outputs/Book/<chapter>.md` 에 머지

## Why this matters

AI가 만든 단락만 모이면 책 전체가 평균값으로 수렴한다. AAV는 **각 단락이 본인이 쓴 것임을 보장하는 게이트**다. cohort 책의 Ch.7 ("N개 도메인의 음성 책쓰기") 가 변별력을 갖는 이유.

## Cohort Context

W2 실습 3단계의 의무 도구. W3 매일 자동 업데이트는 이 프롬프트를 자동 호출하지 않는다 — 보이스 추가는 사람의 판단이다.
