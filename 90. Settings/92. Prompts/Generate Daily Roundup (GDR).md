---
title: Generate Daily Roundup (GDR)
abbreviation: GDR
category: research
---
Generate comprehensive daily summaries integrating multiple sources with quote mining and topic linking.

## Input
- Target Date: YYYY-MM-DD (default: yesterday)
- Daily note: `00. Inbox/01. Daily Notes/{{YYYY-MM-DD}}.md` as the starting point
- Recent activity for the date in `30. Permanent Notes/`, `20. Literature Notes/`, `00. Inbox/02. Clippings/`, and `20. Literature Notes/AppleNotes/`
- If the daily note doesn't exist, create one with the standard 7-field CMDS frontmatter (`type: note`, `aliases`, `description` (English, double-quoted), `author: [[Me]]`, `date created`, `date modified`, `tags`) — see `.claude/rules/frontmatter-standard.md`

## Output
- File: `00. Inbox/03. AI Agent/03-1. Claude Code (MBP)/{{YYYY-MM-DD}}-roundup.md` (per `.claude/rules/file-creation-rules.md` — all AI-agent outputs land in `03. AI Agent/{env}/` first, then can be promoted)
- Enhanced `00. Inbox/01. Daily Notes/{{YYYY-MM-DD}}.md` with a wikilink back to the roundup
- Source coverage report (processed vs. available)
- Minimum 3-5 memorable quotes per roundup
- Bidirectional linking between daily note and roundup

## Main Process
```
1. JOURNAL FOUNDATION
   - Use 00. Inbox/01. Daily Notes/{{YYYY-MM-DD}}.md as starting point
   - If the file doesn't exist, create one with CMDS 7-field frontmatter
   - Keep original language (English/한글)
   - Fill note sections appropriately

2. COMPREHENSIVE SOURCE INTEGRATION
   - Count available sources first across the date's footprint
   - Integrate 20. Literature Notes/AppleNotes/ entries dated for the target day
   - Review 00. Inbox/02. Clippings/ for clippings created/modified that day
   - Pull recent activity from 30. Permanent Notes/ and 20. Literature Notes/Articles/
   - Dedup sources (already-processed/enriched sources have priority over raw)
   - Generate source coverage report

3. QUOTE MINING & TOPIC LINKING
   - Extract 3-5 memorable quotes preserving the original author's voice
   - Search 30. Permanent Notes/ for topic notes (`CMDS: "[[📚 102 Topics]]"`)
     before linking — use the `obsidian-cli` skill (`obsidian search query=...`)
     or invoke /query {topic} for semantic discovery
   - Validate all topic links point to existing files (`obsidian unresolved`)
   - Never invent topic notes — add a "Topics to Create" list at the end of the
     roundup for any concept that didn't have a home

4. JOURNAL ENHANCEMENT
   - Enrich the daily note with a brief roundup summary
   - Add the roundup wikilink (e.g. under a `## Roundup` section, or in a frontmatter array)
   - Ensure bidirectional linking is complete
```

## Caveats
### Folder Exclusion
- Skip `90. Settings/` (system files: skills, prompts, agent settings)
- Skip `80. References/` (external attachments and reference materials)
- Skip any folder starting with `_` (legacy convention; not present in CMDS but defensive)
- Skip `.obsidian/`, `.claude/`, `.gobi/` (config dirs)

### Source Coverage Requirements
⚠️ **CRITICAL**: Target 80%+ coverage of available sources

### Quote Mining & Topic Linking
- Extract 3-5 memorable quotes (format per `obsidian-markdown-structure` skill)
- Validate ALL topic links (use `obsidian-links` skill)
- Link to existing topic notes in `30. Permanent Notes/` (those with `CMDS: "[[📚 102 Topics]]"`); use `/query {topic}` to find candidates. Do not invent topic notes — flag missing ones in a "Topics to Create" section at the end.
- Post-validation: `obsidian unresolved` to catch any broken links after roundup generation (use `obsidian-cli` skill)
- **Wikilink emoji prefix rule**: include the emoji exactly when linking to CMDS pages — `[[📚 102 Topics]]`, not `[[102 Topics]]` (per `.claude/rules/wikilink-rules.md`).

### Journal Enhancement Rules
- Be brief but comprehensive
- Don't touch existing contents
- Each content should have link(s) to source note
- Ensure bidirectional linking is complete
