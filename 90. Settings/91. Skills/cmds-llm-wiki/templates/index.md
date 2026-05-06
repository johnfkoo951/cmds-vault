---
type: documentation
aliases:
  - LLMWiki Index
  - 마스터 인덱스
description: One-liner catalog of every page in this LLMWiki. Read FIRST by every command — drives navigation. Auto-maintained by /cmds-llm-wiki-ingest, /cmds-llm-wiki-query, /cmds-llm-wiki-lint.
author:
  - "[[{your-name}]]"
date created: {YYYY-MM-DD}
date modified: {YYYY-MM-DD}
tags:
  - system
  - llm-wiki
  - index
status: active
---

# 🗂 LLMWiki — Master Index

> 이 파일은 모든 명령의 진입점입니다. `/cmds-llm-wiki-ingest`, `/cmds-llm-wiki-query`, `/cmds-llm-wiki-lint` 가 이 인덱스를 먼저 읽고 동작합니다.

---

## Stats

| Metric | Value |
|--------|-------|
| Sources | 0 |
| Wiki Pages | 0 (Concepts: 0, Entities: 0, Guides: 0, Maps: 0) |
| Queries | 0 |
| Last activity | — |

---

## Concepts

> 추상 개념·기법·패턴. 새 ingest 가 만들어내는 페이지 대부분이 여기에 속합니다.

_(empty — first ingest will populate)_

---

## Entities

> 사람·조직·제품·모델.

_(empty)_

---

## Guides

> How-to, 튜토리얼, 실전 가이드.

_(empty)_

---

## Maps

> 주제별 인덱스 (MOC). 페이지가 5+ 개 모이면 그 주제의 MOC 를 만드세요.

_(empty)_

---

## Queries

> 합성된 Q&A 결과. `/cmds-llm-wiki-query` 가 substantial 답변을 자동으로 여기 등록합니다.

_(empty)_

---

## Recent Ingests

| Date | Source | Pages | Purpose |
|------|--------|-------|---------|
| — | — | — | — |

---

## How this index is maintained

- `/cmds-llm-wiki-ingest` → adds new pages to the relevant section + updates Stats + Recent Ingests row
- `/cmds-llm-wiki-query` → adds substantial query results under `## Queries`
- `/cmds-llm-wiki-lint` → reconciles index against actual files; flags drift

If you edit pages by hand, run `/cmds-llm-wiki-lint` afterwards to keep this index honest.
