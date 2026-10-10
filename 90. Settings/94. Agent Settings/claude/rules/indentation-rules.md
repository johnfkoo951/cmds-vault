# Indentation Rules (YAML vs Markdown)

**Before EVERY Write() or Edit() operation on .md files, verify indentation:**

| Section              | Indentation  | Visual Example               |
| -------------------- | ------------ | ---------------------------- |
| **YAML frontmatter** | **2 SPACES** | `··- "[[link]]"` (· = space) |
| **Markdown body**    | **TAB**      | `→- List item` (→ = tab)     |

## YAML Frontmatter (2 spaces)

```yaml
---
type: note
aliases:
  - Example Alias
author:
  - "[[구요한]]"
tags:
  - AI
  - knowledge-management
---
```

## Markdown Body (TAB)

```markdown
- First level item
	- Second level (TAB)
		- Third level (TAB TAB)
```

## Common Mistakes

- ❌ Using tabs in YAML frontmatter
- ❌ Using spaces in markdown body indentation
- ❌ Mixing tabs and spaces in the same context
