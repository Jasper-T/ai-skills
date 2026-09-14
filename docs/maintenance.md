# Skill 安装与维护

以下命令均在仓库根目录运行。

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

若目标位置已有同名内容，脚本会停止并保留原文件。确认要替换时可加 `--force`；脚本会先检查全部同名冲突，再开始安装。原内容会移动到安装目录旁的唯一备份目录，例如目标为 `/path/to/skills` 时，备份为 `/path/to/.skills.backups/<skill>.<随机后缀>/original`。目标不能与源码目录重叠。

## 同步更新

```bash
cd ai-skills
./scripts/update.sh
```

更新脚本仅执行快进合并（`git pull --ff-only`），并拒绝在仓库有未提交更改时拉取，避免覆盖本地工作。复制安装模式需要显式更新目标副本：

```bash
./scripts/update.sh --copy --force
```

## 检查安装状态

在仓库目录运行 `python3 scripts/check_installation.py`，检查技能是否缺失、链接是否正确及 `SKILL.md` 是否存在。默认只读；真实目录单独报告，不据此认定副本与源码一致。支持 `--target /path/to/skills`，默认目标与安装脚本一致。

显式运行 `python3 scripts/check_installation.py --prune` 才会清理：仅删除安装目录顶层中指向本仓库 `skills/` 内、目标已不存在的符号链接，删除前重新检查。真实目录、有效链接和其他仓库的链接均保留。安装与更新脚本不会自动清理；缺失技能仍通过 `./scripts/install.sh` 安装。

退出码：`0` 表示检查通过，`1` 表示存在缺失、冲突、待清理链接或需核对的真实目录，`2` 表示参数或检查/清理错误。清理失败时此前已完成的清理保留；脚本不保证并发修改下的原子性，请勿同时修改安装目录。

## 安装失败与恢复

安装不是整个批次的原子操作。运行期失败会报告失败目标、已完成数量及当前备份位置；此前成功的安装会保留。若拉取成功而安装失败，仓库已经更新，应解决目标冲突或权限问题后重新运行安装脚本，不要为此重置 Git。

恢复时先检查输出中的备份路径及当前目标内容。将当前目标（包括部分复制结果）移动到安装扫描范围外的另一个唯一位置，再将对应的 `original` 移回原目标。不要直接覆盖或删除尚未检查的内容；恢复完成后核对文件和链接。备份原本是符号链接时保留的是链接，不是源码快照。

更新脚本支持 Git worktree；要求当前分支配置 upstream，并拒绝 detached HEAD、脏工作区和不能快进的分叉。`--help` 和非法参数会在拉取前处理。

## 验证

使用 Python 3 和 Git 运行 `python3 -m unittest discover -s tests -v`。测试仅操作自动清理的临时目录和本地 Git 仓库，不访问远端服务或真实 Skills 安装目录。默认使用 `/bin/bash`；可通过 `SKILLS_TEST_BASH` 指定另一个 Bash，以分别验证 macOS Bash 3.2 和较新版本。

元数据检查运行 `python3 scripts/validate_skills.py`。这是本仓库使用的简单 YAML 标量和 Markdown 本地链接格式检查，不代替完整 Skill 格式验证。行为评审使用 `tests/skill-scenarios.md`；场景断言需结合模型实际输出判断，不由静态检查冒充通过。

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
