---
type: core-context
aliases:
  - User Context
  - 핵심 맥락
description: Pointer-only Core Context. Identity, reuse axes, frameworks, and philosophy live in canonical CMDS files (BRAIN, HQ, CMDS) and are dereferenced at command-time. Skill-local operational rules live in §5 below.
author:
  - "[[{your-name}]]"
date created: {YYYY-MM-DD}
date modified: {YYYY-MM-DD}
tags:
  - system
  - llm-wiki
  - core-context
version: "2.0"
snapshot_date: {YYYY-MM-DD}
status: template      # template (unfilled) | seeded (auto-pointed by /cmds-llm-wiki-status, awaiting review) | active (user-confirmed)
sourcesPath: "10. Raw Sources"   # CMDS-canonical raw-sources home; sources are MOVED here from 00. Inbox/ on ingest
---

# 🧭 Core Context — LLMWiki 사용자 맥락 (Pointer)

> **Pointer file**, not a snapshot. Identity / reuse axes / frameworks / philosophy live in canonical CMDS files; this note tells the skill **where to read them from** so we don't duplicate content.
>
> Bootstrapped automatically by `/cmds-llm-wiki-status`. Review the pointers below, adjust as needed, then flip `status: seeded` → `status: active`.
>
> If your vault is **not** CMDS-style (no `BRAIN.md`, `🏛 CMDS Head Quarter.md`, `CMDS.md`), the bootstrap falls back to inline content in §1/§2 — same shape as v1.0 of this template.

---

## 1. Who → see [[BRAIN]]

`BRAIN.md` at vault root holds the operator profile (name, role, focus, continuity statement). LLMWiki commands `Read("BRAIN.md")` once per session to ground identity.

If `BRAIN.md` doesn't exist, fill in here:
- **이름**: `{Your Name}`
- **직함 / 역할**: `{your current role(s)}`
- **전문 분야**: `{your domain(s)}`

---

## 2. Why — Reuse Axes

→ **Active focus** (changes over time): [[🏛 CMDS Head Quarter#Current Focus Areas]]
→ **Long-term taxonomy** (stable): [[CMDS]] (100–900 categories — `📚 N0N` headings define the durable reuse axes)

**미래의 나에게 보내는 편지**: every `/cmds-llm-wiki-ingest` asks "왜 수집했는가?" and the answer must map to one entry from the linked sources above (or to a long-term `📚 NNN` category from [[CMDS]]).

If neither HQ nor CMDS.md exists, fill in 5–9 axes here manually:
1. `{축 1}` — (예) 학술 연구
2. `{축 2}` — (예) 저술 · 출판
3. ... (5–9 total)

---

## 3. What — Frameworks → see [[CMDS]]

The CMDS process (Connect → Merge → Develop → Share) and 100–900 category system live in `CMDS.md`. LLMWiki uses these as the structural backbone — wiki pages classify into the same categories so they appear in `🏛 CMDS Head Quarter` navigation.

If you use a different framework, document it here:
- {your framework}

---

## 4. How — Philosophy → see [[CMDS#Philosophy]] and [[🏛 CMDS Guide]]

The user's manifesto / operating principles live in `CMDS.md` (philosophy section) and the operational standards in `🏛 CMDS Guide.md`. LLMWiki's bias-checking and contradiction-flagging defer to these.

---

## 5. Operational Directives (skill-local — keep here, do NOT externalize)

This section stays inline because it's LLMWiki-specific behavior, not vault-wide doctrine.

### Ingest

1. `/cmds-llm-wiki-ingest` 는 반드시 "왜 수집했는가?" 를 1회 묻고 §2 축 (HQ Focus Areas 또는 CMDS 카테고리) 중 하나에 매핑한다.
2. Raw source frontmatter `collectionPurpose` 에 사용자 답변을 verbatim 기록.
3. Sources go to `{sourcesPath}/{NN. category}/{YYYY-MM-DD}-{slug}.md` (frontmatter `sourcesPath` above; default `10. Raw Sources`). If the source originated from `00. Inbox/`, it is **MOVED** there — Inbox is intake, `10. Raw Sources/` is the immutable archive.
4. Wiki pages go to `{llmWikiPath}/Wiki/{Topic}.md`. `{llmWikiPath}` is read from this vault's `AGENTS.md` frontmatter (`llmWikiPath:` field).

### Query

1. 답변이 §2 어느 축에 연결되는지 명시 — `이 답변은 {axis}에 활용 가능합니다`.
2. 모든 주장에 `[[wikilink]]` 인용.

### Lint

- Raw source 에 `collectionPurpose` 누락 → flag.
- 본 Core Context `snapshot_date` 가 180 일 이상 → re-bootstrap 추천 (`/cmds-llm-wiki-status` 다시 실행).
- `status: seeded` 가 30 일 이상 review 안 됨 → flag.

---

## 6. After bootstrap

- [ ] Read the pointer targets ([[BRAIN]], [[🏛 CMDS Head Quarter]], [[CMDS]]) — do they reflect your current focus?
- [ ] If yes: flip frontmatter `status: seeded` → `status: active`
- [ ] If a pointer target is missing/empty: fill in the inline fallback in §1 or §2

Once `status: active`, every `/cmds-llm-wiki-ingest` and `/cmds-llm-wiki-query` will follow these pointers fresh — no manual snapshot maintenance needed.

---

## 7. Related

- [[BRAIN]] — operator profile (Who)
- [[🏛 CMDS Head Quarter]] — active focus + navigation hub
- [[CMDS]] — process + categories + philosophy
- [[🏛 CMDS Guide]] — operational standards
- [[index]] — LLMWiki master index
- [[log]] — LLMWiki change log

---

*Template v2.0 — Karpathy LLM Wiki pattern + CMDS-vault integration (pointer-based, dedup with canonical files)*
