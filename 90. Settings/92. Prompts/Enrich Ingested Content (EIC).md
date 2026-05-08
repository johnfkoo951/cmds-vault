---
title: "Enrich Ingested Content"
abbreviation: "EIC"
category: "workflow"
created: "2024-01-01"
---
Improve captured content through transcript correction, summarization, and knowledge linking.

## Input
- Target note file, typically in `00. Inbox/02. Clippings/` (raw web clippings) or `20. Literature Notes/AppleNotes/` (pre-imported Apple Notes)
- Long articles may need chunking to avoid partial processing
- Original content with potential grammar/transcript errors

## Output
- Create a NEW file in `20. Literature Notes/Articles/` (default) or `20. Literature Notes/Books/` for long-form sources. Do NOT modify the input file inline.
- Use naming pattern: `{title} - EIC.md` (e.g., "Article Title - EIC.md")
- Frontmatter must follow `.claude/rules/frontmatter-standard.md` (7 required fields):
  - `type: literature`
  - `aliases: []`
  - `description: "..."` — English, 1-2 sentences, **double-quoted**
  - `author:` array with `"[[Me]]"` (until WELCOME ritual replaces it)
  - `date created:` / `date modified:` — ISO 8601 (`YYYY-MM-DD`)
  - `tags:` array
- Plus EIC-specific fields:
  - `clippings: "[[00. Inbox/02. Clippings/{원본파일명}]]"` — 원본 Clippings 파일 링크 (wikilink in YAML must be quoted per `.claude/rules/wikilink-rules.md`)
  - `status: completed` — CMDS 5-value enum (`unread/reading/inProgress/completed/archived`)
- Summary section added at beginning (`## Summary`)
- Improved formatting and structure
- Links to existing topic notes in `30. Permanent Notes/` (see step 3)

## Main Process
```
1. IMPROVE CAPTURE & TRANSCRIPT (ICT)
   - Fix all grammar or transcript errors
   - Preserve the original language in the body. If summarizing for sharing,
     translate the Summary section to English (CMDS default working language is
     bilingual ko/en; English summaries travel further).
   - Remove extra/duplicated newlines
   - Add chapters using heading3 (###)
   - Add formatting (lists, highlights)
   - Keep overall length equal to original
   - Set status property to completed (per CMDS enum)

2. ADD SUMMARY FOR THREAD
   - Add Summary section at beginning (##)
   - Write catchy summaries suitable for Gobi space sharing
   - Use quotes verbatim to convey author's voice
   - Don't add highlights in summary

3. ENRICH USING CMDS TOPICS
   - Search 30. Permanent Notes/ for notes with frontmatter
     CMDS: "[[📚 102 Topics]]" — those are the canonical topic notes
   - Use the `obsidian-cli` skill: `obsidian search query="<keyword>"` to discover
     candidates, or invoke /query {topic} to synthesize-and-find
   - Validate links resolve before adding (`obsidian unresolved`); never invent
     missing topic notes — flag them in a "Topics to Create" list instead
   - Add a one-line summary about this source to each linked topic note
   - Cross-link to related literature notes (books, articles) in 20. Literature Notes/
```

## Caveats

### Content Completeness - CRITICAL

⚠️ **CRITICAL**: ICT section must be COMPLETE - not truncated

**Common failure pattern:**
- Agent starts ICT section
- Hits token/context limit mid-processing
- ICT cuts off mid-sentence: "Since I last wrote at the beginning of the summer, my methodol..."
- Agent marks status as `completed` anyway ❌ WRONG

**Prevention measures:**
1. **Check article length FIRST** before starting
2. **If source >3000 words**, process in chunks OR request context extension
3. **VERIFY ICT ends at natural stopping point** (end of paragraph/section, not mid-sentence)
4. **Self-check before marking completed**: "Does the last paragraph in ICT feel complete?"
5. **If truncated**, FINISH it before updating status to `completed`

**Quality verification:**
- ICT section should have multiple ### subsections (not just one incomplete section)
- Last sentence should end with proper punctuation, not "..." or cut-off text
- Length should be comparable to original source (not 30-50% shorter due to truncation)

**If you cannot complete full ICT:**
- Leave status at `inProgress` and add a "TODO" note in the body explaining what is missing
- DO NOT mark `completed` with incomplete work

### Rename Filenames
* Convert " " (curly/typographic quotes) to " (straight quote)
   * Same for single quotes
* Remove incomplete words -- 40살 전에 알았다면 `얼마ᄂ`
* Remove `Readwise` at the end

### Formatting Standards
- Use heading3 (###) for chapters
- Limit highlights to essence (one per chapter)
- Preserve original prose structure
- Overall length should equal original

### Topic Linking
- Only link to existing topic notes — those carry frontmatter `CMDS: "[[📚 102 Topics]]"` and live in `30. Permanent Notes/` (per CMDS frontmatter standard; topics are categorized via metadata, not folders)
- Validate all topic links before adding
- Add meaningful one-line summaries to topics
- **Tip**: Use `obsidian search query="keyword"` to discover topic candidates across the vault, or invoke `/query {topic}` for semantic synthesis. Run `obsidian unresolved` afterward to verify all wikilinks resolve (see `obsidian-cli` skill).
- **Wikilink emoji prefix rule**: when linking to a CMDS subcategory page like `📚 102 Topics`, include the emoji exactly — `[[📚 102 Topics]]`, not `[[102 Topics]]` (per `.claude/rules/wikilink-rules.md`).
