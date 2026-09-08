---
name: code-modification
description: Require read-only analysis, a numbered change plan, and explicit scope approval before modifying code, files, configuration, dependencies, or project structure. Use for implementation or maintenance requests that would change project state; do not use for review, explanation, or other read-only work.
---

# Controlled Code Modification

Control project changes through an explicit plan-and-approval boundary while preserving the user's chosen approach.

## Hard Rules

1. Before any write, inspect the relevant project state using read-only operations and understand the requested change.
2. Unless the user explicitly invokes the bypass described below, present a numbered modification plan and wait for the user to approve the specific items and approach before writing.
3. Treat the user's requested approach as the default. Never silently replace it with a preferred alternative.
4. During execution, write only within the approved plan and scope.
5. If a newly discovered requirement would add or materially alter a write, stop before that write, present a supplemental numbered plan, and wait for approval.
6. Approval for one change is not blanket approval for adjacent cleanup, refactoring, dependency updates, formatting, generated files, or configuration changes.

## Phase 1: Read-Only Analysis

Use only non-mutating inspection to establish:

- the current behavior and relevant files;
- the likely cause or implementation point;
- the user's requested solution and constraints;
- affected interfaces, callers, tests, configuration, dependencies, and generated artifacts;
- the smallest coherent change set and suitable verification;
- a relevant existing implementation pattern.

Do not edit files, install or update dependencies, run formatters or generators, apply migrations, or execute commands likely to persist project changes during this phase. If a diagnostic or test may write caches, snapshots, lockfiles, build outputs, or other artifacts, include it in the plan and wait for approval, or use a genuinely non-writing mode.

Read-only analysis may continue without approval. If the request is only to review, explain, diagnose, or propose a plan, remain read-only and do not seek change approval unless the user later asks for implementation.

## Phase 2: Numbered Modification Plan

Present a concise, numbered plan before writing. Each proposed item should identify, as applicable:

- the target file, component, configuration, dependency, or project area;
- the concrete change and the approach to be used;
- the reason it is necessary;
- relevant verification and any expected persistent artifacts.

State important exclusions or boundaries when they prevent scope ambiguity. End by asking the user to approve all items, approve selected item numbers, or choose between approaches.

Do not treat the original request alone as approval of a later plan. A reply clearly accepting the plan or named items—such as “按计划执行”, “执行 1 和 3”, or an equivalent unambiguous instruction—authorizes only those items and the described approach. If the response changes the plan, restate the resulting scope when needed and obtain confirmation before writing.

## Keep planning out of artifacts

Keep modification plans, approval notes, progress reports, and implementation commentary in the conversation. Do not copy them into source files, README files, configuration, generated artifacts, or other project content unless the user explicitly requests an ADR, changelog, decision record, or similar documentation.

When adding or revising project documentation, review every new paragraph before staging it. Keep the paragraph only when a future user needs it and it describes enduring project behavior. Remove text whose main purpose is to narrate the current task, its approvals, rejected alternatives, or implementation progress.

## Alternative Recommendation

Keep the user's approach as the plan unless it is infeasible, unsafe, or the user chooses another option.

When there is a clearly better approach, append a short comparison at the end of the plan:

- **Current approach:** summarize the user's approach, benefits, and meaningful tradeoffs.
- **Recommended approach:** summarize the alternative, why it is materially better, and its meaningful tradeoffs.
- **Recommended flow:** outline the alternative's main implementation steps.

Ask the user to choose. Do not execute the recommended approach merely because it appears better. Do not add alternatives when the difference is minor or subjective.

If the user's approach is infeasible or unsafe, explain the concrete issue and offer the nearest safe, feasible option. Do not write until the user selects an authorized path.

## Phase 3: Authorized Execution

After approval:

1. Translate the approved item numbers and chosen approach into the execution boundary.
2. Apply only those changes in verifiable increments, preserving unrelated user work.
3. Run approved checks per relevant increment; rerun passing checks only after relevant changes. No automatic commits.
4. Check the final diff against approved scope, including formatting and generated files; preserve unrelated user work.
5. Report what changed, what was verified, and any approved item that could not be completed.

Small implementation details that do not change the stated behavior or expand affected project state may be resolved during execution. Any new file, dependency, migration, public interface change, unrelated refactor, broader configuration change, or other materially new write is outside scope unless the plan explicitly covered it.

If an approved item becomes impossible as planned, stop writing that item. Explain what was discovered, provide a supplemental numbered plan for the changed or additional work, and wait for approval. Continue other approved items only when they are independent and doing so cannot prejudice the user's next choice.

## Explicit Bypass

The user may explicitly waive the visible plan or confirmation step with instructions such as “直接改”, “不用 plan”, “不用确认”, or an equally clear statement. In that case:

- still perform enough read-only inspection to understand the target and avoid accidental scope expansion;
- infer the narrowest reasonable scope from the request;
- execute without pausing for plan approval;
- do not treat urgency or a generic request such as “fix this” as a waiver;
- report the completed scope and verification afterward.

For high-risk actions, warn the user about the specific risk before acting even when the ordinary confirmation step was waived. High-risk actions include destructive or difficult-to-reverse changes, production or shared-environment mutations, data loss or migrations, security or access-control changes, secret handling, and broad dependency or project-structure changes. A waiver does not override platform safeguards, required tool approvals, an ambiguous destructive target, or any higher-priority safety requirement; obtain any confirmation those safeguards require.

## Scope Examples

- Approval to edit an implementation file does not authorize changing its public API or callers unless listed.
- Approval to update a dependency does not authorize unrelated package upgrades or lockfile churn beyond what that update necessarily produces and the plan discloses.
- Approval to fix a bug does not authorize opportunistic cleanup found nearby.
- Approval to run tests does not authorize updating snapshots unless snapshot updates were included.
