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
      if (($# < 2)) || [[ -z "$2" || "$2" == --* ]]; then
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

# Resolve existing symlinks and missing path components without creating anything.
resolve_directory() {
  local path="$1" parent leaf
  if [[ -d "$path" ]]; then
    (cd -P -- "$path" && pwd -P)
  elif [[ -e "$path" || -L "$path" ]]; then
    printf 'Error: not a resolvable directory: %s\n' "$path" >&2
    return 1
  else
    parent="$(dirname -- "$path")"
    leaf="$(basename -- "$path")"
    parent="$(resolve_directory "$parent")" || return 1
    case "$leaf" in
      .) printf '%s\n' "$parent" ;;
      ..) dirname -- "$parent" ;;
      *) printf '%s/%s\n' "${parent%/}" "$leaf" ;;
    esac
  fi
}

source_root="$(resolve_directory "$source_root")"
target_root="$(resolve_directory "$target_root")"
backup_root="$(resolve_directory "$(dirname -- "$target_root")/.$(basename -- "$target_root").backups")"

# Ancestors are unsafe too: replacing an entry there could move the source.
for candidate in "$target_root" "$backup_root"; do
  if [[ "$candidate" == "$source_root" || "$candidate" == "$source_root/"* ||
        "$source_root" == "${candidate%/}/"* ]]; then
    printf 'Error: installation or backup path overlaps Skills source: %s\n' "$candidate" >&2
    exit 1
  fi
done
if [[ "$backup_root" == "$target_root" || "$backup_root" == "$target_root/"* ]]; then
  printf 'Error: backup directory must be outside the installation directory.\n' >&2
  exit 1
fi

skill_dirs=()
destinations=()
actions=()
conflicts=0
for skill_dir in "$source_root"/*; do
  [[ -d "$skill_dir" && -f "$skill_dir/SKILL.md" ]] || continue
  skill_name="$(basename "$skill_dir")"
  destination="$target_root/$skill_name"
  action="install"
  if [[ -L "$destination" && "$install_mode" == "link" ]]; then
    current_target="$(resolve_directory "$destination" 2>/dev/null)" || current_target=""
    expected_target="$(resolve_directory "$skill_dir")"
    if [[ "$current_target" == "$expected_target" ]]; then
      action="skip"
    fi
  fi
  if [[ "$action" != "skip" && ( -e "$destination" || -L "$destination" ) ]]; then
    if ((force == 0)); then
      printf 'Conflict: %s already exists. Use --force to back up and replace it.\n' "$destination" >&2
      conflicts=$((conflicts + 1))
    fi
  fi
  skill_dirs+=("$skill_dir")
  destinations+=("$destination")
  actions+=("$action")
done

if ((${#skill_dirs[@]} == 0)); then
  printf 'No Skills found under %s\n' "$source_root" >&2
  exit 1
fi
if ((conflicts > 0)); then
  printf 'Stopped: %d conflicts; no installation changes made.\n' "$conflicts" >&2
  exit 1
fi

installed=0
skipped=0
active_destination="$target_root"
backup_path=""
report_failure() {
  local status=$?
  printf 'Failed at: %s; %d installed, %d already current. Earlier changes remain.\n' \
    "$active_destination" "$installed" "$skipped" >&2
  if [[ -n "$backup_path" ]]; then
    printf 'Original content preserved at: %s\n' "$backup_path" >&2
  fi
  exit "$status"
}
trap report_failure ERR
mkdir -p "$target_root"

for ((i=0; i<${#skill_dirs[@]}; i++)); do
  skill_dir="${skill_dirs[$i]}"
  destination="${destinations[$i]}"
  skill_name="$(basename "$skill_dir")"
  active_destination="$destination"
  backup_path=""
  if [[ "${actions[$i]}" == "skip" ]]; then
    printf 'Already linked: %s\n' "$skill_name"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ -e "$destination" || -L "$destination" ]]; then
    # Recheck in case a destination appeared after preflight.
    if ((force == 0)); then
      printf 'Error: destination appeared after preflight: %s\n' "$destination" >&2
      false
    fi
    mkdir -p "$backup_root"
    backup_dir="$(mktemp -d "$backup_root/$skill_name.XXXXXXXX")"
    mv "$destination" "$backup_dir/original"
    backup_path="$backup_dir/original"
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

printf 'Done: %d installed, %d already current.\n' "$installed" "$skipped"
