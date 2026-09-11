---
name: code-modification
description: Require read-only analysis, a numbered change plan, and explicit scope approval before intentional project modifications. Use for implementation or maintenance requests that would change project state; do not use for review, explanation, diagnosis, or other read-only work.
---

# Controlled Code Modification

Use this skill as a planning and write-authorization layer. It controls what may be changed, not the detailed implementation, testing, or verification procedure Codex uses after approval.

## Core Rules

1. Before any intended project write, inspect enough relevant state with read-only operations to understand the request and required change.
2. Unless the user explicitly invokes the bypass below, present a concise numbered modification plan and wait for approval before writing.
3. The original implementation request is not approval of the later plan. Only explicit acceptance of the plan, selected item numbers, and any chosen approach authorizes those writes.
4. Treat the user's requested approach as the default. Never silently replace it with a preferred alternative.
5. The approved items and approach define the write boundary. Do not add adjacent cleanup, refactoring, dependency changes, public-interface changes, configuration changes, documentation changes, new files, or other project modifications unless the approved plan covers them.
6. If execution reveals a materially new or changed project write, stop before that write, present a supplemental numbered plan, and wait for approval.
7. Do not use this skill to prescribe Codex's normal implementation or verification workflow. Tests, linting, type checks, and other routine verification may run as Codex normally determines. Intentional changes to tests, snapshots, fixtures, generated tracked outputs, or other durable project artifacts are writes and must fall within the approved scope; incidental local caches or build artifacts are not separate scope items unless they materially affect project state.

## Read-Only Analysis

Understand the requested behavior, the user's constraints and chosen approach, and the relevant existing implementation. Trace the modification and impact chain far enough to identify the smallest coherent write set, including affected interfaces, callers, configuration, dependencies, or project structure when they materially influence the change.

Remain read-only when the user asks only for review, explanation, diagnosis, or a plan. Do not seek write approval unless implementation is requested.

## Numbered Modification Plan

Before writing, present a concise numbered plan. Each item should identify the intended target and concrete change, with enough implementation approach and scope boundary for the user to know what they are authorizing.

Include important exclusions only when they prevent scope ambiguity. Do not turn the plan into a general engineering checklist or testing specification.

Ask the user to approve all items, approve selected item numbers, or choose between materially different approaches. If the user changes the plan, restate the resulting write scope when needed before seeking approval.

## User Approach and Alternatives

Preserve the user's requested approach unless it is infeasible, unsafe, or the user chooses another option. If a materially better alternative exists, present it separately and explain the meaningful tradeoff, then let the user choose. Do not add alternatives for minor or subjective differences.

If the requested approach is infeasible or unsafe, explain the concrete issue and offer the nearest feasible option. Do not write until an authorized path is clear.

## Authorized Execution

After approval, treat the approved item numbers and chosen approach as the execution boundary. Resolve ordinary implementation details freely when they do not change the authorized behavior or expand the intended project writes, and preserve unrelated user work.

If an approved item cannot be completed within its authorized scope, stop writing that item and propose the changed or additional write as a supplemental plan. Other approved work may continue only when it is independent of that decision.

## Explicit Bypass

The user may explicitly waive the visible plan or confirmation step with instructions such as “直接改”, “不用 plan”, “不用确认”, or an equally clear statement. In that case, still inspect enough context to understand the target, infer the narrowest reasonable write scope from the request, and execute without pausing for plan approval.

Do not infer a bypass from urgency or a generic request such as “fix this”. A bypass does not override platform safeguards, tool-required confirmations, or higher-priority safety requirements.

## Keep Planning Out of Project Artifacts

Keep modification plans, approval history, rejected alternatives, progress narration, and task-specific implementation commentary in the conversation. Write them into project artifacts only when the user explicitly requests persistent documentation such as an ADR, changelog, or decision record.
