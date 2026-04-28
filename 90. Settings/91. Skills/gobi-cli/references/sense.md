# gobi sense

```
Usage: gobi sense [options] [command]

Sense commands (activities, transcriptions).

Options:
  -h, --help                display help for command

Commands:
  activities [options]      Fetch activity records within a time range.
  transcriptions [options]  Fetch transcription records within a time range.
  help [command]            display help for command
```

## activities

```
Usage: gobi sense activities [options]

Fetch activity records within a time range.

Options:
  --start-time <iso>  Start of time range (ISO 8601 UTC, e.g. 2026-03-20T00:00:00Z)
  --end-time <iso>    End of time range (ISO 8601 UTC, e.g. 2026-03-20T23:59:59Z)
  -h, --help          display help for command
```

## transcriptions

```
Usage: gobi sense transcriptions [options]

Fetch transcription records within a time range.

Options:
  --start-time <iso>  Start of time range (ISO 8601 UTC, e.g. 2026-03-20T00:00:00Z)
  --end-time <iso>    End of time range (ISO 8601 UTC, e.g. 2026-03-20T23:59:59Z)
  -h, --help          display help for command
```
