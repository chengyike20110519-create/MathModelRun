# MyMathModelAgent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Skills: Codex & Claude Code](https://img.shields.io/badge/skills-Codex%20%7C%20Claude%20Code-green.svg)](AGENTS.md)

> 一个**证据驱动的数学建模竞赛 Agent Skill**。把选题、题意分析、模型设计、代码实验、证据冻结、图表、论文写作和最终审计统一为一条可复现流水线。

适用于 CUMCM、MCM/ICM、HiMCM、华为杯、华数杯、电工杯等数学建模竞赛。

---

## 核心能力

- **10 阶段状态机工作流**：从输入预检到双重审计，禁止跳过验证与审计。
- **证据优先**：论文数字只能从 `frozen_numbers.json` 读取，结果可溯源。
- **多模型路由**：每道子题都有 baseline、primary、rejected、fallback 与验证计划。
- **多执行引擎**：Python / AMPL / Typst / LaTeX 任选，优化问题自动检查 `solve_result`。
- **双平台兼容**：同时支持 Codex 的 `my-mathmodel-agent` Skill 与 Claude Code 的 `.claude/skills/my-mathmodel-agent` Skill。
- **开箱工具**：项目脚手架、环境诊断、结果冻结、工作区审计、仓库自检。

---

## 安装

### 方式一：npx 一键安装（推荐）

```bash
npx -y skills@latest add <your-github-username>/MyMathModelAgent --skill '*' --agent codex claude-code
```

### 方式二：Git 克隆到 Codex Skills 目录

```bash
# macOS / Linux
git clone https://github.com/<your-github-username>/MyMathModelAgent.git \
  ~/.codex/skills/my-mathmodel-agent

# Windows (PowerShell)
git clone https://github.com/<your-github-username>/MyMathModelAgent.git \
  %USERPROFILE%\.codex\skills\my-mathmodel-agent
```

### 方式三：Git 克隆到 Claude Code Skills 目录

```bash
git clone https://github.com/<your-github-username>/MyMathModelAgent.git \
  ~/.claude/skills/my-mathmodel-agent
```

### 方式四：手动复制

下载 ZIP 后，把仓库复制到对应工具的 skills 目录即可。

> 安装后重启 Codex / Claude Code，让新 skill 被发现。

---

## 快速开始

### 1. 脚手架新建赛题项目

```bash
python3 my-mathmodel-agent/scripts/init_project.py 2026-himcm-demo
```

这会生成标准目录结构：

```text
2026-himcm-demo/
├── problem_files/        # 题面和附件
├── planning/             # 选题、路线、评分
├── methods/              # 模型假设、公式、PoC
├── code/                 # Python / AMPL 代码
├── data_cleaned/         # 清洗后的数据
├── results/              # 运行结果、指标、日志
├── figures/              # 图表
├── paper/                # Typst / LaTeX 论文
├── audit/                # 审计报告
├── frozen_numbers.json   # 冻结数字
├── project_manifest.json # 项目元数据
└── state.json            # 当前阶段与门禁
```

### 2. 放入赛题文件

把官方 PDF、Excel、CSV 等复制到 `2026-himcm-demo/problem_files/`。

### 3. 调用 Agent Skill

- **Codex**:
  ```text
  使用 $my-mathmodel-agent 完成 2026-himcm-demo 的数学建模
  ```

- **Claude Code**:
  ```text
  /my-mathmodel-agent 开始处理 2026-himcm-demo
  ```

### 4. 审计与交付

最终由 `audit_workspace.py` 生成 `audit/final_report.md`，零硬错误后进入 `READY` 状态。

---

## 仓库结构

```text
MyMathModelAgent/
├── README.md                         # 本文件
├── AGENTS.md                         # 通用 Agent 入口
├── LICENSE                           # MIT
├── .gitignore
├── .codex-plugin/
│   └── plugin.json                   # Codex plugin 元数据
├── my-mathmodel-agent/               # Codex Skill
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/workflow-contract.md
│   └── scripts/
│       ├── init_project.py
│       ├── doctor.py
│       ├── freeze_numbers.py
│       └── audit_workspace.py
├── .claude/skills/my-mathmodel-agent/ # Claude Code Skill 镜像
│   ├── SKILL.md
│   └── agents/                       # 角色子 Agent 提示词
├── docs/                             # 详细文档
├── templates/                        # 项目模板与论文模板
└── tests/                            # 回归测试
```

---

## 文档

| 文档 | 说明 |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | 详细安装与配置 |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | 10 阶段工作流与门禁 |
| [docs/CONTRIBUTE.md](docs/CONTRIBUTE.md) | 贡献指南 |
| [my-mathmodel-agent/references/workflow-contract.md](my-mathmodel-agent/references/workflow-contract.md) | 阶段契约与产物规范 |

---

## 常用脚本

| 脚本 | 用途 |
|---|---|
| `my-mathmodel-agent/scripts/init_project.py` | 新建赛题项目 |
| `my-mathmodel-agent/scripts/doctor.py` | 环境诊断 |
| `my-mathmodel-agent/scripts/freeze_numbers.py` | 冻结结果 |
| `my-mathmodel-agent/scripts/audit_workspace.py` | 工作区审计 |
| `scripts/validate_repo.py` | 仓库结构自检 |

---

## 贡献

欢迎提交 Issue 与 PR。请先阅读 [docs/CONTRIBUTE.md](docs/CONTRIBUTE.md)。

---

## License

[MIT](LICENSE) © MyMathModelAgent contributors
