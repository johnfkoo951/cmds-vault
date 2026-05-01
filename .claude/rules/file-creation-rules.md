# File Creation Rules

## Code Output Location

**ALL code-related outputs MUST be saved in:** `00. Inbox/03. AI Agent/` under an environment subfolder.

For single-machine usage, just use `03-1. Claude Code/` (no machine suffix needed). For multi-machine workflows (e.g., MacBook Pro + Mac Studio synced via Obsidian Sync), you may add machine-tagged subfolders to track which device an artifact came from:

| Subfolder (example) | Agent | Machine |
|---------------------|-------|---------|
| `03-1. Claude Code (MBP)/` | Claude Code | MacBook Pro |
| `03-2. Claude Code (Studio)/` | Claude Code | Mac Studio |
| `03-3. OpenClaw (MBP)/` | OpenClaw | MacBook Pro |
| `03-4. OpenClaw (Studio)/` | OpenClaw | Mac Studio |

**Auto-detection (multi-machine setup)**: Check base path to determine machine. Example:

- `<MBP base path>` → MBP subfolder
- `<Studio base path>` → Studio subfolder

(For single-machine vaults, this whole section is irrelevant — use one folder.)

## File Naming Convention

- Include date: `YYYY-MM-DD-description.ext`
- Use descriptive names
- Examples: `2026-04-28-data-analysis.py`, `2026-04-28-meeting-summary.md`

## Multi-File Project Folder Rule

When creating projects with multiple related files:
1. **FIRST** create an intermediate folder: `YYYY-MM-DD-project-name/`
2. **THEN** create all related files inside that folder

```
00. Inbox/03. AI Agent/03-1. Claude Code/
└── 2026-04-28-project-name/
    ├── index.html
    ├── styles.css
    └── script.js
```

**Never** scatter related project files directly in subfolder root.

## Exception: Video Projects (Remotion / heavy deps)

Video projects with `node_modules` or large render artifacts MUST go to a separate directory **outside the vault** (e.g., `~/DEV/video-projects/<name>/`) instead of the vault. Only context/progress MD files stay in the vault.

See `video-project-workflow.md` for full rule.
