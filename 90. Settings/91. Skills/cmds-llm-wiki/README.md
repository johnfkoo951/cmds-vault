# cmds-llm-wiki — Install & Use

A Claude Code skill that builds and maintains a [Karpathy-style LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) inside your existing Obsidian vault — without committing to a separate vault upfront.

## Install

You have two options. Both copy the same files; pick based on whether you want the skill globally or project-local.

### Option A — Global (recommended for personal use)

```bash
cp -r "90. Settings/91. Skills/cmds-llm-wiki" ~/.claude/skills/cmds-llm-wiki
```

Then in Claude Code, run:

```
> /reload-plugins
```

`/reload-plugins` is the fastest way to make a freshly-installed skill visible — no restart needed. (If your build doesn't expose that command, restart Claude Code as a fallback.)

Verify with `/help` — the four commands `/cmds-llm-wiki-ingest`, `/cmds-llm-wiki-query`, `/cmds-llm-wiki-lint`, `/cmds-llm-wiki-status` should appear.

### Option B — In-vault (recommended for cohort/team distribution)

Drop the entire `90. Settings/91. Skills/cmds-llm-wiki/` folder into your vault at the same path used by `cmds-vault` (sister skills: `gobi-cli`, `cmds-onboarding`, `cmds-maintenance`, `daily-book-update`). Claude Code, when launched from the vault root, picks up project-local skills under `90. Settings/91. Skills/`. This keeps the skill versioned alongside the vault. Same `/reload-plugins` step applies.

## First run

1. **Bootstrap + auto-seed Core Context** — run `/cmds-llm-wiki-status` from your vault root. This is the canonical first command:
   - Creates `LLMWiki/` skeleton (Sources / Wiki / Queries / index / log).
   - **Smart-seeds `Core Context.md`** by sampling 5–15 notes from your existing CMDS-style folders (`30. Permanent Notes/`, `Topics/`, `60. Collections/`, `20. Literature Notes/`, `Roundup/`) and inferring §1 (identity) + §2 (5–9 reuse axes) from real content.
   - The seeded Core Context lands with `status: seeded` (not yet active).
2. **Review Core Context** — open `LLMWiki/Core Context.md`. Refine §1 and §2 (especially the axes — the seed is a starting point, not a final answer). Once it reads correctly, flip frontmatter `status: seeded` → `status: active`.
   - If your vault has no `30. Permanent Notes/` etc., the bootstrap leaves a blank template (`status: template`) — fill §1/§2 manually.
3. **First ingest** — `/cmds-llm-wiki-ingest <file path or URL>`. File paths are the smoothest first try (e.g., something already clipped under `00. Inbox/`). The command will (a) ask "why are you saving this?", (b) save the source verbatim under `Sources/`, (c) compile 5–10 wiki pages under `Wiki/`, (d) update `index.md` and `log.md`.
4. **First query** — `/cmds-llm-wiki-query "<question>"`. The command reads `Core Context.md` + `index.md`, then drills into relevant `Wiki/` pages to synthesize a cited answer.
5. **First lint** — `/cmds-llm-wiki-lint`. Catches orphans, broken `[[links]]`, contradictions, stale claims. Run weekly.

## What gets created in your vault

```
{your-vault}/
└── LLMWiki/                    ← self-contained, portable
    ├── Core Context.md         # you fill this in once
    ├── index.md                # auto-maintained
    ├── log.md                  # auto-appended
    ├── Sources/                # immutable raw docs
    ├── Wiki/                   # LLM synthesis pages
    └── Queries/                # filed-back Q&A
```

Nothing else in your vault is touched. The wiki is self-contained.

## Graduating to full LLMWiki

When the lightweight version outgrows in-vault life (typical signal: 80–120 sources, or you want Web Clipper integration / qmd search / Book Ingest mode), graduate to the full template:

```bash
# 1. Move the wiki out
mv {your-vault}/LLMWiki ~/my-llm-wiki

# 2. Layer the full cmds-llm-wiki template on top
cd ~/my-llm-wiki
# (clone the upstream template into a sibling, then merge — see upstream README)

# 3. Open ~/my-llm-wiki as a new Obsidian vault
```

Because the lightweight skill uses the same schema and naming as upstream, **no content rewriting is needed**. You just gain the upstream features (mothership linking, qmd search, hooks, Book Ingest, etc.).

Upstream template: `cmds-llm-wiki v1.3.0` ([repo](https://github.com/johnfkoo951/cmds-llm-wiki))

## Sanity checklist

After install:

- [ ] `/reload-plugins` (or restart) — `/help` shows the four `/cmds-llm-wiki-*` commands
- [ ] `/cmds-llm-wiki-status` bootstraps `LLMWiki/` and seeds `Core Context.md` from existing notes (or leaves a clean template if the vault is empty)
- [ ] Reviewed `Core Context.md` — flipped `status: seeded` → `status: active`, axes feel right
- [ ] First `/cmds-llm-wiki-ingest <file>` produces a verbatim `Sources/` file and 5–10 `Wiki/` pages
- [ ] All wiki pages have the 7 required frontmatter properties
- [ ] `index.md` reflects the actual file tree (run `/cmds-llm-wiki-lint` to verify)

## Troubleshooting

- **"command not found" right after install** — run `/reload-plugins` in Claude Code. If your build lacks that command, restart Claude Code. Verify with `ls ~/.claude/skills/cmds-llm-wiki/commands/`.
- **Frontmatter rejected by Obsidian** — check YAML uses 2-space indent, wikilinks in YAML are quoted (`"[[link]]"`).
- **`/cmds-llm-wiki-ingest` fails on URL** — WebFetch may be blocked by the site; download to a local file and pass the path instead. (The first ingest is most reliable on a local file path anyway.)
- **Wiki feels generic** — `Core Context.md` is `status: seeded` and you haven't reviewed/refined the axes yet, or it's the unfilled template. Refine §2, flip to `status: active`; quality jumps immediately.
- **`/cmds-llm-wiki-ingest` says "run /status first"** — `LLMWiki/` doesn't exist yet. Status now owns bootstrap; that's intentional.

## Related

- Upstream template (graduation target): `/Users/lifidea/dev/cmds-llm-wiki-v1.3.0/`
- Sister skills: `90. Settings/91. Skills/{gobi-cli,cmds-onboarding,cmds-maintenance,daily-book-update}/`
- CMDS rules: cmds-vault `CLAUDE.md` + cmds-system-files `rules/{indentation,frontmatter-standard,wikilink}-rules.md`
- Karpathy gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
