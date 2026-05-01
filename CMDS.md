---
type: documentation
aliases:
  - CMDS Context Guide
  - System Philosophy
description: "Context and philosophy guide for all LLM assistants working with this CMDS starter vault. Explains system purpose, vault operator profile (placeholder until WELCOME ritual fills it in), 9 categories (100-900), and the Connect→Merge→Develop→Share process. Reference first when starting a new conversation about this vault."
author:
  - "[[Me]]"
date created: 2025-10-22T21:52
date modified: 2026-04-28
tags:
  - CMDS
  - system
audience: All LLM assistants
scope: context-philosophy
precedence: 3
memory-type: user
required-for:
  - context-understanding
  - new-conversation
optional-for:
  - code-generation
  - file-editing
token-estimate: 8500
CMDS: "[[📚 601 Knowledge Management]]"
index: "[[🏛 CMDS Head Quarter]]"
version: "2.3"
status: completed
changelog:
  - "2.3 (2026-04-28): Starter vault 적응 — 운영자 프로필 placeholder 화, 개인 식별 정보 제거"
  - "2.2 (2026-04-07): 필수 프로퍼티 7개 반영 (description 추가, English required)"
  - "2.1 (2026-04-01): precedence/memory-type/required-for/token-estimate 추가"
  - "2.0 (2026-03-15): 전면 리뷰, 통계 갱신, AI Tools 업데이트"
---

