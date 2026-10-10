# Obsidian Wikilink Rules

## Syntax

| Pattern | Usage |
|---------|-------|
| `[[Note Name]]` | Basic link |
| `[[Note Name\|Display Text]]` | Aliased link |
| `[[Note Name#Heading]]` | Link to heading |
| `[[Note Name^block-id]]` | Link to block |
| `![[Note Name]]` | Embed file |
| `![[image.png]]` | Embed image |

## Rules

1. **Always use wikilinks `[[]]`** for internal references, NOT markdown links
2. **Wikilinks in YAML must be quoted**: `"[[link]]"` not bare `[[link]]`
3. **Array fields** (`author:`, `attendees:`, `aliases:`): Use array format with quoted wikilinks
4. **Emoji prefixes are PART of the filename — never strip them**. Files with 📜/📚/🏛/🏷/📎/📦/🔖/📈/🎹/📘 prefixes require the exact emoji in the wikilink. If you write `[[Schema는 Harness다]]` instead of `[[📜 Schema는 Harness다]]`, Obsidian treats it as a missing link and **auto-creates an empty placeholder file in `00. Inbox/`** when clicked. This pollutes the inbox with orphan files.
5. **Verify before linking**: Before writing a wikilink to a file with an emoji prefix, use Glob/Bash to confirm the exact filename including the prefix. Never guess.
6. **Use aliases for cleaner display**: If the visible text shouldn't show the emoji, use the aliased form: `[[📜 Long Title|Display Text]]` — the link still resolves correctly because the target before `|` is exact.

## Examples in This Vault

- `[[🏛 CMDS Head Quarter]]` — Main hub
- `[[📚 620 Generative AI]]` — CMDS category
- `[[구요한]]` — People note (no prefix)
- `[[🏷 Meeting Notes]]` — Index page
- `[[📜 Schema는 Harness다 - Karpathy LLM Wiki와 CMDS의 구조적 동치에 관한 보고서|Schema는 Harness다 보고서]]` — Aliased link with emoji-prefixed target

## Anti-Pattern (DO NOT)

```markdown
❌ [[Schema는 Harness다 보고서]]                    # Missing 📜 prefix → creates empty file in Inbox
❌ [[CMDS Head Quarter]]                          # Missing 🏛 prefix → creates empty file
❌ [[620 Generative AI]]                          # Missing 📚 prefix → creates empty file
```

```markdown
✅ [[📜 Schema는 Harness다 - Karpathy LLM Wiki와 CMDS의 구조적 동치에 관한 보고서]]
✅ [[🏛 CMDS Head Quarter]]
✅ [[📚 620 Generative AI]]
```
