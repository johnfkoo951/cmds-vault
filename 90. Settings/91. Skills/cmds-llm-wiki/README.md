# cmds-llm-wiki — Install & Use

A Claude Code skill that builds and maintains a [Karpathy-style LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) inside your existing Obsidian vault — **integrated with CMDS conventions** (sources in `10. Raw Sources/`, Core Context as pointer to `BRAIN.md`/HQ/`CMDS.md`, location persisted in `AGENTS.md`). No vault-content duplication.

## Install

You have two options. Both copy the same files; pick based on whether you want the skill globally or project-local.

### Option A — Global (recommended for personal use)

```bash
cp -r "90. Settings/91. Skills/cmds-llm-wiki" ~/.claude/skills/cmds-llm-wiki
```

Then in Claude Code:

```
> /reload-plugins
```

`/reload-plugins` is the fastest way to make a freshly-installed skill visible — no restart needed. (If your build doesn't expose that command, restart Claude Code as a fallback.)

Verify with `/help` — the four commands `/cmds-llm-wiki-ingest`, `/cmds-llm-wiki-query`, `/cmds-llm-wiki-lint`, `/cmds-llm-wiki-status` should appear.

### Option B — In-vault (recommended for cohort/team distribution)

Drop the entire `90. Settings/91. Skills/cmds-llm-wiki/` folder into your vault at the same path used by `cmds-vault` (sister skills: `gobi-cli`, `cmds-onboarding`, `cmds-maintenance`, `daily-book-update`). Claude Code, when launched from the vault root, picks up project-local skills under `90. Settings/91. Skills/`. This keeps the skill versioned alongside the vault. Same `/reload-plugins` step applies.

## First run

1. **Bootstrap** — `/cmds-llm-wiki-status` from your vault root (canonical first command).
   - **Asks where to create the wiki folder**: `LLMWiki/` (default), `90. Settings/LLMWiki/`, or a custom path. Persists the choice to `AGENTS.md` frontmatter (`llmWikiPath:`).
   - Creates `{llmWikiPath}/{Wiki,Queries}` + `index.md` + `log.md`. **No `Sources/` subfolder** — sources go to CMDS-canonical `10. Raw Sources/{NN. category}/`.
   - **Seeds `Core Context.md` as a pointer file**: §1 → [[BRAIN]], §2 → [[🏛 CMDS Head Quarter#Current Focus Areas]], §3 → [[CMDS]], §4 → [[CMDS]] / [[🏛 CMDS Guide]]. Skill commands dereference at runtime — no content duplication.
   - For non-CMDS vaults (no canonical files), falls back to inline-seeding axes from sampled notes in `30. Permanent Notes/`, `Topics/`, etc.
   - Lands with `status: seeded`.
2. **Review Core Context** — open `{llmWikiPath}/Core Context.md`. Confirm the pointer targets reflect your current focus. Once it reads correctly, flip `status: seeded` → `status: active`.
3. **First ingest** — `/cmds-llm-wiki-ingest <file path or URL>`. The command will:
   - (a) Ask "why are you saving this?" — bound to a HQ Focus Area or `📚 NNN` CMDS category.
   - (b) Save the source verbatim to `10. Raw Sources/{NN. category}/{YYYY-MM-DD}-{slug}.md`.
   - (c) If the source originated from `00. Inbox/`, **MOVE** it (not copy) — single source of truth.
   - (d) Compile 5–10 wiki pages under `{llmWikiPath}/Wiki/`.
   - (e) Update `index.md` and `log.md`.
4. **First query** — `/cmds-llm-wiki-query "<question>"`. The command reads `Core Context.md` (follows pointers to BRAIN/HQ/CMDS), then `index.md`, then candidate `Wiki/` pages, to synthesize a cited answer. Substantial answers file to `Queries/`.
5. **First lint** — `/cmds-llm-wiki-lint`. Catches orphans, broken `[[links]]`, contradictions, stale claims, and **Inbox residue** (sources that should have been MOVED). Run weekly.

## What gets created in your vault

```
{your-vault}/
├── AGENTS.md                       ← `llmWikiPath:` field added on first run
├── 10. Raw Sources/                ← CMDS canonical (created on first ingest)
│   ├── 11. Articles/
│   ├── 12. Papers/
│   ├── 13. Books/
│   ├── 14. Transcripts/
│   └── 15. Clippings/
└── {llmWikiPath}/                  ← default `LLMWiki/`, configurable
    ├── Core Context.md             # POINTER to BRAIN/HQ/CMDS — no content dup
    ├── index.md                    # auto-maintained catalog
    ├── log.md                      # auto-appended event log
    ├── Wiki/                       # LLM synthesis pages
    └── Queries/                    # filed-back Q&A
```

**The wiki does NOT duplicate vault content**:
- Sources live ONCE — under `10. Raw Sources/` (CMDS canonical), MOVED from `00. Inbox/` on ingest.
- Core Context POINTS to existing CMDS files instead of snapshotting their content.
- Location is configurable so the wiki fits your existing layout, not the other way around.

## Graph view

`/cmds-llm-wiki-status` offers to install a tuned `.obsidian/graph.json` with **4 color groups** and a path filter scoped to LLMWiki content:

| Color | What | Query |
|-------|------|-------|
| 🔴 Pink/red | Raw Sources | `path:"10. Raw Sources"` |
| 🔵 Blue/teal | Wiki pages | `path:"{llmWikiPath}/Wiki"` |
| 🟢 Green | Queries | `path:"{llmWikiPath}/Queries"` |
| 🟡 Yellow | Core Context (hub) | `path:"{llmWikiPath}/Core Context"` |

Default filter: `(path:"{llmWikiPath}" OR path:"10. Raw Sources") -file:log -file:index` — hides everything outside LLMWiki, plus excludes the `log.md` and `index.md` system files from the graph (they accumulate links to every page and make the graph noisy). Clear the filter in the UI to see your full vault.

Open Graph view: `Cmd+G` (macOS) / `Ctrl+G` (Windows/Linux). You'll see Raw Sources cluster on one side, Wiki pages densely cross-linked in the middle, Queries hanging off the Wiki cluster, and Core Context as a central hub.

**Install behavior**: silent if your vault has the Obsidian default graph (no color groups, empty search). If you've customized your graph view, the bootstrap asks before overwriting and lets you skip. Re-install later by copying `templates/graph.json` from this skill manually.

## Graduating to full LLMWiki

When the lightweight version outgrows in-vault life (typical signal: 80–120 sources, or you want Web Clipper templates / qmd search / Book Ingest mode), graduate to the full template:

```bash
# 1. Move the wiki + raw sources out (two folders, since they're separate now)
mv "{your-vault}/{llmWikiPath}" ~/my-llm-wiki
mv "{your-vault}/10. Raw Sources" ~/my-llm-wiki/

# 2. Layer the full cmds-llm-wiki template on top
cd ~/my-llm-wiki
# (clone the upstream template into a sibling, then merge — see upstream README)

# 3. Update Core Context.md — pointer targets (BRAIN/HQ/CMDS) won't resolve in the new vault
#    Either copy those files in, or convert Core Context back to inline content
#    (the pointer template's §1/§2 fallback content shows the inline shape).

# 4. Open ~/my-llm-wiki as a new Obsidian vault
```

Schema and file naming match upstream so **no content rewriting is needed**. The CMDS-integrated trade vs. v0.1: graduation is two `mv` commands + a Core Context inline-conversion (the price for in-vault dedup). You gain the upstream features in return.

Upstream template: `cmds-llm-wiki v1.3.0` ([repo](https://github.com/johnfkoo951/cmds-llm-wiki))

## Sanity checklist

After install:

- [ ] `/reload-plugins` (or restart) — `/help` shows the four `/cmds-llm-wiki-*` commands
- [ ] `/cmds-llm-wiki-status` asks where to create LLMWiki, persists choice to `AGENTS.md`, seeds Core Context as pointer file
- [ ] `AGENTS.md` frontmatter contains `llmWikiPath: "..."`
- [ ] Reviewed `{llmWikiPath}/Core Context.md` — pointer targets resolve, flipped `status: seeded` → `active`
- [ ] First `/cmds-llm-wiki-ingest <file>` saves the source under `10. Raw Sources/{NN. category}/`, NOT `{llmWikiPath}/Sources/`
- [ ] If source came from `00. Inbox/`, the original file was deleted (MOVE not COPY)
- [ ] All wiki pages have the 7 required frontmatter properties
- [ ] `index.md` reflects the actual file tree (run `/cmds-llm-wiki-lint` to verify)

## Troubleshooting

- **"command not found" right after install** — run `/reload-plugins` in Claude Code. If your build lacks that command, restart Claude Code. Verify with `ls ~/.claude/skills/cmds-llm-wiki/commands/`.
- **Frontmatter rejected by Obsidian** — check YAML uses 2-space indent, wikilinks in YAML are quoted (`"[[link]]"`).
- **`/cmds-llm-wiki-ingest` fails on URL** — WebFetch may be blocked by the site; download to a local file and pass the path instead. (The first ingest is most reliable on a local file path anyway.)
- **Wiki feels generic** — `Core Context.md` pointer targets are stale (e.g., HQ Focus Areas don't match your current work). Refresh the targets, then re-run `/cmds-llm-wiki-status` to re-seed if needed.
- **`/cmds-llm-wiki-ingest` says "run /status first"** — `{llmWikiPath}/` doesn't exist yet. Status owns bootstrap; that's intentional.
- **Sources appearing in `{llmWikiPath}/Sources/`** — old layout. v0.2 puts sources in `10. Raw Sources/{NN. category}/` instead. If upgrading from v0.1, manually move sources out of `{llmWikiPath}/Sources/` into the canonical location.
- **Core Context pointer targets don't exist** (`BRAIN.md` / HQ / CMDS missing) — your vault isn't CMDS-style. The bootstrap should have fallen back to inline §1/§2 — if it didn't, edit Core Context manually (the template's fallback content shows the inline shape).

## Related

- Upstream template (graduation target): `/Users/lifidea/dev/cmds-llm-wiki-v1.3.0/`
- Sister skills: `90. Settings/91. Skills/{gobi-cli,cmds-onboarding,cmds-maintenance,daily-book-update}/`
- CMDS rules: cmds-vault `CLAUDE.md` + cmds-system-files `rules/{indentation,frontmatter-standard,wikilink}-rules.md`
- Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Future work (deferred — see SKILL.md)

Captured but not in v0.2: drop `index.md` in favor of HQ Focus Lens, reuse `60. Collections/61. People/` for entities, add `CMDS:` field to wiki pages, drop `log.md` to BRAIN activity, full CMDS-native reframe (no `{llmWikiPath}/Wiki/` at all), non-CMDS vault `.cmds-llm-wiki.yml` config fallback.
