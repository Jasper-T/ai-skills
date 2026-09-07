# AI Skills

这是个人 AI Skills 的唯一源码仓库（source of truth）。在一台机器上修改并推送，在其他机器上通过 `git pull` 同步；Codex 等客户端从本仓库安装或链接 Skills。

## 仓库结构

```text
ai-skills/
├── README.md
├── scripts/
│   ├── install.sh        # 安装或链接仓库内的 Skills
│   └── update.sh         # 快进拉取后重新安装
└── skills/
    └── skill-repo-sync/  # 维护本仓库的工作流 Skill
        ├── SKILL.md
        └── agents/openai.yaml
```

## 在新机器上安装

```bash
git clone git@github.com:Jasper-T/ai-skills.git
cd ai-skills
./scripts/install.sh
```

默认安装位置是 `${CODEX_HOME:-$HOME/.codex}/skills`。安装脚本默认创建符号链接，适合需要持续编辑 Skills 的机器：仓库更新后，已链接的 Skill 会立即生效，新增加的 Skill 会在下次运行安装脚本时加入。

如果客户端不支持符号链接，可以复制安装：

```bash
./scripts/install.sh --copy
```

自定义目标目录：

```bash
./scripts/install.sh --target /path/to/skills
```

若目标位置已有同名内容，脚本会停止并保留原文件。确认要替换时可加 `--force`；原内容会先移动到带时间戳的备份路径，而不是直接删除。

## 同步更新

```bash
cd ai-skills
./scripts/update.sh
```

更新脚本仅执行快进合并（`git pull --ff-only`），并拒绝在仓库有未提交更改时拉取，避免覆盖本地工作。复制安装模式需要显式更新目标副本：

```bash
./scripts/update.sh --copy --force
```

## 新增或修改 Skill

1. 在 `skills/<skill-name>/` 下创建或编辑 `SKILL.md` 及必要资源。
2. 验证 Skill，确保 frontmatter、名称和资源引用有效。
3. 运行 `./scripts/install.sh`，让新 Skill 在本机可用。
4. 检查 `git status` 和 `git diff`，确认没有密钥、令牌或机器私有配置。
5. 提交并推送；其他机器运行 `./scripts/update.sh`。

推荐保持每个提交只做一件事，例如：

```bash
git add skills/my-skill
git commit -m "feat(my-skill): add initial workflow"
git push
```

## 约定

- 只在本仓库的 `skills/` 下维护源码，不把客户端安装目录当作独立副本编辑。
- 不提交密码、API 密钥、访问令牌、私有证书或机器专属路径。
- 不使用强制推送、自动重置或自动清理来解决同步冲突；先保留现场并人工决定。
- 仓库默认保持私有；发布通用 Skill 时再单独评估公开范围和许可。
