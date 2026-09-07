#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

if [[ ! -d "$repo_root/.git" ]]; then
  printf 'Error: %s is not a Git repository. Clone the repository before updating.\n' "$repo_root" >&2
  exit 1
fi

if [[ -n "$(git -C "$repo_root" status --porcelain)" ]]; then
  printf 'Error: the repository has uncommitted changes. Commit or preserve them before pulling.\n' >&2
  git -C "$repo_root" status --short >&2
  exit 1
fi

git -C "$repo_root" pull --ff-only
exec "$repo_root/scripts/install.sh" "$@"
