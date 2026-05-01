# Interview Question Bank — cmds-onboarding

Extended question pool. The main `SKILL.md` ships with 12 default questions in 5 batches (A–E). This file holds *domain-flavored variants* the agent can swap in when it has signal about the user's role.

## When to use this file

The agent reads this file *only when*:
- User answers Batch B Q4 with a specific role (researcher / executive / creator / student / engineer)
- Agent wants to refine remaining batches with role-tuned wording

Otherwise the default questions in `SKILL.md` are enough.

## Variants by Domain

### 🎓 Researcher (academic / industrial R&D)

**Replace Batch C Q7 with**:
- "What's the longest research thread you've maintained — months / years? Where do its notes currently live?"
- "Pick one paper you read in the last year that you wish you'd taken better notes on. What would those notes have looked like?"

**Add to Batch B**:
- "What citation manager do you use? (Bookends / Zotero / Mendeley / EndNote / nothing)"
- "Do you co-author? How are notes shared between collaborators today?"

**Add to Batch D**:
- "Are you working on a paper / dissertation / book chapter right now? What's the working title?"

### 👔 Executive / Manager / Consultant

**Replace Batch B Q5 with**:
- "Which decisions do you make weekly that you wish you had better historical context for?"

**Add to Batch C**:
- "What kinds of meetings do you spend most time in? (1:1 / team / board / external)"
- "After a meeting, what do you typically lose track of within 3 days?"

**Add to Batch D**:
- "Are you preparing a public talk, board presentation, or strategic memo in the next 12 weeks?"

### 🎨 Creator / Newsletter / YouTuber / Speaker

**Replace Batch C Q8 with**:
- "What's your current publishing rhythm? (daily / weekly / monthly / when-inspired)"

**Add to Batch D**:
- "What's your newsletter / channel / show / book about?"
- "What format do you publish in? (essay / video / podcast / twitter thread / mixed)"

**Add to Batch E**:
- "Who's your audience in 1 sentence? Strangers, peers, fans?"

### 🎓 Student (undergrad / grad / self-learner)

**Replace Batch B Q4 with**:
- "What are you studying — formally or informally? What courses or topics this semester?"

**Add to Batch C**:
- "Which lectures or readings do you find yourself revisiting? Why?"
- "What's your current note-taking workflow during class? (laptop / paper / hybrid)"

**Add to Batch D**:
- "Goal: better grades / deeper understanding / portfolio / job prep / curiosity?"

### 💻 Engineer / Developer

**Replace Batch B Q6 with**:
- "What 2–3 systems / repos / frameworks are you most active in?"

**Add to Batch C**:
- "What kinds of context do you find yourself googling repeatedly? (API docs / past commits / past meetings / your own old code)"
- "Where do you currently keep technical decisions? (commit messages / docs / your head / nowhere)"

**Add to Batch D**:
- "Working on a side project, OSS contribution, or job change?"

## Voice Mode — Compressed Questions

When voice mode is active, replace 12 default questions with these 5:

1. "도메인 한 줄로?"  (Batch B compressed)
2. "지금 가장 잃기 싫은 정보 하나?" (Batch C compressed)
3. "12주 후 뭘 만들고 싶으세요?" (Batch D compressed)
4. "주로 누가 읽나요? 어떤 톤?" (Batch E compressed)
5. "지금 안 쓰는 도구 중에 옮길 만한 게 있나요?" (Batch A compressed)

## Anti-patterns — Questions to AVOID

- ❌ "Tell me everything about yourself" → too open, paralysis
- ❌ "What's your goal in life?" → too philosophical for 15-min onboarding
- ❌ "Write 5 paragraphs about your work" → user is here to *do less typing*, not more
- ❌ "How experienced are you with AI?" → answers vary wildly and don't change the flow much
- ❌ Yes/no questions → low information density. Prefer "what / how / where" open-ended.

## Question Quality Heuristics

A good interview question for cmds-onboarding:
- **Single subject** — one thing per question
- **Concrete answer possible in <30 seconds**
- **Answer maps to a frontmatter field or stub note**
- **Skippable** — user can pass without breaking the flow
- **In the user's working language** (Korean if Korean session)

## How the Agent Should Use This Bank

1. Default to SKILL.md's 12 questions
2. After Batch B Q4 (role), match user's answer to a domain variant above
3. Swap or add 2–3 questions from that variant in remaining batches
4. Keep total questions per turn ≤ 3 in voice mode, ≤ 4 in text mode
5. Always summarize back what the agent learned at end of each batch
