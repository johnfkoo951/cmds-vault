---
type: core-context
aliases:
  - User Context
  - 핵심 맥락
description: User identity, reuse axes, and philosophy. LLMWiki commands MUST read this BEFORE every ingest/query/lint so operations align with the user's purpose, not just structure. Fill in placeholders before running the first ingest.
author:
  - "[[{your-name}]]"
date created: {YYYY-MM-DD}
date modified: {YYYY-MM-DD}
tags:
  - system
  - llm-wiki
  - core-context
version: "1.0"
snapshot_date: {YYYY-MM-DD}
status: template      # template (unfilled) | seeded (auto-seeded by /cmds-llm-wiki-status, awaiting review) | active (user-reviewed)
---

# 🧭 Core Context — LLMWiki 사용자 맥락

> **템플릿 노트**입니다. 아래 placeholder 를 본인 맥락으로 채운 뒤 frontmatter `status:` 를 `active` 로 바꾸세요.
>
> 채우는 방법:
> 1. **자동 시드 (권장)** — `/cmds-llm-wiki-status` 가 본인 vault 의 기존 노트 (`30. Permanent Notes/`, `Topics/` 등) 를 읽고 §1/§2 를 자동으로 채워줍니다. 그 결과는 `status: seeded` 로 표시됨 — 검토 후 `active` 로.
> 2. **직접 작성** — 자기소개·목적·철학을 아래 섹션에 직접 입력
> 3. **기존 기록에서 추출** — 이미 블로그·노트가 있다면, 그 글을 읽고 이 노트를 채워달라고 LLM 에게 요청
> 4. **STT 인터뷰** — 마이크로 자기소개 녹음 → LLM 에게 정리 요청

---

## 1. Who — 사용자 정체성

- **이름**: `{Your Name}`
- **직함 / 역할**: `{your current role(s)}`
- **전문 분야**: `{your domain(s)}`
- **주 활동 영역**: `{your working domain}`

### 연속성 선언 (Continuity Statement)

> "{현재 지식 관리 활동이 과거의 어떤 질문과 연결되는지 1~3 문장}"

**예시**:
> "나는 원래 A 를 연구하던 사람이다. 지금 B 를 말할 때도 내가 보는 것은 결국 A 다. C 는 A 를 더 잘 다루기 위한 도구의 진화일 뿐이다."

이 선언은 LLM 이 "왜 이 사람이 이 주제를 수집하는가" 의 깊이를 이해하는 앵커입니다.

---

## 2. Why — 지식을 수집하는 목적 (재활용 축)

**미래의 나에게 보내는 편지**: "이 소스가 아래 어느 축에 재활용될지" 를 수집 시점에 명시하지 못하면 수집하지 않습니다.

축은 5~9개 권장. 너무 적으면 모든 수집이 같은 축으로 쏠리고, 너무 많으면 축 자체가 무의미해집니다.

1. **`{축 1}`**: (예) 학술 연구 / 논문 · 학위
2. **`{축 2}`**: (예) 저술 · 출판
3. **`{축 3}`**: (예) 강의 · 강연
4. **`{축 4}`**: (예) 컨설팅 · 자문
5. **`{축 5}`**: (예) 제품 · 소프트웨어 개발
6. **`{축 6}`**: (예) 개인 에세이 · 브랜딩
7. **`{축 7}`**: (예) 커뮤니티 · 교육 자료

---

## 3. What — (옵션) 개인 지식 프레임워크

자체 지식 관리 프레임워크가 있다면 여기 기록. 없다면 비워도 OK.

**예시 구조**:
- 지식 생애주기 단계 (예: Connect → Merge → Develop → Share)
- 카테고리 체계 (예: 100 Themes / 200 Literature / ... / 900 Divisions)

---

## 4. How — (옵션) 지식 시스템 철학

LLM 이 정리 과정에서 따라야 할 사용자의 원칙·manifesto. 본인 에세이/블로그에서 핵심 3~5개로 요약.

**예시 (참고용)**:
- 스키마가 문서보다 먼저다 — Retrieval 은 구조 위에서 작동한다
- Harness 설계가 경쟁력이다 — 모델보다 harness 에 투자
- 암묵지 외재화가 AI-Ready 볼트의 본질이다

각 원칙은 LLM 이 ingest 시 "이 수집이 내 철학과 어떻게 정렬되는가" 를 판단하는 기준입니다.

---

## 5. Operational Directives (LLM 행동 규칙)

### Ingest 시
1. `/cmds-llm-wiki-ingest` 는 반드시 "왜 수집했는가?" 를 1회 묻고 §2 축 중 하나에 매핑한다.
2. Source frontmatter `collectionPurpose` 에 사용자 답변을 verbatim 기록.

### Query 시
1. 답변이 §2 어느 축에 연결되는지 명시 — `이 답변은 {axis}에 활용 가능합니다`.
2. 모든 주장에 `[[wikilink]]` 인용.

### Lint 시
- Source 에 `collectionPurpose` 누락 → flag.
- 본 Core Context `snapshot_date` 가 180 일 이상 → re-snapshot 추천.

---

## 6. 채우고 나서

- [ ] §1 정체성 채움
- [ ] §2 재활용 축 5~9개 정의
- [ ] (옵션) §3 개인 프레임워크
- [ ] (옵션) §4 철학 3~5개
- [ ] frontmatter `status: template` → `status: active`
- [ ] frontmatter `snapshot_date` 오늘 날짜
- [ ] frontmatter `author` 본인 이름

완료 후 첫 `/cmds-llm-wiki-ingest` 를 실행해보세요. Core Context 가 작동하면 LLM 이 §2 축을 언급하며 수집 목적 질문을 던집니다.

---

## 7. Related

- [[index]] — Master Index
- [[log]] — Change Log

---

*템플릿 v1.0 — Karpathy LLM Wiki pattern, lightweight in-vault edition*
