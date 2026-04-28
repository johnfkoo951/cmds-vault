# gobi space

```
Usage: gobi space [options] [command]

Space commands (threads, replies).

Options:
  --space-slug <slug>                Space slug (overrides .gobi/settings.yaml)
  -h, --help                         display help for command

Commands:
  list                               List spaces you are a member of.
  warp [spaceSlug]                   Select the active space. Pass a slug to warp directly, or omit for interactive selection.
  get-thread [options] <threadId>    Get a thread and its replies (paginated).
  list-threads [options]             List threads in a space (paginated).
  create-thread [options]            Create a thread in a space.
  edit-thread [options] <threadId>   Edit a thread. You must be the author.
  delete-thread <threadId>           Delete a thread. You must be the author.
  create-reply [options] <threadId>  Create a reply to a thread in a space.
  edit-reply [options] <replyId>     Edit a reply. You must be the author.
  delete-reply <replyId>             Delete a reply. You must be the author.
  help [command]                     display help for command
```

## list

```
Usage: gobi space list [options]

List spaces you are a member of.

Options:
  -h, --help  display help for command
```

## warp

```
Usage: gobi space warp [options] [spaceSlug]

Select the active space. Pass a slug to warp directly, or omit for interactive selection.

Options:
  -h, --help  display help for command
```

## get-thread

```
Usage: gobi space get-thread [options] <threadId>

Get a thread and its replies (paginated).

Options:
  --limit <number>   Replies per page (default: "20")
  --cursor <string>  Pagination cursor from previous response
  -h, --help         display help for command
```

## list-threads

```
Usage: gobi space list-threads [options]

List threads in a space (paginated).

Options:
  --limit <number>   Items per page (default: "20")
  --cursor <string>  Pagination cursor from previous response
  -h, --help         display help for command
```

## create-thread

```
Usage: gobi space create-thread [options]

Create a thread in a space.

Options:
  --title <title>           Title of the thread
  --content <content>       Thread content (markdown supported)
  --auto-attachments        Upload wiki-linked [[files]] to webdrive before posting
  --vault-slug <vaultSlug>  Vault slug for attachment uploads (overrides .gobi/settings.yaml)
  -h, --help                display help for command
```

## edit-thread

```
Usage: gobi space edit-thread [options] <threadId>

Edit a thread. You must be the author.

Options:
  --title <title>           New title for the thread
  --content <content>       New content for the thread (markdown supported)
  --auto-attachments        Upload wiki-linked [[files]] to webdrive before editing
  --vault-slug <vaultSlug>  Vault slug for attachment uploads (overrides .gobi/settings.yaml)
  -h, --help                display help for command
```

## delete-thread

```
Usage: gobi space delete-thread [options] <threadId>

Delete a thread. You must be the author.

Options:
  -h, --help  display help for command
```

## create-reply

```
Usage: gobi space create-reply [options] <threadId>

Create a reply to a thread in a space.

Options:
  --content <content>  Reply content (markdown supported)
  -h, --help           display help for command
```

## edit-reply

```
Usage: gobi space edit-reply [options] <replyId>

Edit a reply. You must be the author.

Options:
  --content <content>       New content for the reply (markdown supported)
  --auto-attachments        Upload wiki-linked [[files]] to webdrive before editing
  --vault-slug <vaultSlug>  Vault slug for attachment uploads (overrides .gobi/settings.yaml)
  -h, --help                display help for command
```

## delete-reply

```
Usage: gobi space delete-reply [options] <replyId>

Delete a reply. You must be the author.

Options:
  -h, --help  display help for command
```
