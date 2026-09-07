#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
source_root="$repo_root/skills"
target_root="${CODEX_HOME:-$HOME/.codex}/skills"
install_mode="link"
force=0

usage() {
  printf '%s\n' \
    "Usage: ./scripts/install.sh [--link|--copy] [--target PATH] [--force]" \
    "" \
    "  --link         Create symbolic links (default)." \
    "  --copy         Copy Skill directories." \
    "  --target PATH  Install into PATH instead of the Codex Skills directory." \
    "  --force        Back up and replace an existing destination."
}

while (($# > 0)); do
  case "$1" in
    --link)
      install_mode="link"
      ;;
    --copy)
      install_mode="copy"
      ;;
    --target)
      if (($# < 2)); then
        printf 'Error: --target requires a path.\n' >&2
        exit 2
      fi
      target_root="$2"
      shift
      ;;
    --force)
      force=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Error: unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ ! -d "$source_root" ]]; then
  printf 'Error: Skills source directory not found: %s\n' "$source_root" >&2
  exit 1
fi

mkdir -p "$target_root"

installed=0
skipped=0

for skill_dir in "$source_root"/*; do
  [[ -d "$skill_dir" && -f "$skill_dir/SKILL.md" ]] || continue

  skill_name="$(basename "$skill_dir")"
  destination="$target_root/$skill_name"

  if [[ -L "$destination" && "$install_mode" == "link" ]]; then
    current_target="$(cd "$(dirname "$destination")" && readlink "$destination")"
    if [[ "$current_target" == "$skill_dir" ]]; then
      printf 'Already linked: %s\n' "$skill_name"
      skipped=$((skipped + 1))
      continue
    fi
  fi

  if [[ -e "$destination" || -L "$destination" ]]; then
    if ((force == 0)); then
      printf 'Conflict: %s already exists. Re-run with --force to back it up and replace it.\n' "$destination" >&2
      exit 1
    fi

    backup_path="${destination}.backup.$(date +%Y%m%d%H%M%S)"
    mv "$destination" "$backup_path"
    printf 'Backed up: %s -> %s\n' "$destination" "$backup_path"
  fi

  if [[ "$install_mode" == "link" ]]; then
    ln -s "$skill_dir" "$destination"
    printf 'Linked: %s\n' "$skill_name"
  else
    cp -R "$skill_dir" "$destination"
    printf 'Copied: %s\n' "$skill_name"
  fi

  installed=$((installed + 1))
done

if ((installed == 0 && skipped == 0)); then
  printf 'No Skills found under %s\n' "$source_root" >&2
  exit 1
fi

printf 'Done: %d installed, %d already current.\n' "$installed" "$skipped"
