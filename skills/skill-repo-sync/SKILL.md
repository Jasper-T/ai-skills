---
name: skill-repo-sync
description: Maintain a GitHub-backed source-of-truth repository for personal AI Skills across machines. Use when initializing, cloning, installing, syncing, updating, or versioning a Skills repository; do not use for publishing secrets or silently overwriting local Skills.
---

# Skill Repository Sync

Keep one Git repository as the editable source of truth. Treat client Skill directories as installations derived from that repository, not as independent sources.

## Identify the operation

Determine whether the user needs to:

- initialize and publish a repository;
- clone it onto another machine;
- install or relink Skills into a client;
- pull updates safely;
- add or revise a Skill and version the change;
- diagnose divergence or an installation conflict.

Inspect the repository, current branch, remote, working-tree state, and target Skill directory before changing anything. Preserve the user's repository host, visibility, install location, and requested workflow when specified.

## Initialize a repository

For a new personal repository, use this minimal structure unless the user needs more:

```text
README.md
scripts/install.sh
scripts/update.sh
skills/<skill-name>/SKILL.md
```

Default to a private GitHub repository when visibility is unspecified because Skills may encode personal workflows. Do not create the remote or push until the user has authorized those external changes. Initialize the local repository on `main`, add the remote, review the complete initial diff, commit, and push.

Document the exact clone URL and first-machine/new-machine commands in the README. Keep credentials, tokens, private certificates, `.env` files, and machine-specific state out of version control.

## Keep repository artifacts durable

Write repository files for future users, not as a transcript of the current task. Include only durable operating instructions, interfaces, commands, constraints, and information needed to maintain the repository.

Keep migration commentary, approval history, progress reports, rejected alternatives, and explanations of what was excluded in the conversation unless the user explicitly requests an ADR, changelog, decision record, or similar artifact. Before committing documentation, remove any sentence whose main purpose is to explain this turn's planning or decisions rather than the repository's enduring behavior.

## Install Skills

Prefer the repository's `scripts/install.sh` when present.

- Use symbolic links by default on machines where the repository will be edited. This keeps installed Skills current without duplicate sources.
- Use copy mode only when the client cannot follow symbolic links or when the user requests an isolated snapshot.
- Never overwrite an existing destination silently. Stop and show the conflict, or use the repository's explicit backup-and-replace option after authorization.
- Keep the repository's directory names aligned with each Skill's frontmatter name.

After installation, verify that each destination exists and that linked paths resolve to the repository copy.

## Sync and update

Prefer the repository's `scripts/update.sh` when present. Before pulling:

1. Check for uncommitted and untracked changes.
2. Check the active branch and configured upstream.
3. Pull with fast-forward-only behavior.
4. Re-run installation so newly added Skills become available.

If the working tree is dirty, branches have diverged, or a merge conflict appears, stop and preserve the current state. Explain the choices; do not automatically stash, reset, clean, rewrite history, or force-push.

## Add or update a Skill

Edit the canonical copy under `skills/`. Keep `SKILL.md` concise and place only genuinely reusable scripts, references, or assets beside it. Validate a new or substantially revised Skill with the available Skill validator, and run any added helper script through a meaningful non-destructive test.

Before committing:

- review status and the complete diff;
- confirm no secret or machine-specific file is included;
- review each new documentation paragraph and keep it only when a future user needs it and it describes enduring behavior;
- include only the intended Skill and supporting repository changes;
- use a focused commit message, preferably Conventional Commits when that matches the repository;
- push only when the user asked to publish or sync the change.

On another machine, clone once, run the installer, and use the updater thereafter.

## Safety boundaries

- Never make the installed directory a second editable source of truth.
- Never expose a private repository, add collaborators, change permissions, or publish a Skill without explicit authorization.
- Never resolve sync problems through destructive Git commands unless the user explicitly selects that recovery path after seeing what will be lost.
- Prefer backups over deletion when replacing an installed Skill.
