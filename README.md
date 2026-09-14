# AI Agents

这个仓库维护我的 AI Agent、Skill 和相关维护说明，是这些能力的唯一源码仓库。GitHub 仓库地址仍为 `Jasper-T/ai-skills`。

## 结构与职责

| 位置 | 职责 |
| --- | --- |
| [agents/](agents/) | 面向完整目标的工作流编排，目前包含 [coding-agent](agents/coding-agent/AGENT.md) |
| [skills/](skills/) | 独立、可复用的能力或工作流 |
| [docs/](docs/) | 设计或维护说明，目前包含 [Skill 安装与维护](docs/maintenance.md) |
| [AGENTS.md](AGENTS.md) | 维护本仓库时适用的 Skill 设计执行规则 |
| [scripts/](scripts/) 与 [tests/](tests/) | 已有的 Skill 安装、同步、检查工具及验证用例 |

Agent 面向完整目标，组织多个能力完成任务；Skill 面向单一、可复用的能力或工作流。使用 coding-agent 时读取其 `AGENT.md`；现有安装脚本只安装 Skills。

当前 Skills：

- [change-planning](skills/change-planning/SKILL.md)：修改前规划和范围确认。
- [git-commit-message](skills/git-commit-message/SKILL.md)：生成和检查 Conventional Commits 提交消息。
- [skill-repo-sync](skills/skill-repo-sync/SKILL.md)：维护 Skill 源码、安装及同步。

## Skill 设计原则

1. **只写模型默认不会稳定做到的事**：规则应补足实际行为缺口。
2. **只保留特有信息**：优先记录非显然约束、明确决策和工作流边界。
3. **保持最小必要信息量**：删除不会实质改善行为的指令。
4. **保持职责边界清晰**：每个 Skill 负责一个能清楚描述的能力或工作流。
5. **只固化值得固化的问题**：针对反复出现的问题、非显然约束或高代价失误增加规则。
6. **约束必要结果，不干预无关过程**：只有过程本身重要时才规定实现步骤。

## 安装与维护

```bash
git clone git@github.com:Jasper-T/ai-skills.git
cd ai-skills
./scripts/install.sh
```

默认以符号链接安装到 `${CODEX_HOME:-$HOME/.codex}/skills`；后续运行 `./scripts/update.sh` 快进同步并安装新增 Skill。

复制安装、自定义目录、冲突恢复、安装检查与验证命令见 [Skill 安装与维护](docs/maintenance.md)。
