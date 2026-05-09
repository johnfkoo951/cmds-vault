---
title: "Paragraph → Image (PTI) — Example"
abbreviation: PTI-EX
category: book-writing
parent_prompt: "[[Paragraph-to-Image (PTI)]]"
created: "2026-05-08"
tags:
  - prompt/book
  - prompt/example
  - living-book
when_to_use: "PTI가 어떤 이미지 프롬프트와 alt 텍스트를 만드는지 볼 때"
---

> 부모 프롬프트: [[Paragraph-to-Image (PTI)]]

## Scenario

챕터 1 첫 단락 (AAV 통과 결과)에 어울리는 editorial illustration 1장. 챕터 톤은 `tech editorial`.

## Sample Input

단락:

```
나는 작년 11월 어느 새벽에, 내가 짠 코드 두 줄이 LLM이 짠 코드 200줄보다 더 많은 일을 하는 걸 봤다. AI는 문법과 보일러플레이트를 가져간다. ...
```

챕터 톤: `tech editorial`
색상 팔레트: 기본 (soft / muted)

## Sample Output

이미지 모델 프롬프트:

```
Editorial illustration, conceptual not literal: two small handwritten lines of code on the left, a cascading column of machine-typed code on the right, both feeding into a single quiet shape — a person at a desk silhouetted at dawn. Soft muted palette, deep blue and warm cream. Minimal composition. No text in the image. 16:9 aspect ratio.
```

Alt 텍스트:

```
사람이 새벽에 쓴 두 줄과 기계가 쏟아낸 코드 한 줄기가 같은 책상 위로 모여드는 장면 — 사람의 결정과 LLM의 생성이 만나는 지점.
```

저장 경로: `70. Outputs/Book/01-ai-and-voice/images/ai-and-voice-opening.png`
챕터 임베드: `![[ai-and-voice-opening.png|400]]`
![[ai-and-voice-opening.png|400]]
## Notes

- "Conceptual > literal" 적용 — 단락의 사례를 그대로 그리지 않고 추상화
- 이미지 내 텍스트 없음 — 다국어 호환 유지
- 16:9 — Brain Homepage / Remotion 호환
- alt 텍스트만 읽어도 단락과의 연결이 전달됨
