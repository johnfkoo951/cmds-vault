# gobi brain

```
Usage: gobi brain [options] [command]

Brain commands (search, ask, publish, unpublish, updates).

Options:
  -h, --help                        display help for command

Commands:
  search [options]                  Search public brains by text and semantic similarity.
  ask [options]                     Ask a brain a question. Creates a targeted session (1:1 conversation).
  publish                           Upload BRAIN.md to the vault root on webdrive. Triggers post-processing (brain sync, metadata update, Discord notification).
  unpublish                         Delete BRAIN.md from the vault on webdrive.
  list-updates [options]            List recent brain updates. Without --space-slug, lists all updates for you. With --space-slug, lists updates for that space. Use --mine to show only updates by
                                    you.
  post-update [options]             Post a brain update for a vault.
  edit-update [options] <updateId>  Edit a published brain update. You must be the author.
  delete-update <updateId>          Delete a published brain update. You must be the author.
  help [command]                    display help for command
```

## search

```
Usage: gobi brain search [options]

Search public brains by text and semantic similarity.

Options:
  --query <query>  Search query
  -h, --help       display help for command
```

## ask

```
Usage: gobi brain ask [options]

Ask a brain a question. Creates a targeted session (1:1 conversation).

Options:
  --vault-slug <vaultSlug>  Slug of the brain/vault to ask
  --question <question>     The question to ask (markdown supported)
  --rich-text <richText>    Rich-text JSON array (e.g. [{"type":"text","text":"hello"}])
  --mode <mode>             Session mode: "auto" or "manual"
  -h, --help                display help for command
```

## publish

```
Usage: gobi brain publish [options]

Upload BRAIN.md to the vault root on webdrive. Triggers post-processing (brain sync, metadata update, Discord notification).

Options:
  -h, --help  display help for command
```

## unpublish

```
Usage: gobi brain unpublish [options]

Delete BRAIN.md from the vault on webdrive.

Options:
  -h, --help  display help for command
```

## list-updates

```
Usage: gobi brain list-updates [options]

List recent brain updates. Without --space-slug, lists all updates for you. With --space-slug, lists updates for that space. Use --mine to show only updates by you.

Options:
  --vault-slug <vaultSlug>  Vault slug (overrides .gobi/settings.yaml)
  --space-slug <spaceSlug>  List updates for a space
  --mine                    List only my own brain updates
  --limit <number>          Items per page (default: "20")
  --cursor <string>         Pagination cursor from previous response
  -h, --help                display help for command
```

## post-update

```
Usage: gobi brain post-update [options]

Post a brain update for a vault.

Options:
  --vault-slug <vaultSlug>  Vault slug (overrides .gobi/settings.yaml)
  --title <title>           Title of the update
  --content <content>       Update content (markdown supported)
  --auto-attachments        Upload wiki-linked [[files]] to webdrive before posting
  -h, --help                display help for command
```

## edit-update

```
Usage: gobi brain edit-update [options] <updateId>

Edit a published brain update. You must be the author.

Options:
  --title <title>           New title for the update
  --content <content>       New content for the update (markdown supported)
  --vault-slug <vaultSlug>  Vault slug for attachment uploads (overrides .gobi/settings.yaml)
  --auto-attachments        Upload wiki-linked [[files]] to webdrive before editing
  -h, --help                display help for command
```

## delete-update

```
Usage: gobi brain delete-update [options] <updateId>

Delete a published brain update. You must be the author.

Options:
  -h, --help  display help for command
```