> **🔄 Last Updated: 2026-04-28** | Upstream reference: [system.cmdspace.work](https://system.cmdspace.work) (canonical CMDS conventions by 구요한 / Yohan Koo)

# CMDS.md

This file provides LLM assistants with essential context about the CMDS (커맨드스페이스) Personal Knowledge Management system. The CMDS framework was created by 구요한 (Yohan Koo); this document describes how the framework applies to **your** vault.

## Essential (Post-Compact)

> 컨텍스트 압축 후에도 반드시 기억해야 할 핵심 컨텍스트:
> 1. **CMDS Process**: Connect → Merge → Develop → Share (지식 생애주기)
> 2. **Vault operator** (이 볼트의 사용자): 시작 시점에는 `[[Me]]` placeholder. WELCOME ritual 후 본인 정보로 채워짐.
> 3. **9개 카테고리**: 100 Themes → 200 Literature → 300 Data → 400 Methods → 500 Products → 600 Specialties → 700 Creatives → 800 Outputs → 900 Divisions
> 4. **Author 표기**: 시스템 파일과 새 노트는 모두 `author: [[Me]]` 로 시작. 본인 이름으로 일괄 치환은 [[WELCOME]] 절차 참조.
> 5. **기술 규칙**: [[CLAUDE]] (precedence 1) 또는 [[AGENTS]] (precedence 2) 참조

<!-- STATIC: 아래 시스템 구조와 철학은 거의 변경되지 않습니다 -->

---

## System Documentation Overview

This vault has **5 core system files** that complement each other. You are currently reading the **context guide**.

### The 5 Core Files

**🤖 AI Documents** (loaded into context window):

| File                    | Your Use Case                          | Key Content                                      |
| ----------------------- | -------------------------------------- | ------------------------------------------------ |
| **CMDS.md** (this file) | Understanding WHY & WHAT               | Operator profile, system philosophy, workflows   |
| **CLAUDE.md**           | Technical implementation (Claude Code) | Claude Code specific rules, commands             |
| **AGENTS.md**           | Technical implementation (Other AI)    | Gemini CLI, Codex, Cursor, etc.                  |

**👤 Human Documents** (referenced in Obsidian):

| File                        | Your Use Case      | Key Content                         |
| --------------------------- | ------------------ | ----------------------------------- |
| **🏛 CMDS Head Quarter.md** | Quick navigation   | 91 category links                   |
| **🏛 CMDS Guide.md**        | Standards reference | Properties templates, naming rules  |

### When to Reference Each File

**Start here (CMDS.md) when**:
- First time working with this vault
- Need to understand the operator's work context
- Want to know the PURPOSE of each category (100-900)
- Learning about CMDS Process (Connect → Merge → Develop → Share)

**Reference CLAUDE.md when**:
- Claude Code is writing or modifying code
- Need Claude-specific technical specs

**Reference AGENTS.md when**:
- Other AI coding agents (Gemini CLI, Codex) working with vault
- Need general technical specs without Claude-specific content

**Reference 🏛 CMDS Head Quarter.md when**:
- Need the full category structure at a glance

**Reference 🏛 CMDS Guide.md when**:
- Creating new notes (need Properties template)
- Checking standard note types or naming conventions

### Quick Decision Tree

```
Are you trying to...
├─ Understand the system? → CMDS.md (you are here)
├─ Write code (Claude Code)? → CLAUDE.md
├─ Write code (Other AI)? → AGENTS.md
├─ Navigate to a category? → 🏛 CMDS Head Quarter.md
└─ Check standards/templates? → 🏛 CMDS Guide.md
```

**This file provides the "story" behind the system. For technical "how-to", see CLAUDE.md or AGENTS.md.**

---

## Working Environments & Sync (선택)

<!-- TODO: 본인 환경에 맞춰 채울 것

| 환경 | 기기 | Base Path |
|------|------|-----------|
| Primary | (your machine) | `~/Documents/cmds-vault` |

다중 머신 사용 시:
- Obsidian Sync (공식) 또는 iCloud / Dropbox / Syncthing 등으로 동기화
- AI 코딩 결과물의 출처 분리는 `00. Inbox/03. AI Agent/` 하위에 머신/에이전트별 서브폴더(`03-1` ~ `03-4`)를 두어 추적
-->

---

## What is CMDS?

**CMDS (커맨드스페이스)** is a comprehensive Personal Knowledge Management (PKM) system built on Obsidian, designed to transform raw information into actionable knowledge and creative outputs. It's not just a filing system—it's a living ecosystem where ideas connect, merge, develop, and share.

The CMDS framework was developed by **구요한 (Yohan Koo)** through 3+ years of running a 10,000+ note vault. The canonical conventions live at [system.cmdspace.work](https://system.cmdspace.work). This starter vault is a class-friendly graft of those conventions.

### Core Philosophy

1. **Knowledge as a Network**: Every note is a node in an interconnected web of knowledge
2. **Process-Driven**: Knowledge flows through distinct stages (Connect → Merge → Develop → Share)
3. **AI-Enhanced**: Integrated with multiple AI tools (ChatGPT, Claude, Midjourney, etc.)
4. **Output-Focused**: Knowledge exists to be transformed into tangible outputs (research, lectures, consulting, creative works)
5. **Personal yet Structured**: Flexible enough for creativity, structured enough for productivity

---

## The Vault Operator: (Your Name)

> **Status**: Placeholder until WELCOME ritual is run. The operator's profile below is template text — replace it during onboarding.

<!-- TODO: 온보딩 시 본인 정보로 교체

### Professional Identity (예시 형식)

- **Role**: (학생 / 연구자 / 전문가 / 개인 사업자 / etc.)
- **Primary work**: (현재 시간을 가장 많이 쓰는 활동)
- **Background**: (학력, 경력 — 한 줄 요약)
- **Areas of expertise**: (전문 분야 1-3개)

### Current Focus Areas (1-4개 권장)

지금 깊이 파고드는 주제. 노트가 가장 활발하게 생성될 영역.

1. (focus area 1)
2. (focus area 2)
3. (...)

### Primary Activities

- (주활동 1 — 예: 회사 업무, 박사 연구, 콘텐츠 제작 등)
- (주활동 2)
- (...)

### Why this matters for AI assistants

이 섹션이 채워지면 LLM이 "사용자가 X를 물었을 때 이 사람의 직업과 관심사를 고려해 답해야겠다"고 더 잘 판단합니다. 비어있으면 LLM이 일반 답변만 하게 됩니다.

-->

---

## CMDS Architecture: 9 Categories (100-900 Series)

The CMDS system organizes all knowledge into 9 major categories, each representing a distinct stage or aspect of the knowledge lifecycle.

### 📖 100 Themes — Discovery & Connection
**Purpose**: Capture emerging interests, topics, variables, and terminologies
**Contains**:
- 📚 101 Interests — Personal and professional interests
- 📚 102 Topics — Subjects being explored
- 📚 103 Variables — Research variables, concepts to operationalize
- 📚 104 Terminologies — Definitions and vocabulary

**Role in Workflow**: This is where curiosity lives. New ideas, unfamiliar terms, and potential research topics are captured here before they mature into full concepts.

### 📖 200 Literature — Integration & Theory
**Purpose**: Integrate knowledge from external sources into personal understanding
**Contains**:
- 📚 201 Concepts — Core conceptual frameworks
- 📚 202 Frameworks — Theoretical frameworks and models
- 📚 203 Models — Analytical and conceptual models
- 📚 204 Theories — Established theories
- 📚 205 Classics — Foundational texts and seminal works
- 📚 210 Literature Reviews — Academic literature synthesis
- 📚 220 Personal Insights — Original interpretations and connections
- 📚 240 Books — Book notes and reviews
- 📚 290 Bible — Biblical texts and theology
- 📚 291 Sermon — Sermon notes and spiritual reflections

**Role in Workflow**: Raw ideas from 100 Themes are enriched with literature, transformed into robust theoretical foundations. This is where learning happens.

### 📖 300 Data — Collection & Management
**Purpose**: Manage research data, surveys, and information systems
**Contains**:
- 📚 301 Scale Development and Validation
- 📚 302 Questionnaires — Survey instruments
- 📚 303 Panel Data — Longitudinal data
- 📚 310 Data Management — Data organization and workflows
- 📚 311 Database Systems — Database design and implementation
- 📚 330 Learning Management Systems — LMS platforms and usage

**Role in Workflow**: Theoretical knowledge from 200 Literature is operationalized into measurable data. This is where theory meets empirical reality.

### 📖 400 Methodologies — Analysis & Implementation
**Purpose**: Apply research methods, statistical techniques, and analytical approaches
**Contains**:
- 📚 401 Research Methods — Research design principles
- 📚 402 Quantitative Research
- 📚 403 Experimental Research
- 📚 404 Qualitative Research
- 📚 405 Mixed Methods
- 📚 410 Statistical Inference
- 📚 411 Regression Analysis
- 📚 412 Causal Inference
- 📚 420 Machine Learning
- 📚 421 Time Series Analysis
- 📚 422 Deep Learning
- 📚 423 Predictive Analytics
- 📚 490 Syntax — Statistical software syntax
- 📚 491 Codes — Programming code snippets
- 📚 492 Prompts — AI prompts and templates
- 📚 493 Scripts — Automation scripts

**Role in Workflow**: Data from 300 is analyzed using appropriate methods. This is where insights are generated through systematic analysis.

### 📖 500 Products — Tools & Platforms
**Purpose**: Master and leverage productivity tools and AI platforms
**Contains**:
- 📚 501 Obsidian — PKM system mastery
- 📚 502 Notion — Project management
- 📚 510 DevonThink — Document management
- 📚 520 ChatGPT — AI assistance and automation
- 📚 521 Claude — AI writing and analysis
- 📚 522 Gemini — Google AI tools
- 📚 523 LLaMa — Open-source LLMs
- 📚 530 Midjourney — AI image generation
- 📚 531 Stable Diffusion — Image AI
- 📚 541 n8n — Workflow automation

**Role in Workflow**: Tools are not just used—they are studied, mastered, and integrated into workflows. This category captures tool knowledge and best practices.

### 📖 600 Specialties — Expertise & Application
**Purpose**: Develop deep expertise in specialized domains
**Contains**:
- 📚 601 Knowledge Management — PKM theory and practice
- 📚 603 Second Brain — Building a Second Brain methodology
- 📚 604 ZettelKasten — Zettelkasten method
- 📚 610 Productivity — Personal productivity systems
- 📚 620 Generative AI — AI applications and education
- 📚 630 Development — Software development
- 📚 651 Physical Health — Exercise and wellness
- 📚 652 Mental Health — Psychology and well-being
- 📚 653 Biohacking — Performance optimization
- 📚 680 Educations — Educational theory and practice
- 📚 690 Spirituality — Faith and spiritual growth

**Role in Workflow**: This is where the operator develops and maintains professional expertise. It's a combination of theory (200), methods (400), and practical experience.

### 📖 700 Creatives — Expression & Content
**Purpose**: Create and distribute creative content across multiple platforms
**Contains**:
- 📚 701 YouTube — Video content creation
- 📚 710 SNS — Social media content
- 📚 720 Music — Music composition and production
- 📚 721 Jazz — Jazz theory and performance
- 📚 730 Images — Visual content
- 📚 731 Digital Art and Design — AI-generated art, design work

**Role in Workflow**: Knowledge and expertise are transformed into creative expressions. This is where ideas become content.

### 📖 800 Outputs — Publication & Delivery
**Purpose**: Produce and deliver formal outputs (academic, professional, educational)
**Contains**:
- 📚 801 PhD — Doctoral dissertation and research
- 📚 802 Articles — Published articles and essays
- 📚 803 Books — Book manuscripts
- 📚 804 Community — Community building and engagement
- 📚 805 Group Study — Study groups and cohorts
- 📚 806 Webpages — Web content and sites
- 📚 820 Research — Research projects
- 📚 821 Academic Journals — Journal publications
- 📚 822 Conference Presentations — Academic presentations
- 📚 830 Projects — Client projects
- 📚 831 Consulting — Consulting deliverables
- 📚 840 Lectures — Teaching materials
- 📚 841 Curriculum — Course design
- 📚 842 Course Development and Resources — Educational resources
- 📚 843 Class Administration and Management — Teaching operations

**Role in Workflow**: This is the ultimate destination—where all prior work (Connect, Merge, Develop) culminates in tangible outputs that serve others.

### 📖 900 Divisions — Operations & Management
**Purpose**: Organize and manage the operational structure of the operator's professional activities
**Contains**:
- 📚 901 Knowledge Management & Research Division
- 📚 902 Writing & Publishing Division
- 📚 903 Teaching & Curriculum Division
- 📚 904 Creative Arts & Media Division
- 📚 905 Research Methods & Analytics Division
- 📚 906 Partnerships & Networks Division
- 📚 907 Product & Engineering Division
- 📚 908 Events & Community Engagement Division
- 📚 909 Consulting & Advisory Division

**Role in Workflow**: Meta-organizational layer that maps the operator's work onto a recurring division structure. Customize subcategories as your professional structure evolves.

---

## CMDS Process: The Knowledge Lifecycle

The CMDS framework is not just a filing system—it's a **process** that guides knowledge through four distinct stages.

### 🔗 Connect — Idea Discovery (100 Themes)
**What happens**: Encounter new ideas, capture interests, identify gaps
**Questions to ask**:
- What am I curious about?
- What terminology do I need to learn?
- What topics are emerging in my field?
- What variables matter for my research?

**Outputs**: Notes in 100 Themes (interests, topics, variables, terminologies)

### 🔀 Merge — Knowledge Integration (200 Literature)
**What happens**: Read literature, connect ideas, build theoretical frameworks
**Questions to ask**:
- How does this concept relate to what I already know?
- What do scholars say about this topic?
- What frameworks exist to explain this phenomenon?
- What are my own insights and interpretations?

**Outputs**: Literature notes, concept maps, theoretical frameworks, personal insights

### 🛠 Develop — Application & Creation (300-600)
**What happens**: Collect data, apply methods, use tools, build expertise
**Questions to ask**:
- What data do I need?
- Which methods are appropriate?
- What tools will help me execute?
- How do I deepen my expertise in this area?

**Outputs**: Datasets, analysis scripts, tool mastery notes, domain expertise

### 📤 Share — Output & Impact (700-800)
**What happens**: Create content, publish research, teach, consult, serve others
**Questions to ask**:
- How can I share this knowledge?
- Who needs this information?
- What format will be most impactful?
- How can I help others learn and grow?

**Outputs**: YouTube videos, articles, research papers, lectures, consulting projects, creative works

---

## Note Hierarchy & Navigation

### Hierarchical Structure
```
🏛 Home/Guide (최상위)
└── 📖 1st Level CMDS (100-900 시리즈)
    └── 📚 2nd Level CMDS (N01-N99)
        └── (No Icon) 3rd Level Notes (세부 주제)
```

### Key Hub Notes
- **[[🏛 CMDS Head Quarter]]** — Central navigation hub, links to all 9 categories
- **[[🏛 CMDS Guide]]** — Properties standards, naming conventions, operational guidelines

### Index Notes (🏷)
Index notes aggregate related content across categories:
- [[🏷 Daily Notes]] — Daily journal entries
- [[🏷 Meeting Notes]] — Meeting minutes
- [[🏷 Research Notes]] — Research documentation
- [[🏷 Lecture Notes]] — Teaching materials
- [[🏷 People]] — People profiles
- [[🏷 Prompts]] — AI prompt library
- [[🏷 Syntax and Codes]] — Code snippets

(These are conventions — actual 🏷 notes you create as you go.)

---

## Note Properties & Metadata

Every note in CMDS contains structured metadata that enables powerful queries and connections.

### Required Properties (7 fields)
```yaml
---
type:           # Note category (see types below)
aliases: []     # Alternative names
description: "" # English 1-2 sentence summary for LLMs (always double-quoted)
author:
  - "[[Me]]"  # Replace with your name during WELCOME ritual
date created:   # YYYY-MM-DD
date modified:  # YYYY-MM-DD
tags: []        # Topical tags
---
```

> **`description` field** (added 2026-04-07): Must be in English, 1-2 sentences, skill-description style. Explains what the note contains AND when an LLM should reference it. This is a machine-readable relevance hint for AI agents working across the vault. Always wrap in double quotes.

### Common Note Types

**Content Types**:
- `note` — General knowledge notes
- `terminology` — Term definitions
- `research-pipeline` — Research pipeline documents
- `manuscript` — Manuscripts and drafts
- `books` — Book notes and reviews
- `article` — Articles and essays
- `research-review` — Literature reviews
- `sermon` — Spiritual reflections

**Structural Types**:
- `CMDS` — Category index pages (replaces traditional MOC concept)
- `moc` — Map of Content
- `api` — API documentation
- `index` — Collection pages

**Activity Types**:
- `meeting` — Meeting minutes
- `people` — People profiles
- `curriculum` — Course curricula
- `channel` — YouTube/Blog/Newsletter 채널 프로필
- `project` — Project documentation

### Status Values
- `unread` — Not yet processed
- `reading` — Currently reading/processing
- `inProgress` — Active work in progress
- `completed` — Finished
- `archived` — Historical reference

---

## Workflow Patterns & Common Scenarios

### Research Workflow
1. **Discover** a research question → Capture in [[📚 102 Topics]]
2. **Define** key variables → Document in [[📚 103 Variables]]
3. **Review** literature → Create notes in [[📚 210 Literature Reviews]]
4. **Design** study → Plan in [[📚 401 Research Methods]]
5. **Collect** data → Manage in [[📚 310 Data Management]]
6. **Analyze** → Apply methods from [[📚 410 Statistical Inference]]
7. **Write** → Draft in [[📚 821 Academic Journals]]
8. **Present** → Prepare in [[📚 822 Conference Presentations]]

### Teaching Workflow
1. **Design** curriculum → Create in [[📚 841 Curriculum]]
2. **Develop** resources → Build in [[📚 842 Course Development and Resources]]
3. **Prepare** lectures → Store in [[📚 840 Lectures]]
4. **Teach** → Document in [[🏷 Daily Notes]]
5. **Reflect** → Write insights in [[📚 220 Personal Insights]]

### Consulting Workflow
1. **Meet** with client → Record in [[🏷 Meeting Notes]]
2. **Research** client's needs → Reference [[📚 601 Knowledge Management]] or [[📚 620 Generative AI]]
3. **Design** solution → Draft in [[📚 831 Consulting]]
4. **Deliver** → Present and document in [[📚 830 Projects]]
5. **Follow up** → Track in `60. Collections/63. Meetings/`

### Content Creation Workflow
1. **Identify** topic from [[📚 102 Topics]] or [[📚 220 Personal Insights]]
2. **Research** using [[📖 200 Literature]] notes
3. **Script** content using [[📚 492 Prompts]] and AI tools
4. **Create** in appropriate platform (YouTube, article, etc.)
5. **Publish** and document in [[📚 701 YouTube]] or [[📚 802 Articles]]

### Development Workflow
1. **Plan** feature or tool → Design in [[📚 630 Development]]
2. **Build** with Claude Code → Output to `00. Inbox/03. AI Agent/`
3. **Test** and iterate → Reference [[📚 491 Codes]] or [[📚 493 Scripts]]
4. **Deploy** → Document in [[📚 806 Webpages]] or [[📚 830 Projects]]
5. **Maintain** → Track in skills, plugins, or automation workflows

---

## AI Integration in CMDS

### AI Tools Commonly Used

- **Claude Code**: Code generation, vault automation, writing assistance, slash commands
- **ChatGPT** (Custom GPTs): Knowledge work, reasoning, analysis
- **Gemini CLI**: Cross-validation, web search integration
- **Midjourney / Stable Diffusion**: AI image generation
- **n8n / Make.com**: Workflow automation
- **Obsidian AI Plugins**: Copilot, Smart Connections, Smart Composer

> 위 도구들은 권장이지 강제가 아님. 본인이 쓰는 AI 스택에 맞춰 조정하세요.

### Custom AI Assistants (선택)

<!-- TODO: 본인이 만든/사용하는 커스텀 GPT, Custom Claude Project, Gemini Gem 등을 기록

예시:
- **My Research Helper** — 논문 분석 전용 GPT
- **My Daily Note GPT** — 일일 노트 정리 보조
-->

### AI-Generated Content
- **Prompts Library**: [[📚 492 Prompts]] — Reusable prompt templates
- **Code Snippets**: [[📚 491 Codes]] — AI-generated and human-curated code
- **Agent Settings**: `.claude/{agents,commands,rules,skills}/` 가 default 위치. Multi-machine sync 시 `90. Settings/94. Agent Settings/claude/` 를 원본으로 두고 symlink 권장.

---

## Key Directories & Their Roles

### 00. Inbox/ — Processing Area
**Purpose**: Temporary storage for new inputs before they're processed into the CMDS system
- `01. Daily Notes/` — Daily reflections and logs (with 01-1. Planners, 01-2. Weekly Notes)
- `02. Clippings/` — Web clippings (with 02-1. Literature Notes)
- `03. AI Agent/` — **PRIMARY WORKING DIRECTORY** for all AI coding outputs
- `04. Excalidraw/` — Visual diagrams
- `05. Canvas/` — Canvas notes
- `06. Automation/` — Automation workflows
- `07. App Sync/` — External app sync
- `08. Unlisted/` — Unlisted items
- `09. Legacy/` — Legacy and archived content

**Workflow**: Items in Inbox are temporary. They should be processed and moved to appropriate CMDS categories.

### 10. CMDS Process/ — Process Documentation
Documents the **Connect → Merge → Develop → Share** workflow itself
- `11. Connect/` — Capturing and connecting ideas
- `12. Merge/` — Integrating knowledge
- `13. Develop/` — Building and creating
- `14. Share/` — Publishing and sharing

### 20. Literature Notes/ — Reading Notes
Notes from books, articles, papers (usually migrate to [[📖 200 Literature]] categories)

### 30. Permanent Notes/ — Evergreen Content
Fully developed, timeless notes that represent mature knowledge

### 40. Docs/ — Technical Documentation
Central repository for technical documents and guides

### 50. Assets/ — Reusable Resources
Reusable resources, templates, and media assets

### 60. Collections/ — Entity Management
- `61. People/`, `62. Organization/`, `63. Meetings/`, `69. Preferences/`, etc.

### 70. Outputs/ — Final Deliverables
- `71. Published/`, `72. Presentations/`, `73. Courses/`, `74. Projects/`, `75. Consulting/`, `79. Portfolio/`

### 80. References/ — External Materials
Attachments, web articles, Zotero references, books

### 90. Settings/ — System Configuration
- `91. Skills/` — User-installed skills (gobi-onboarding, gobi-cli 등)
- `92. Prompts/` — Prompt library (CBH 등)
- `94. Agent Settings/` — AI agent configs (claude/{commands,rules,skills,agents})

---

## Common Terminology & Concepts

### PKM Terms
- **Second Brain**: External system for storing and organizing knowledge (Tiago Forte's methodology)
- **Zettelkasten**: Note-taking method focused on atomic notes and connections
- **Evergreen Notes**: Timeless, fully developed notes that don't decay
- **CMDS Index**: Category index pages that organize related notes (replaces traditional MOC concept in this vault)
- **Atomic Notes**: Small, focused notes on single concepts
- **Progressive Summarization**: Highlighting and condensing information in stages

### CMDS-Specific Terms
- **CMDS Process**: Connect → Merge → Develop → Share workflow
- **Space Collection**: First-level CMDS categories (100-900)
- **Spaces**: Second-level CMDS categories (N01-N99)
- **Hub Notes**: 🏛 notes that serve as navigation centers
- **Index Notes**: 🏷 notes that aggregate related content

### File Prefix Meanings
- 📎 — Web Clips (captured from web)
- 🏷 — Index pages (collections)
- 📦 — Reviews (analyzed content)
- 🔖 — Personal outputs (your original ideas)
- 📜 — Others' outputs (curated external content)
- 📈 — Code and syntax (technical content)
- 🎹 — Music (compositions, theory)
- 📘 — Books and references

---

## Understanding User Intent

When the operator asks an LLM to work with this vault, frame the response with the operator's profile (`(Your Name)` section above) in mind.

### Research Context
- Reference relevant literature ([[📖 200 Literature]]) and methodological approaches ([[📖 400 Methodologies]])
- Outputs typically become **manuscripts, decks, or articles** depending on operator's role

### Teaching Context
- Reference curriculum designs ([[📚 841 Curriculum]])
- Link to relevant subject expertise ([[📖 600 Specialties]])
- Consider student learning outcomes ([[📚 842 Course Development and Resources]])

### Consulting Context
- Document in meetings (`60. Collections/63. Meetings/`)
- Connect to relevant expertise ([[📚 831 Consulting]])
- Reference applicable frameworks ([[📖 200 Literature]])

### Content Creation Context
- Identify target platform ([[📚 701 YouTube]], [[📚 802 Articles]], etc.)
- Reference source knowledge ([[📖 200 Literature]], [[📖 600 Specialties]])
- Use prompt templates ([[📚 492 Prompts]])

### Knowledge Management Context
- Reference [[🏛 CMDS Guide]] for standards
- Consider [[📚 601 Knowledge Management]] best practices
- Apply Second Brain principles ([[📚 603 Second Brain]])

---

## Working with the CMDS System

### When Creating New Notes
1. Determine the **CMDS category** (100-900 series) based on content type
2. Use appropriate **note type** (note, meeting, curriculum, etc.)
3. Add required **properties** (type, aliases, description, author, date created, date modified, tags)
4. Link to relevant **index notes** (🏷)
5. Reference related **CMDS categories**
6. Create **backlinks** to related notes

### When Organizing Information
- **Connect Stage** → Capture in [[📖 100 Themes]]
- **Merge Stage** → Integrate into [[📖 200 Literature]]
- **Develop Stage** → Apply in [[📖 300 Data]] through [[📖 600 Specialties]]
- **Share Stage** → Output via [[📖 700 Creatives]] or [[📖 800 Outputs]]

### Command Suite: CMDS Process as Operational Verbs (2026-04-14+)

The CMDS Process is the **operational vocabulary** of the vault via 8 slash commands. Each stage has a matching command:

| CMDS Process Stage | Command | What it does |
|-------------------|---------|--------------|
| 🔗 **Connect** | `/connect` | Capture inbox items into `📖 100 Themes` as stubs. Auto-classifies type. Low-friction. |
| 🔀 **Merge** | `/merge` | Synthesize N notes into 1 `📖 200 Literature` note. Multi-dialog. The heaviest command. |
| 🛠 **Develop** | `/develop` | Apply methodology, build artifact (code, prompt, curriculum). Outputs to `00. Inbox/03. AI Agent/` first. |
| 📤 **Share** | `/share` | Orchestrate existing skills to produce 700-800 outputs. |

Plus cross-cutting utilities (`/inbox`, `/lint`, `/query`, `/status`).

**Why this matters philosophically**: The CMDS Process is more than a filing framework — with commands, it becomes an **interactive cognitive scaffold**. Asking "이걸 connect할까, merge할까?" is the first metacognitive step of any session, sharpening what the work actually is.

**Typical session patterns**:
- **Daily**: `/status` → `/inbox` → (`/connect` or `/merge`)
- **Weekly**: `/lint inbox` → `/merge {topic}` → `/share` (if applicable)
- **Project work**: `/query {topic}` → `/merge {topic}` → `/develop` or `/share`

> For command implementation details, see [[CLAUDE]] "CMDS Process Command Suite (2026-04-14+)" section. Command source files live in `.claude/commands/`.

### When Searching for Context
Look for relevant notes in:
1. **Index pages** (🏷) — Aggregated collections
2. **Hub pages** (🏛) — Main navigation
3. **CMDS categories** (📖, 📚) — Topical organization
4. **Daily/Weekly notes** — Temporal context
5. **Meeting notes** — Project context
6. **People notes** — Relationship context

---

<!-- DYNAMIC: 아래 통계와 도구 목록은 주기적으로 갱신됩니다 -->

## Vault Statistics

> 처음 시작하면 노트 수는 0~수십 개. 사용하면서 자연스럽게 늘어나는 숫자입니다. 일정 단계마다 본인 통계를 여기에 기록해도 좋음.

<!-- TODO: 정기적으로 업데이트 (예: 매월 1일)

- **Total Notes**: ~N개 (as of YYYY-MM-DD)
- **Note Types**: <type> N개, ...
- **Years Active**: ~ N년
-->

---

## Guiding Principles

1. **Every note has a home**: All knowledge belongs somewhere in the 100-900 system
2. **Links create value**: Isolated notes are less useful than connected notes
3. **Process matters**: Knowledge flows through Connect → Merge → Develop → Share
4. **Output is the goal**: Knowledge exists to serve others through outputs
5. **AI is a partner**: AI tools enhance but don't replace human thinking
6. **Standards enable freedom**: Consistent structure allows creative flexibility
7. **Evolution over perfection**: The system grows and adapts continuously

---

## Quick Reference: When to Use Which Category

| If you're working with... | Use Category... | Subcategory Examples |
|---------------------------|-----------------|---------------------|
| New ideas, emerging topics | 📖 100 Themes | 102 Topics, 103 Variables |
| Books, papers, theories | 📖 200 Literature | 210 Literature Reviews, 240 Books |
| Survey data, datasets | 📖 300 Data | 302 Questionnaires, 310 Data Management |
| Analysis methods, code | 📖 400 Methodologies | 420 Machine Learning, 491 Codes, 492 Prompts |
| Software tools, AI platforms | 📖 500 Products | 501 Obsidian, 520 ChatGPT, 521 Claude |
| Domain expertise, skills | 📖 600 Specialties | 601 Knowledge Management, 620 Generative AI |
| Creative content | 📖 700 Creatives | 701 YouTube, 720 Music |
| Publications, deliverables | 📖 800 Outputs | 801 PhD, 840 Lectures, 831 Consulting |
| Business operations | 📖 900 Divisions | 901-909 (specific divisions) |

---

**Remember**: CMDS is not just a filing system—it's a **thinking environment** for developing ideas, conducting research, creating content, and serving others.

**For technical implementation details, file operations, and coding guidelines, see [[CLAUDE]].**
