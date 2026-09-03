# 安装指南

本仓库是 Codex / Claude Code 双平台兼容的数学建模 Skill。

## 环境要求

- Python 3.9+
- Git
- 可选：AMPL 与 `amplpy`
- 可选：Typst 或 LaTeX 用于论文编译
- 可选：Pandoc 用于 Word 转换

## 安装方式

### npx 一键安装（推荐）

```bash
npx -y skills@latest add <your-github-username>/MyMathModelAgent --skill '*' --agent codex claude-code
```

### Codex（macOS / Linux）

```bash
git clone https://github.com/<your-github-username>/MyMathModelAgent.git \
  ~/.codex/skills/my-mathmodel-agent
```

### Codex（Windows PowerShell）

```powershell
git clone https://github.com/<your-github-username>/MyMathModelAgent.git `
  "$HOME\.codex\skills\my-mathmodel-agent"
```

### Claude Code（macOS / Linux）

```bash
git clone https://github.com/<your-github-username>/MyMathModelAgent.git \
  ~/.claude/skills/my-mathmodel-agent
```

### Claude Code（Windows PowerShell）

```powershell
git clone https://github.com/<your-github-username>/MyMathModelAgent.git `
  "$HOME\.claude\skills\my-mathmodel-agent"
```

### 项目级安装

也可以只在某个项目里使用：

```bash
mkdir -p my-contest/.claude/skills
git clone https://github.com/<your-github-username>/MyMathModelAgent.git \
  my-contest/.claude/skills/my-mathmodel-agent
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
