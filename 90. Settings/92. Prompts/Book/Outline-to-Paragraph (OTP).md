---
title: "Outline → Paragraph (OTP)"
abbreviation: OTP
category: book-writing
created: "2026-05-02"
tags:
  - prompt/book
  - living-book
when_to_use: "아웃라인 노드 한 개를 첫 단락 초안으로 풀고 싶을 때"
---

아웃라인 노드 1개를 입력으로 받아 챕터 단락 초안을 생성한다. **W2 (Session 2)** 책쓰기의 첫 프롬프트.

## Input
- **Required**: 펼칠 아웃라인 노드 텍스트 (예: "AI가 가져가는 것 vs 사람의 영역")
- **Optional**: 관련 자료 (`20. Literature Notes/`, `00. Inbox/` 의 위키링크)
- **Optional**: 본인 책의 `core_question` (`70. Outputs/Book/My Book Outline.md` 에서)

## Output
- 4–7 문장의 단락 1개
- 위키링크 인용 포함 (자료를 줬다면)
- 다음 단락으로 이어지는 hook 문장으로 마무리

## Main Process

```
0. CONTEXT
   - core_question 읽기: My Book Outline.md → frontmatter
   - 자료 위키링크 따라가서 핵심 인용/사실 추출

1. WRITE
   - 첫 문장: 정의가 아닌 구체적 주장 또는 사례
   - 본문: 자료를 [[wikilink]] 로 인용하며 주장 전개
   - 마지막 문장: 다음 섹션이나 단락으로 이어지는 hook

2. VOICE CHECK
   - 짧은 문장, 구체적 명사 사용
   - 교과서 톤 ("일반적으로", "널리 알려진") 금지
```

## Constraints
- **Output only the paragraph.** 메타 코멘트·preamble 없이.
- 4–7 문장 (위반 시 짧으면 더 풀고, 길면 자르기)
- AI 자체 판단으로 새 자료를 만들어내지 않음 — 줘진 자료만 사용

## Post-processing (사람이 한다)

- 결과 단락 위에 본인 보이스 1–2 문단 추가 (선택: `Add-Author-Voice (AAV)` 프롬프트로 강제)
- 챕터 파일에 머지: `70. Outputs/Book/<chapter>.md`
- 잘 된 변형이 있으면 이 프롬프트를 본인 사례로 수정하여 본인 vault에 별도 저장

## Cohort Context

W2 실습 1단계 ("AI에게 단락 풀어 쓰기") 의 핵심 프롬프트. → [[Session 2 - AI 활용 + Claude Code]]
