# gobi session

```
Usage: gobi session [options] [command]

Session commands (get, list, reply).

Options:
  -h, --help                   display help for command

Commands:
  get [options] <sessionId>    Get a session and its messages (paginated).
  list [options]               List all sessions you are part of, sorted by most recent activity.
  reply [options] <sessionId>  Send a human reply to a session you are a member of.
  help [command]               display help for command
```

## get

```
Usage: gobi session get [options] <sessionId>

Get a session and its messages (paginated).

Options:
  --limit <number>   Messages per page (default: "20")
  --cursor <string>  Pagination cursor from previous response
  -h, --help         display help for command
```

## list

```
Usage: gobi session list [options]

List all sessions you are part of, sorted by most recent activity.

Options:
  --limit <number>   Items per page (default: "20")
  --cursor <string>  Pagination cursor from previous response
  -h, --help         display help for command
```

## reply

```
Usage: gobi session reply [options] <sessionId>

Send a human reply to a session you are a member of.

Options:
  --content <content>     Reply content (markdown supported)
  --rich-text <richText>  Rich-text JSON array (e.g. [{"type":"text","text":"hello"}])
  -h, --help              display help for command
```
