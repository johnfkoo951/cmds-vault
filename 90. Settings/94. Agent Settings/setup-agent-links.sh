#!/usr/bin/env bash
# setup-agent-links.sh — recreate the agent dotfolder symlinks for this vault.
#
# The canonical agent settings live in a normal (synced) folder:
#   90. Settings/94. Agent Settings/claude/
# and .claude/ points at it with RELATIVE symlinks:
#   .claude/agents   -> ../90. Settings/94. Agent Settings/claude/agents
#   .claude/commands -> ../90. Settings/94. Agent Settings/claude/commands
#   .claude/rules    -> ../90. Settings/94. Agent Settings/claude/rules
#   .claude/skills   -> ../90. Settings/94. Agent Settings/claude/skills
# Add a hooks/ folder to the canonical claude/ folder and to LINKS if you use hooks.
#
# Run it once per machine, or again whenever the links are missing
# (ZIP downloads, Windows checkouts, Obsidian Sync copies can flatten them).
# Safe to re-run: correct links are left alone, stray copies are backed up.
#
# Usage:  bash "90. Settings/94. Agent Settings/setup-agent-links.sh" [--check]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
VAULT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
cd "$VAULT"

CANON="90. Settings/94. Agent Settings"
CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

# "<link path>|<canonical path relative to vault root>"
LINKS=(
	".claude/agents|$CANON/claude/agents"
	".claude/commands|$CANON/claude/commands"
	".claude/rules|$CANON/claude/rules"
	".claude/skills|$CANON/claude/skills"
)

stamp="$(date +%Y%m%d-%H%M%S)"
problems=0

for entry in "${LINKS[@]}"; do
	link="${entry%%|*}"
	target="${entry#*|}"
	parent="$(dirname "$link")"
	rel="../$target"

	if [[ ! -d "$target" ]]; then
		if [[ -d "$link" && ! -L "$link" ]]; then
			# Old layout: real folder in the dotfolder, no canonical copy yet.
			if (( CHECK_ONLY )); then
				echo "MIGRATE  $link -> $target (canonical missing)"; problems=$((problems + 1)); continue
			fi
			mkdir -p "$(dirname "$target")"
			mv "$link" "$target"
			echo "moved    $link -> $target"
		else
			echo "MISSING  $target (canonical folder not found — did Sync/ZIP bring it?)" >&2
			problems=$((problems + 1)); continue
		fi
	fi

	if [[ -L "$link" && "$(readlink "$link")" == "$rel" ]]; then
		echo "ok       $link"
		continue
	fi

	if (( CHECK_ONLY )); then
		echo "FIX      $link (should link to $rel)"; problems=$((problems + 1)); continue
	fi

	mkdir -p "$parent"
	if [[ -L "$link" ]]; then
		rm "$link"
	elif [[ -d "$link" ]]; then
		if [[ -z "$(find "$target" -mindepth 1 ! -name .gitkeep ! -name .DS_Store -print -quit)" ]]; then
			# Canonical folder is still an empty placeholder: move the real files in.
			find "$link" -mindepth 1 -maxdepth 1 ! -name .DS_Store -exec mv {} "$target/" \;
			rm -rf "$link"
			echo "moved    $link/* -> $target/"
		elif diff -rq -x .DS_Store -x .gitkeep "$link" "$target" >/dev/null 2>&1; then
			rm -rf "$link"
		else
			mv "$link" "${link}_backup-$stamp"
			echo "backup   $link -> ${link}_backup-$stamp (differs from canonical — merge by hand, then delete)"
		fi
	elif [[ -e "$link" ]]; then
		# A flattened symlink (plain text file holding the path).
		rm "$link"
	fi
	ln -s "$rel" "$link"
	echo "linked   $link -> $rel"
done

# Obsidian Sync and ZIP extraction can drop the executable bit.
if (( ! CHECK_ONLY )); then
	for hooks in "$CANON/claude/hooks" "$CANON/codex/hooks"; do
		[[ -d "$hooks" ]] && find "$hooks" -name '*.sh' -exec chmod +x {} +
	done
fi

for hooks in .claude/hooks .codex/hooks; do
	for f in "$hooks"/*.sh; do
		[[ -e "$f" ]] || continue
		[[ -x "$f" ]] || { echo "NOT EXEC $f" >&2; problems=$((problems + 1)); }
	done
done

if (( problems )); then
	echo "Done with $problems problem(s)." >&2
	exit 1
fi
echo "All agent links are in place."
