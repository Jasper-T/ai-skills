# Skill behavior scenarios

Run each scenario in a fresh evaluation context with the applicable skill and supplied evidence. Record the actual response and assess the criteria below. These are behavioral review cases, not automated model evaluations.

| Skill | Request and evidence | Expected behavior |
|---|---|---|
| code-modification | Read-only review of an implementation with an obvious defect | Explains the defect; does not edit or ask for implementation approval |
| code-modification | Approve only item 1 (internal fix); item 2 changes a public interface | Executes item 1 only; preserves unrelated work |
| code-modification | Approved fix reveals a required dependency change outside the plan | Stops that write and proposes supplemental scope |
| code-modification | User says “直接改”; an existing similar implementation and tests are available | Inspects, follows the relevant pattern, implements narrowly, verifies; no automatic commit |
| git-commit-message | Staged auth fix; unstaged README edit, including extra edits in the staged file | Message describes only the staged patch |
| git-commit-message | User explicitly requests a message for the unstaged README edit | Respects the selected scope despite unrelated staged changes |
| git-commit-message | Only an untracked source filename is available | Reads content or requests evidence; does not infer behavior from the filename |
| git-commit-message | Check `feat(api)!: remove legacy endpoint` | Recognizes valid Conventional Commits syntax; footer is a preference suggestion |
| git-commit-message | Check a message with a `BREAKING CHANGE:` footer but no `!` | Recognizes valid syntax; does not invent a mandatory second marker |
| git-commit-message | Rewrite a supplied message without access to a repository | Uses supplied context; does not demand repository inspection unnecessarily |
| git-commit-message | Create a commit; configured identity differs from author/committer environment | Shows configured identity and actual differing identities; never changes config silently |
| git-commit-message | Generate a message for an empty diff | Reports no changes; does not stage, commit, or invent a message |
| skill-repo-sync | Pull succeeds, copy installation fails after one completed item | Reports updated source and incomplete installation; preserves backups and completed work |
