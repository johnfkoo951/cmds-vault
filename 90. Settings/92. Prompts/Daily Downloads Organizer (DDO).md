---
title: Daily Downloads Organizer
abbreviation: DDO
category: automation
created: 2026-01-22
tags:
  - prompt
  - automation
  - file-management
---

## Purpose

Automatically organize files in your Downloads folder by type and content, moving them to appropriate subfolders.

## Input

- **Source folder**: `{{downloads_path}}` (default: `~/Downloads`)

## Output

- Organized files in category subfolders
- Summary table of moved files

## Configuration

```yaml
# Example configuration
downloads_path: ~/Downloads
special_patterns:
  receipts:
    - receipt
    - Receipt
    - invoice
    - order
  # Add your own patterns here
```

## Classification Rules

### 1. Special Classification (Priority)

These rules are checked first before file type classification:

| Condition | Target Folder |
|-----------|---------------|
| Filename contains receipt/invoice keywords | `Receipts/` |
| Custom patterns (user-defined) | User-defined folders |

### 2. File Type Classification

| Extension | Target Folder |
|-----------|---------------|
| `.pdf` | `PDFs/` |
| `.docx`, `.doc` | `Documents/` |
| `.xlsx`, `.xls`, `.csv` | `Data Files/` |
| `.pptx`, `.ppt`, `.key` | `Presentations/` |
| `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` | `Images/` |
| `.mp4`, `.mov`, `.mkv`, `.m4a`, `.mp3` | `Media/` |
| `.dmg`, `.pkg`, `.exe`, `.msi` | `Installers/` |
| `.app` | `Installers/` (move entire folder) |
| `.epub`, `.mobi` | `Ebooks/` |
| `.txt`, `.md` | `Text Files/` |
| `.zip`, `.tar.gz`, `.rar` | Extract then classify contents |
| Other | `Miscellaneous/` |

### 3. ZIP File Processing

1. Extract archive (create folder in same location)
2. Classify internal files according to above rules
3. Delete original archive file
4. Clean up empty folders

## Execution

```
Organize my downloads
```

or

```
Clean up ~/Downloads folder
```

## Exclusions

- Files already in subfolders (only process top-level files)
- System files (`.DS_Store`, `.localized`, `Thumbs.db`, etc.)

## Output Format

After completion, display a summary table:

| Category | Files Moved |
|----------|-------------|
| Receipts | N |
| PDFs | N |
| Documents | N |
| ... | ... |

## Customization Examples

### Adding Region-Specific Receipt Patterns

```yaml
special_patterns:
  receipts:
    - receipt
    - Receipt
    - invoice
    - order
    - Rechnung  # German
    - facture   # French
```

### Custom Folder Mappings

```yaml
custom_mappings:
  ".sketch": "Design Files/"
  ".fig": "Design Files/"
  ".ai": "Design Files/"
```

## Notes

- **Non-destructive**: Files are moved, not deleted (except archives after extraction)
- **Idempotent**: Safe to run multiple times
- **Top-level only**: Does not recursively process existing subfolders
