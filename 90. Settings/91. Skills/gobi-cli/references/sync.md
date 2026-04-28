# gobi sync

```
Usage: gobi sync [options]

Sync local vault files with Gobi Webdrive.

Options:
  --upload-only              Only upload local changes to server
  --download-only            Only download server changes to local
  --conflict <strategy>      Conflict resolution strategy: ask|server|client|skip (default: "ask")
  --dir <path>               Local vault directory (default: current directory)
  --dry-run                  Preview changes without making them
  --full                     Full sync: ignore cursor and hash cache, re-check every file
  --path <path>              Restrict sync to a specific file or folder (repeatable) (default: [])
  --plan-file <path>         Write dry-run plan to file (use with --dry-run) or read plan to execute (use with --execute)
  --execute                  Execute a previously written plan file (requires --plan-file)
  --conflict-choices <json>  Per-file conflict resolutions as JSON object, e.g. '{"file.md":"server"}' (use with --execute)
  -h, --help                 display help for command
```
