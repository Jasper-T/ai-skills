---
name: git-commit-message
description: Generate, rewrite, or check Git commit messages using Conventional Commits. Use whenever the user asks AI to write, improve, normalize, review, or validate a commit message.
---

# Git Commit Message

Write clear, focused Git commit messages that describe the actual change and follow the repository's established conventions. If the repository defines its own commit rules, follow them; otherwise use the rules below.

## Format

Use Conventional Commits:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

Only the first line is required. `scope`, `body`, and `footer` are optional.

## Choose the type

- `feat`: introduce a new feature or capability
- `fix`: correct a bug
- `docs`: change documentation only
- `style`: change formatting without affecting behavior
- `refactor`: restructure code without adding a feature or fixing a bug
- `perf`: improve performance
- `test`: add or change tests
- `build`: change the build system or dependencies
- `ci`: change continuous-integration configuration or workflows
- `chore`: perform maintenance not covered by another type
- `revert`: revert an earlier commit

Choose the most specific type supported by the primary purpose of the change. Do not use `chore` merely because the correct type is uncertain.

## Decide whether to use a scope

Use a short, stable module or component name when it makes the affected area clearer:

```text
fix(auth): refresh expired access tokens
feat(api): add batch prediction endpoint
```

The scope is optional. It may be omitted for small projects or changes whose scope is already obvious:

```text
docs: clarify installation steps
```

For medium or large projects, prefer a scope when the repository has recognizable modules. Do not invent or force a scope when no meaningful one exists, and do not use a long file path as the scope.

## Write the subject

- Describe one coherent change. A commit should be independently understandable and, as far as practical, independently reversible.
- Keep the subject concise and specific.
- Prefer an action expression such as `add`, `fix`, `remove`, `prevent`, `rename`, or `support`.
- Describe the result or behavior, not the editing activity.
- Avoid low-information subjects such as `update`, `fix bug`, `changes`, or `修改代码`.
- Do not combine unrelated work with wording such as `fix bugs and add feature`.

If the provided changes contain multiple independent concerns, recommend splitting them into separate commits and propose one message per commit. Do not conceal unrelated changes inside one broad message.

## Body and footers

Add a body only when the subject does not adequately explain important context, motivation, or consequences. Focus on why the change was needed and any non-obvious behavior.

For an incompatible change, add `!` before the colon and include a `BREAKING CHANGE:` footer that explains the impact. Include migration guidance when it is known:

```text
feat(api)!: change prediction response format

BREAKING CHANGE: `result` is now returned as an array.
```

Use a footer to associate an issue or pull request when relevant:

```text
fix(auth): refresh expired access tokens

Closes #123
```

Use the repository's preferred footer keyword when one is documented, such as `Closes`, `Fixes`, or `Refs`.

## Handle each request

- **Generate:** inspect the described or available changes, identify the primary purpose, and return the best commit message. Offer alternatives only when the change is genuinely ambiguous.
- **Rewrite:** preserve the original intent while correcting the type, scope, subject, body, or footer. Do not claim details unsupported by the change context.
- **Check:** state whether the message conforms, identify concrete problems, and provide a corrected message when needed.

When evidence about the change is insufficient to write a truthful, specific subject, request the relevant diff or a concise description. Never fabricate behavior, issue numbers, scopes, or breaking-change details.

## Select the change evidence

When drafting from a repository, keep the message tied to one explicit change set:

1. Follow the user's specified diff, paths, revision range, or staged/working-tree selection first. Do not silently broaden that scope.
2. If no scope is specified, inspect repository status and use the staged diff when it contains changes. Do not include unstaged edits, even when they affect the same file.
3. If nothing is staged, use the working-tree changes to draft a message and briefly state that those changes are not staged yet. Do not stage them automatically.
4. For untracked files within the selected scope, read their relevant contents before describing their behavior. A filename or status entry alone is not sufficient evidence.
5. If the selected scope has no changes, report that instead of inventing a message. If a diff is incomplete or cannot be read, disclose the limitation and obtain enough evidence before making specific claims.

Use status and diff summaries to locate changes, then read the relevant full diff. For a supplied message rewrite or check, use the supplied context; repository inspection is needed only when verifying claims requires it. Generating a message from unstaged or untracked content does not make that content part of a future commit.

## Show commit identity before execution

When the user asks to create one or more commits, resolve the effective `user.name` and `user.email` in the current repository once per turn. Immediately before the concrete commit plan, show exactly one concise line:

```text
提交身份：<name> <email>（当前仓库生效配置）
```

If either value is missing, name the missing setting in that line and do not create the commit until the user decides how to proceed. Never modify Git configuration without an explicit request. Omit this identity line when only generating, rewriting, or checking a commit message.

Generating a message does not authorize staging files, creating a commit, pushing changes, or modifying repository history. Perform those actions only when the user explicitly requests them.
