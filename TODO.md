# 待评估方向

这里记录可能值得评估的方向，不是既定 roadmap，也不承诺实施或完成日期。只有实际使用中出现重复需求、明确收益或现有结构开始产生摩擦时，才将条目升级为实施计划。

状态：`Idea` 候选想法；`Evaluate` 正在评估需求与收益；`Planned` 已确认实施范围。条目不必依次推进。

- **Idea · 独立 Tool 抽象**：若仓库级脚本演化为多个具有稳定接口、独立测试或多 backend 的可复用能力，再考虑从 `scripts/` 抽象出顶层 `tools/`。`skill-installer`、`repo-validator`、`codex-config-sync`、`release-helper` 仅为候选示例，不代表当前需要创建。
- **Idea · Agent 设计规范**：若 Agent 数量与使用模式增加，再根据实际共性总结 `agent-design` 规范，当前不提前创建。
- **Idea · 全局指令同步**：若跨机器同步 Global Codex instructions 成为真实需求，再评估 config、dotfiles、symlink 与 install 方案，当前不提前实现。
