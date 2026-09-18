# 安装指南

本仓库包含两个 Codex / Claude Code 双平台兼容的 Skill：

- `my-mathmodel-agent`：完整的数学建模比赛工作流；
- `paper-iteration-pack`：把论文建议转化为图表、排版和渲染迭代的通用 Skill。

## 环境要求

- Python 3.9+
- Git
- 可选：AMPL 与 `amplpy`
- 可选：Typst 或 LaTeX 用于论文编译
- 可选：Pandoc 用于 Word 转换

## 安装方式

### npx 一键安装（推荐）

```bash
npx -y skills@latest add chengyike20110519-create/MathModelRun --skill '*' --agent codex claude-code
```

只安装论文迭代包：

```bash
npx -y skills@latest add chengyike20110519-create/MathModelRun \
  --skill paper-iteration-pack --agent codex claude-code
```

只安装完整数模工作流：

```bash
npx -y skills@latest add chengyike20110519-create/MathModelRun \
  --skill my-mathmodel-agent --agent codex claude-code
```

### Codex（macOS / Linux）

```bash
git clone https://github.com/chengyike20110519-create/MathModelRun.git \
  ~/.codex/skills/my-mathmodel-agent
```

### Codex（Windows PowerShell）

```powershell
git clone https://github.com/chengyike20110519-create/MathModelRun.git `
  "$HOME\.codex\skills\my-mathmodel-agent"
```

### Claude Code（macOS / Linux）

```bash
git clone https://github.com/chengyike20110519-create/MathModelRun.git \
  ~/.claude/skills/my-mathmodel-agent
```

### Claude Code（Windows PowerShell）

```powershell
git clone https://github.com/chengyike20110519-create/MathModelRun.git `
  "$HOME\.claude\skills\my-mathmodel-agent"
```

### 项目级安装

也可以只在某个项目里使用：

```bash
mkdir -p my-contest/.claude/skills
git clone https://github.com/chengyike20110519-create/MathModelRun.git \
  my-contest/.claude/skills/my-mathmodel-agent
```

### 手动安装论文迭代 Skill

`paper-iteration-pack` 是仓库中的独立 Skill。先取得仓库，再把它放到目标 Agent 的
skills 目录中：

```bash
git clone --depth 1 https://github.com/chengyike20110519-create/MathModelRun.git \
  /tmp/MathModelRun
mkdir -p ~/.codex/skills ~/.claude/skills
cp -R /tmp/MathModelRun/skills/paper-iteration-pack ~/.codex/skills/
cp -R /tmp/MathModelRun/skills/paper-iteration-pack ~/.claude/skills/
```

## 环境诊断

安装后运行诊断脚本：

```bash
python3 my-mathmodel-agent/scripts/doctor.py
```

可选参数：

- `--skip-tools`：跳过外部工具检查
- `--competition cumcm|mcm|himcm`：按竞赛类型检查模板

## 安装科学计算依赖

如果要运行示例或完整实验，安装依赖：

```bash
python3 -m pip install -r templates/shared/requirements.txt
```

## 卸载

删除对应 skills 目录即可：

```bash
# Codex
rm -rf ~/.codex/skills/my-mathmodel-agent

# Claude Code
rm -rf ~/.claude/skills/my-mathmodel-agent
```
