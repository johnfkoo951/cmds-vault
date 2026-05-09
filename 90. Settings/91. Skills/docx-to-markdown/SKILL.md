---
name: docx-to-markdown
description: Convert DOCX files into markdown while preserving headings, lists, tables, metadata, and extracted images.
---

# DOCX to Markdown Skill

Convert DOCX files to well-formatted markdown files with images extracted.

## Usage

```bash
python3 docx_to_markdown.py "<docx_path>" -o "<output_path>"
```

## Features

- **Metadata extraction**: title, author, subject, keywords
- **Heading preservation**: Maintains H1-H6 hierarchy from Word styles
- **Inline formatting**: Bold, italic conversion
- **List support**: Ordered and unordered lists
- **Table extraction**: Tables converted to markdown format
- **Image extraction**: Extracts images to `_files_/` folder with document prefix

## Output Structure

```
20. Literature Notes/Books/         # CMDS literature folder (typical for books)
├── document.docx                   # Original file
├── document.md                     # Extracted markdown
└── _files_/                        # Images folder (sibling to .md)
    ├── DocTitle_image1.png
    ├── DocTitle_figure2.jpg
    └── ...
```

### CMDS Output Defaults

Pick the destination based on source type:

| Source type | Recommended `-o` path |
|---|---|
| Book / long-form | `20. Literature Notes/Books/<title>.md` |
| Article / paper | `20. Literature Notes/Articles/<title>.md` |
| Apple Notes export | `20. Literature Notes/AppleNotes/<title>.md` |
| Triage (unsure) | `00. Inbox/02. Clippings/<title>.md`, then promote later |

Images extract to a `_files_/` sibling folder relative to the output `.md`. After conversion, link images via the relative `![alt](_files_/...)` markdown the script emits — Obsidian resolves them automatically.

**Pairs with**: `/connect` (capture as theme stub) or `cmds-llm-wiki-ingest` (compile into LLM Wiki) once the `.md` is in place.

## Image Prefix

Images are extracted with a document prefix derived from the title:
- Title: "Die Empty: Unleash Your Best Work Every Day"
- Prefix: `DieEmptyUnleash` (first 3 words, special chars removed)
- Image: `_files_/DieEmptyUnleash_image1.png`

This prevents filename collisions when extracting multiple documents to the same folder.

## Output Format

The script emits CMDS-conformant frontmatter (per `.claude/rules/frontmatter-standard.md`) plus optional provenance fields:

```markdown
---
type: literature
aliases: []
description: "Markdown extracted from DOCX: original.docx. {subject if present}"
author:
  - "[[Me]]"
date created: YYYY-MM-DD
date modified: YYYY-MM-DD
tags:
  - literature
  - imported
status: unread
source_file: "original.docx"
source_type: docx
extracted: YYYY-MM-DD HH:MM:SS
---

# {Document Title}

**Source author**: {DOCX core_properties author, if present}

{content with ![alt](_files_/DocTitle_image.png) links}
```

Notes:
- `author: [[Me]]` is the CMDS placeholder for user-created notes (resolved by the WELCOME ritual). The original DOCX author is surfaced as `**Source author**:` in the body so it stays visible without producing a YAML wikilink orphan.
- `status: unread` follows the CMDS 5-value enum (`unread/reading/inProgress/completed/archived`).
- Adjust `type:` (e.g. to `note`, `meeting`) and `tags:` as appropriate after import.

## Dependencies

```bash
pip install python-docx
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## Options

| Flag | Description |
|------|-------------|
| `-o`, `--output` | Output markdown file path (default: same as docx with .md) |
| `-q`, `--quiet` | Suppress progress messages |

## Limitations

- **Password-protected DOCX**: Cannot be opened (will fail with error)
- **Complex layouts**: May not preserve exact positioning
- **Embedded objects**: Non-image objects may not be extracted
