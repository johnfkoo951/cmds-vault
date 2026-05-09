---
title: "Outline → Paragraph (OTP) — Example"
abbreviation: OTP-EX
category: book-writing
parent_prompt: "[[Outline-to-Paragraph (OTP)]]"
created: "2026-05-08"
tags:
  - prompt/book
  - prompt/example
  - living-book
when_to_use: "OTP가 실제로 어떤 입출력을 기대하는지 처음 볼 때"
---

> 부모 프롬프트: [[Outline-to-Paragraph (OTP)]]

## Scenario

W2 첫 실습. 본인 책 아웃라인의 한 노드를 첫 단락 초안으로 풀어쓴다. 챕터 1 — "AI가 가져가는 것 vs 사람의 영역".

## Sample Input

```
아웃라인 노드: AI가 가져가는 것 vs 사람의 영역
core_question: 음성으로 책을 쓰는 시대에, 사람의 보이스는 무엇으로 남는가?
참고 자료: [[2026-04-30 - Karpathy on Software 3.0]]
```

## Sample Output

```
2025년 한 엔지니어가 자기 코드의 80%를 LLM에게 맡겼다고 말했을 때, 이 직업의 좌표축이 흔들렸다. AI는 문법, 보일러플레이트, 그리고 이미 알려진 패턴을 가져간다 — 이 부분의 노동을 사람이 다시 할 이유가 없다. 그러나 [[2026-04-30 - Karpathy on Software 3.0|Karpathy의 관찰]]처럼, 무엇을 만들지 정하는 의사결정과 코드가 배포된 후의 시스템적 책임은 여전히 사람의 영역이다. 본인의 보이스, 즉 "왜 이 문제를 푸는가"의 서술은 LLM이 흉내내지 못한다. 다음 섹션에서 이 보이스가 책쓰기에서는 어떻게 살아남는지 본다.
```

## Notes

- 첫 문장이 정의가 아니라 구체적 사례 (엔지니어 일화) — OTP voice check 통과
- 위키링크로 자료 인용 — 임의로 새 자료 만들지 않음
- 마지막 문장이 다음 섹션 hook — AAV / SNS 로 이어지는 seam
- 5문장 → OTP의 4–7문장 제약 안
- 후처리: 이 단락을 [[Add-Author-Voice (AAV)]] 에 넘겨 본인 보이스를 입힌다
