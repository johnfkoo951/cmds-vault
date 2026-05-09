---
title: "Add Author Voice (AAV) — Example"
abbreviation: AAV-EX
category: book-writing
parent_prompt: "[[Add-Author-Voice (AAV)]]"
created: "2026-05-08"
tags:
  - prompt/book
  - prompt/example
  - living-book
when_to_use: "AAV가 generic AI 단락을 어떻게 본인 보이스로 바꾸는지 볼 때"
---

> 부모 프롬프트: [[Add-Author-Voice (AAV)]]

## Scenario

OTP가 만든 단락이 본인이 쓴 것 같지 않다. AAV에 voice cue 와 함께 넘겨 본인 톤을 입힌다. (입력은 [[Outline-to-Paragraph (OTP) - Example]] 의 출력과 동일.)

## Sample Input

원본 단락 (OTP output):

```
2025년 한 엔지니어가 자기 코드의 80%를 LLM에게 맡겼다고 말했을 때, 이 직업의 좌표축이 흔들렸다. AI는 문법, 보일러플레이트, 그리고 이미 알려진 패턴을 가져간다 — 이 부분의 노동을 사람이 다시 할 이유가 없다. 그러나 무엇을 만들지 정하는 의사결정과 코드가 배포된 후의 시스템적 책임은 여전히 사람의 영역이다. 본인의 보이스, 즉 "왜 이 문제를 푸는가"의 서술은 LLM이 흉내내지 못한다. 다음 섹션에서 이 보이스가 책쓰기에서는 어떻게 살아남는지 본다.
```

Voice cue (BRAIN_PROMPT.md 발췌):

```
- 짧은 문장 선호
- 일반화 ("It is widely known") 대신 본인 경험 1개로 시작
- "알고리즘" 보다 "이 코드가 돌면" 같은 동사형 표현
```

## Sample Output

```
나는 작년 11월 어느 새벽에, 내가 짠 코드 두 줄이 LLM이 짠 코드 200줄보다 더 많은 일을 하는 걸 봤다. AI는 문법과 보일러플레이트를 가져간다. 한 번 본 패턴은 사람이 다시 손으로 칠 이유가 없다. 그러나 [my-anecdote: 그날 새벽에 내가 결정한 것 — 왜 이 두 줄이어야 했는지]는 LLM이 알지 못했다. 보이스는 거기에서 산다. 다음 섹션에서, 이 보이스가 책쓰기로 옮겨갈 때 무엇이 살아남는지 본다.
```

## Notes

- 첫 문장이 일반화에서 본인 일화로 바뀜 ("한 엔지니어가" → "나는 작년 11월")
- `[my-anecdote: ...]` placeholder 1개 — 사람이 음성 모드로 채울 자리
- 길이: 원본 5문장 → 새 단락 6문장 → ±20% 안
- 사실 골격 보존 (AI = 문법·보일러플레이트, 사람 = 의사결정)
- 후처리: placeholder 채우기 전엔 챕터에 머지 금지 (AAV의 룰)
