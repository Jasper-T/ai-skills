# Repository instructions

## Skill design

When creating or modifying skills:

- Only encode behavior the model would not reliably infer by default.
- Prefer non-obvious constraints, explicit decisions, and workflow boundaries over generic guidance.
- Minimize instruction cost; remove rules that do not materially improve behavior.
- Keep each skill focused on one clearly describable responsibility.
- Add rules only for recurring issues, non-obvious constraints, or high-cost failures.
- Constrain necessary outcomes rather than implementation details unless the process itself matters.
