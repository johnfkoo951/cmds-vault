# cmds-vault

> Class-ready Obsidian vault running [CMDS conventions](https://system.cmdspace.work) with [Gobi Desktop](https://gobi.app) integration baked in. Clone, open in Obsidian, start writing.

## What this is

This vault is a **graft**:

- **Base** — [cmds-system-files](https://github.com/johnfkoo951/cmds-system-files) by John Koo. The 5 system files (`CLAUDE.md`, `AGENTS.md`, `CMDS.md`, `CMDS-Guide.md`, `🏛 CMDS Head Quarter.md`) and 7 shared rules (`.claude/rules/`) define the CMDS PKM operating model — atomic notes, frontmatter standard, 4-stage pipeline (Connect → Merge → Develop → Share), wikilink discipline.
- **Add-on** — minimal Gobi files (`BRAIN.md`, `BRAIN.jpg`, `BRAIN_PROMPT.md`, `app/home.html`, `.gobi/`) so the vault registers as a Gobi Brain and can publish to Gobi Space. Gobi tooling lives in `90. Settings/gobi/Skills/gobi-cli/` and `90. Settings/gobi/Prompts/`.

Numeric folders (`00. Inbox/` … `90. Settings/`) are pre-created with `.gitkeep` placeholders matching `cmds-system-files/rules/directory-structure.md`. No manual setup required.

## Quickstart

### 1. Clone and open

```bash
git clone https://github.com/jykim/cmds-vault.git ~/Documents/cmds-vault
```

Open `~/Documents/cmds-vault` in Obsidian via **Open folder as vault**.

### 2. Personalize the Brain

- Replace `BRAIN.jpg` with your own portrait or icon (square, 512×512+, JPG/PNG renamed to `BRAIN.jpg`).
- Edit `BRAIN.md` — fill in your name, interests, pinned notes.
- Edit `BRAIN_PROMPT.md` — set the voice your Brain uses when answering chat sessions on Gobi Space.

### 3. Connect Gobi (optional but recommended)

Install [Gobi Desktop](https://gobi.app), sign in, and add this vault as a Brain:

```bash
gobi vault add ~/Documents/cmds-vault
gobi sync
```

`.gobi/syncfiles` controls what gets pushed to Gobi Space (default: `BRAIN.{md,jpg}`, `BRAIN_PROMPT.md`, `app/home.html`). `.gobi/settings.yaml` carries the `vaultSlug` and chat configuration — adjust as needed.

To customize the homepage that Gobi Space renders for visitors, run the **Create Brain Homepage (CBH)** prompt at `90. Settings/gobi/Prompts/Create Brain Homepage (CBH).md` from Claude Code.

### 4. Start writing

- Daily fragments → `00. Inbox/01. Daily Notes/`
- Web clippings → `00. Inbox/02. Clippings/`
- AI agent outputs → `00. Inbox/03. AI Agent/`
- Distilled notes → `30. Permanent Notes/` (after Connect → Merge → Develop)

Refer to `[[🏛 CMDS Head Quarter]]` in Obsidian for the full navigation.

## Layout

```
cmds-vault/
├── CLAUDE.md, AGENTS.md, CMDS.md, CMDS-Guide.md      # CMDS system files (load order: precedence 1-4)
├── 🏛 CMDS Head Quarter.md                            # Navigation hub (precedence 5)
├── .claude/rules/                                    # 7 shared rules (frontmatter, wikilink, etc.)
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
│   ├── 94. Agent Settings/claude/{agents,commands,rules,skills}/   # cmds Agent Settings (symlink-ready)
│   └── gobi/                                                       # Gobi-specific tooling
│       ├── Skills/gobi-cli/                                        # Gobi CLI skill (sync, space, brain, session)
│       └── Prompts/Create Brain Homepage (CBH).md                  # Customize app/home.html
│
├── BRAIN.md, BRAIN.jpg, BRAIN_PROMPT.md              # Gobi Brain identity
├── .gobi/{settings.yaml, syncfiles}                  # Gobi sync configuration
└── app/home.html                                     # Gobi Space homepage (CMDS-themed default)
```

## What this vault does NOT include

Kept deliberately minimal for class use. The following are **not** copied from the upstream `ai4pkm-vault`:

- `orchestrator.yaml` and the 22 ai4pkm prompts (EIC, GDR, TIU, ARP, …) — these are ai4pkm-specific automation; out of scope here
- ai4pkm community workflows (GSA, CPU, CUP, ACQ, ANQ, CUS) — relevant only inside ai4pkm's Gobi space, not class
- `gobi-onboarding`, `gobi-migration` skills — first-time setup or legacy migration, not needed for new student vaults

If you want any of these later, copy them from [ai4pkm-vault](https://github.com/jykim/ai4pkm-vault) by hand.

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
