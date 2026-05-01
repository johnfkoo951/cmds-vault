# cmds-vault

> Class-ready Obsidian vault running [CMDS conventions](https://system.cmdspace.work) with [Gobi Desktop](https://gobi.app) integration baked in. Clone, open in Obsidian, start writing.

## What this is

This vault is a **graft**:

- **Base** — [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) by John Koo. The 5 system files (`CLAUDE.md`, `AGENTS.md`, `CMDS.md`, `🏛 CMDS Guide.md`, `🏛 CMDS Head Quarter.md`) and 7 shared rules (`.claude/rules/`) plus 8 slash commands (`.claude/commands/`) define the CMDS PKM operating model — atomic notes, frontmatter standard, 4-stage pipeline (Connect → Merge → Develop → Share), wikilink discipline.
- **Add-on** — minimal Gobi identity files (`BRAIN.md`, `BRAIN.jpg`, `BRAIN_PROMPT.md`) so the vault registers as a Gobi Brain. Skills and prompts that drive Gobi live in cmds-style `90. Settings/91. Skills/` and `90. Settings/92. Prompts/`. The `.gobi/` runtime folder is **not** shipped — `gobi init` creates it on first run.

Numeric folders (`00. Inbox/` … `90. Settings/`) are pre-created with `.gitkeep` placeholders matching `cmds-system-files/rules/directory-structure.md`. No manual setup required.

## Quickstart

### 1. Clone and open

```bash
git clone https://github.com/johnfkoo951/cmds-vault.git ~/Documents/cmds-vault
```

Open `~/Documents/cmds-vault` in Obsidian via **Open folder as vault**.

### 2. Read [[WELCOME]] first

Before personalizing, open `WELCOME.md` in Obsidian. It walks through:

- The 5 system files (CLAUDE / AGENTS / CMDS / 🏛 CMDS Guide / 🏛 HQ) and what each one is for
- How to batch-replace the `[[Me]]` placeholder with your own name (one Claude Code session)
- A 5-minute first Connect → Merge → Develop → Share cycle
- Where to find the slash commands

The WELCOME doc is the canonical "first read." This README is just deployment.

### 3. Personalize the Brain

- Replace `BRAIN.jpg` with your own portrait or icon (square, 512×512+, JPG/PNG renamed to `BRAIN.jpg`).
- Edit `BRAIN.md` — fill in your name, interests, pinned notes.
- Edit `BRAIN_PROMPT.md` — set the voice your Brain uses when answering chat sessions on Gobi Space.

### 4. Connect Gobi

Install [Gobi Desktop](https://gobi.app) (or just the [CLI](https://github.com/gobi-ai/cli)), then run the four setup commands **in order**:

```bash
cd ~/Documents/cmds-vault

gobi init           # log in, create or pick a vault → creates .gobi/settings.yaml with vaultSlug
gobi space warp     # pick which Gobi space to publish to → adds selectedSpaceSlug

# tell Gobi what to sync (one-time)
mkdir -p .gobi && cat > .gobi/syncfiles <<'EOF'
/BRAIN.jpg
/BRAIN.md
/BRAIN_PROMPT.md
EOF

gobi sync           # first upload of BRAIN.{md,jpg}, BRAIN_PROMPT.md
```

The repo ships **without** `.gobi/` — `gobi init` creates it cleanly with the auto-generated `vaultSlug` (like `brave-path-zr962w`). Don't hand-edit those values.

After `gobi sync`, your Brain page appears at `https://gobispace.com/@<your-vault-slug>`.

For the full first-run flow with troubleshooting and resume logic, follow the **Gobi Onboarding** skill at:
- `90. Settings/91. Skills/gobi-onboarding/SKILL.md`

To customize what visitors see on your Brain page, run the **Create Brain Homepage (CBH)** prompt at:
- `90. Settings/92. Prompts/Create Brain Homepage (CBH).md`

CBH creates `app/home.html` from scratch. After running it, add `homepage: "[[app/home.html]]"` to `BRAIN.md` frontmatter and `/app/home.html` to `.gobi/syncfiles`, then re-sync.

### 5. Start writing

- Daily fragments → `00. Inbox/01. Daily Notes/`
- Web clippings → `00. Inbox/02. Clippings/`
- AI agent outputs → `00. Inbox/03. AI Agent/`
- Distilled notes → `30. Permanent Notes/` (after Connect → Merge → Develop)

Refer to `[[🏛 CMDS Head Quarter]]` in Obsidian for the full navigation.

## Layout

```
cmds-vault/
├── CLAUDE.md, AGENTS.md, CMDS.md, 🏛 CMDS Guide.md   # CMDS system files (load order: precedence 1-4)
├── 🏛 CMDS Head Quarter.md                            # Navigation hub (precedence 5)
├── WELCOME.md                                         # First-read onboarding doc (vault use guide + author batch-replace)
├── .claude/rules/                                    # 7 shared rules (frontmatter, wikilink, etc.)
├── .claude/commands/                                 # 8 slash commands (connect/merge/develop/share/inbox/lint/query/status)
│
├── 00. Inbox/{01-09 subfolders}/                     # Capture
├── 10. CMDS Process/                                 # Connect → Merge → Develop → Share
├── 20. Literature Notes/                             # 외부 지식 내재화
├── 30. Permanent Notes/                              # Evergreen content
├── 40. Docs/                                         # Technical documentation
├── 50. Assets/                                       # Reusable resources
├── 60. Collections/                                  # People, Meetings, Preferences
├── 70. Outputs/                                      # Final deliverables
├── 80. References/                                   # Reference materials
├── 90. Settings/
│   ├── 91. Skills/
│   │   ├── gobi-cli/                                  # Gobi CLI skill (sync, space, brain, session)
│   │   └── gobi-onboarding/                           # First-run setup walkthrough
│   ├── 92. Prompts/
│   │   └── Create Brain Homepage (CBH).md             # Build a custom Brain page on demand
│   └── 94. Agent Settings/claude/{agents,commands,rules,skills}/   # cmds Agent Settings (symlink-ready)
│
└── BRAIN.md, BRAIN.jpg, BRAIN_PROMPT.md              # Gobi Brain identity (sync target)
```

`.gobi/` (settings + sync state) is created by `gobi init` on first run — not shipped. `app/home.html` is created on demand by the CBH prompt — also not shipped.

## What this vault does NOT include

Kept deliberately minimal for class use. The following are **not** copied from the upstream `ai4pkm-vault`:

- `orchestrator.yaml` and the 22 ai4pkm prompts (EIC, GDR, TIU, ARP, …) — these are ai4pkm-specific automation; out of scope here
- ai4pkm community workflows (GSA, CPU, CUP, ACQ, ANQ, CUS) — relevant only inside ai4pkm's Gobi space, not class
- `gobi-migration` skill — legacy ai4pkm-vault migration tool, not needed for new student vaults

If you want any of these later, copy them from [ai4pkm-vault](https://github.com/jykim/ai4pkm-vault) by hand.

> Note: `gobi-onboarding` IS included (under `90. Settings/91. Skills/gobi-onboarding/`) but it's a **streamlined class version** of ai4pkm's, not a copy. Voice mode is optional, no BBF/BBG profile-extraction games, anchored to CMDS folder taxonomy and Connect→Merge→Develop→Share vocabulary.

## Symlink the .claude/ folder (advanced, optional)

`cmds-system-files/rules/directory-structure.md` recommends keeping the source-of-truth `.claude/` content under `90. Settings/94. Agent Settings/claude/` so it syncs through Obsidian Sync, then symlinking from the hidden `.claude/` to the visible folder. This vault ships the **flat** layout (`rules/` directly under `.claude/`) so cloning works zero-setup. If you want the cmds-recommended layout:

```bash
cd cmds-vault/.claude
mv rules rules_backup
ln -s "../90. Settings/94. Agent Settings/claude/rules" rules
# Move the actual rule files
mv rules_backup/* "../90. Settings/94. Agent Settings/claude/rules/"
rmdir rules_backup
```

Repeat for `agents`, `commands`, `skills` if you populate them.

## Credits

- **CMDS conventions** — [구요한 (John Koo)](https://github.com/johnfkoo951) ([cmds-system-files](https://github.com/johnfkoo951/cmds-system-files))
- **Gobi integration** — adapted from [ai4pkm-vault](https://github.com/jykim/ai4pkm-vault) by [Jin Kim](https://github.com/jykim)
- **License** — see upstream repos. CMDS rules are MIT-licensed; this vault redistributes them under the same terms.

## Updating

To pull upstream cmds rule changes:

```bash
# Fetch the latest cmds-system-files
cd ~/dev/cmds-system-files && git pull

# Copy any updated rules
cp ~/dev/cmds-system-files/rules/*.md /path/to/cmds-vault/.claude/rules/
cp ~/dev/cmds-system-files/files/CLAUDE.md /path/to/cmds-vault/CLAUDE.md
# etc.
```

Open a PR to this repo if you want the class-wide vault to track the change.
