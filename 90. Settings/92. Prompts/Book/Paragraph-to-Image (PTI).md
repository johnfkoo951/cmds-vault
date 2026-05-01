---
title: "Paragraph → Image (PTI)"
abbreviation: PTI
category: book-writing
created: "2026-05-02"
tags:
  - prompt/book
  - living-book
when_to_use: "챕터 단락에 어울리는 이미지 1장을 생성할 때"
---

단락 텍스트를 입력으로 받아 챕터에 임베드할 이미지 1장을 생성한다.

## Input
- **Required**: 단락 텍스트
- **Optional**: 챕터 톤 (예: "tech editorial", "personal essay", "academic")
- **Optional**: 색상 팔레트 (없으면 soft / muted 기본)

## Output
- 이미지 1장 (PNG 또는 JPG)
- alt 텍스트 한 줄 (이미지 없이 의미가 전달되도록)

## Main Process

```
0. ANALYZE
   - 단락의 핵심 컨셉 1개 추출 (literal scene 아님)
   - 챕터 전체 톤 추론 (frontmatter status, parent_book의 core_question)

1. PROMPT IMAGE MODEL
   Style guide:
   - Editorial illustration, clean composition
   - Minimal text in image (이미지 내 텍스트는 피한다 — 다국어 호환)
   - Soft palette, no stock-photo aesthetic
   - Conceptual > literal

2. ALT TEXT
   - 한 문장으로 이미지가 무엇인지 + 단락과 어떻게 연결되는지
```

## Constraints
- 이미지 내 텍스트 금지 (예외: 짧은 라벨 1-2단어)
- 사진 stock 느낌 금지
- 정사각 또는 16:9 권장 (Brain Homepage / Remotion 호환)

## Post-processing

- 저장: `70. Outputs/Book/<chapter-slug>/images/<descriptive-name>.png`
- 챕터 임베드: `![[<descriptive-name>.png|400]]`
- alt 텍스트는 챕터 마크다운 옆에 코멘트로 보존

## Cohort Context

W2 실습 3단계 ("본인 보이스 + 이미지 추가") 또는 매일 자동 갱신에서 단락이 새로 생성될 때 함께 호출된다.
