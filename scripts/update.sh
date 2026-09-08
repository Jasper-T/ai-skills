#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

# Validate installer arguments before any Git operation.
args=("$@")
while (($# > 0)); do
  case "$1" in
    --link|--copy|--force) ;;
    --target)
      if (($# < 2)) || [[ -z "$2" || "$2" == --* ]]; then
        printf 'Error: --target requires a path.\n' >&2
        exit 2
      fi
      shift
      ;;
    -h|--help)
      printf 'Usage: ./scripts/update.sh [--link|--copy] [--target PATH] [--force]\n'
      printf 'Fast-forward the current branch, then install Skills.\n'
      exit 0
      ;;
    *)
      printf 'Error: unknown option: %s\n' "$1" >&2
      exit 2
      ;;
  esac
  shift
done

if ! git_root="$(git -C "$repo_root" rev-parse --show-toplevel 2>/dev/null)" ||
   [[ "$(cd "$git_root" && pwd -P)" != "$(cd "$repo_root" && pwd -P)" ]]; then
  printf 'Error: %s is not a Git working-tree root. Clone the repository before updating.\n' "$repo_root" >&2
  exit 1
fi

if ! branch="$(git -C "$repo_root" symbolic-ref --quiet --short HEAD)"; then
  printf 'Error: detached HEAD; select a branch before updating.\n' >&2
  exit 1
fi
if ! upstream="$(git -C "$repo_root" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null)"; then
  printf 'Error: branch %s has no upstream; configure the intended upstream before updating.\n' "$branch" >&2
  exit 1
fi

if [[ -n "$(git -C "$repo_root" status --porcelain)" ]]; then
  printf 'Error: the repository has uncommitted changes. Commit or preserve them before pulling.\n' >&2
  git -C "$repo_root" status --short >&2
  exit 1
fi

printf 'Updating %s from %s\n' "$branch" "$upstream"
git -C "$repo_root" pull --ff-only
exec "$repo_root/scripts/install.sh" ${args[@]+"${args[@]}"}
