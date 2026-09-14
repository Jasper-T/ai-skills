# Coding Agent

Orchestrate software coding and repository modification tasks. Read this workflow when carrying a repository change from scope planning through delivery.

1. Establish the write scope with [change-planning](../../skills/change-planning/SKILL.md). Carry forward an already approved plan; revisit approval only when the required scope materially changes.
2. Implement the approved change using the coding environment's native capabilities. Keep affected documentation in the same change and run the repository's relevant verification before final diff review.
3. Review the complete change as a coherent workspace, including additions, deletions, and moves. If review requires edits, repeat the affected verification before delivery.
4. When committing is requested, use [git-commit-message](../../skills/git-commit-message/SKILL.md) after the change and verification are complete. Keep one logical change in one atomic commit; do not create incidental commits while editing.
5. For Skill repository synchronization, use [skill-repo-sync](../../skills/skill-repo-sync/SKILL.md) when applicable. Push only when authorized, then verify worktree and remote state before reporting delivery.
