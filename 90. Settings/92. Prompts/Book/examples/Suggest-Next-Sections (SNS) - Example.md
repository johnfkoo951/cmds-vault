---
title: "Suggest Next Sections (SNS) — Example"
abbreviation: SNS-EX
category: book-writing
parent_prompt: "[[Suggest-Next-Sections (SNS)]]"
created: "2026-05-08"
tags:
  - prompt/book
  - prompt/example
  - living-book
when_to_use: "SNS의 A/B/C 추천 형식이 실제로 어떻게 출력되는지 볼 때"
---

> 부모 프롬프트: [[Suggest-Next-Sections (SNS)]]

## Scenario

챕터 1의 첫 섹션 ("AI가 가져가는 것 vs 사람의 영역")을 마쳤다. 다음에 무엇을 쓸지 막혔다.

## Sample Input

현재 챕터 본문 (마지막 섹션 끝 단락):

```
... 보이스는 거기에서 산다. 다음 섹션에서, 이 보이스가 책쓰기로 옮겨갈 때 무엇이 살아남는지 본다.
```

`core_question`: "음성으로 책을 쓰는 시대에, 사람의 보이스는 무엇으로 남는가?"

이미 쓴 다른 챕터 헤더: (없음 — 첫 챕터)

## Sample Output

```markdown
- **A — 음성으로 받아쓰기 vs 손으로 쓰기, 두 단락의 결이 어떻게 갈리는가**: 같은 주장을 음성·텍스트로 각각 작성한 단락 비교. 보이스의 흔적을 가시화.
- **B — AAV 프롬프트의 placeholder가 책 전체에서 본인 일화의 진입점이 되는 이유**: 도구 차원의 답. 어떻게 본인 보이스를 강제하는가.
- **C — 다른 작가의 보이스를 흉내내는 것과 본인 보이스를 강화하는 것의 차이**: 일반론 / 다소 추상적.

**추천**: A — core_question이 "보이스가 무엇으로 남는가"인데, A는 보이스의 흔적을 단락 단위로 보여주는 가장 직접적 답이다. B는 도구 이야기로 빠지고, C는 추상적이다.
```

## Notes

- 정확히 3개 — SNS의 카운트 제약
- 각 헤더가 5–10단어 한국어, 추상명사 ("분석", "고찰", "전망") 없음
- 추천 1개 + 한 줄 이유 — 형식 그대로
- 만약 셋 다 약했으면 출력은: `이 챕터는 끝났을 가능성. 다음 챕터로 넘어가는 것을 고려.`
