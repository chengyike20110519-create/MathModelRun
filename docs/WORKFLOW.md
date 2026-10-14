# MathModel Run 工作流

目标：建立“题面事实 → 判断 → 模型 → 验证 → 证据 → 局部写作 → 论文 → 审计”的可复现闭环，而不是默认一键生成整篇文章。

## 默认工作方式

每轮先回答“现在最需要做哪个判断”，再决定是否运行代码或写文字。系统默认输出一个小型工作包，而不是整篇论文：

- 当前瓶颈：第一个未通过门禁是什么；
- 阻塞原因：为什么不能直接进入下一阶段；
- 下一步动作：一个可在本轮完成的判断或最小实验；
- 通过标准：什么证据足以打开门禁；
- 失败回退：结果不成立时回到哪里。

只有模型路线、数据口径、实验结果和结论完成验证后，才允许整理对应论文段落。除非用户明确要求全文，否则优先产出题意卡、模型决策卡、实验计划、批判报告、结果解释或单个章节。

## 十阶段状态机

```text
S0 PREFLIGHT
  input_manifest.json
      |
      v
S1 ANALYZE
  planning/problem_analysis.json
      |
      v
S2 ROUTE
  methods/model_route.json
      |
      v
S3 DATA_PLAN
  data_cleaned/data_plan.json + figures/visualization_plan.json
      |
      v
S4 METHOD_POC
  methods/method_validation.json + code/poc_*
      |
      v
S5 EXPERIMENT
  results/run_manifest.json + runs/* + figures/*
      |
      v
S6 FREEZE
  frozen_numbers.json
      |
      v
S7 WRITE
  paper/main.tex 或 paper/main.typ + paper/evidence_map.json
      |
      v
S8 RENDER
  paper/main.pdf + paper/render_log.json
      |
      v
S9 AUDIT
  audit/acceptance.json + audit/final_report.md
      |
      v
READY
```

## 每轮固定动作

1. 读取 `state.json`、`project_manifest.json`、`PROGRESS.md` 和当前阶段产物。
2. 找到第一个为 `false` 的门禁，不跳步。
3. 明确本轮产物、验收标准和失败回退点。
4. 生成最小可验证结果。
5. 切换到 Reviewer 视角复现命令、日志、图表或人工检查。
6. 更新 `state.json`、`PROGRESS.md`、`audit/gate_evidence.json`。
7. 写出阶段、产物、证据、风险和精确下一步。

## 阶段与门禁

| 阶段 | 必须完成 | 门禁 |
|---|---|---|
| S0 输入预检 | 题面/附件可读，路径、SHA-256、访问日期、环境完整 | `input_snapshot` |
| S1 题意拆解 | 每问有输入、输出、约束、指标、事实/假设/歧义、验收标准 | `problem_decomposed` |
| S2 模型选路 | 每问有 baseline、primary、fallback、拒绝路线和验证计划 | `model_route_selected` |
| S3 数据图表 | 字段、单位、清洗、泄漏检查、图表目的和脚本明确 | `data_plan_ready` |
| S4 方法 PoC | 符号、假设、目标、约束、算法和最小可运行样例一致 | `method_validated` |
| S5 正式实验 | baseline、primary、消融、敏感性、稳健性、图表都可复现 | `experiments_reproduced` |
| S6 结果冻结 | 论文数字有 name/value/unit/source_file/source_run/subproblem/notes | `results_frozen` |
| S7 证据写作 | 每个 claim、数字、表和图映射到冻结值或运行记录 | `paper_written` |
| S8 渲染检查 | PDF 编译成功并逐页检查，无硬错误 | `pdf_verified` |
| S9 独立审计 | 独立复现证据，硬错误为 0，评分达到门槛 | `audit_passed` |

## 证据类型

每个门禁都要落到可复现证据：

- `command`：命令与退出结果；
- `test`：自动测试通过/失败；
- `data`：来源、字段、行数、哈希或 schema；
- `figure`：生成脚本与输出图；
- `log`：参数、种子、环境、输入哈希、指标；
- `manual`：有路径的人工视觉检查。

## 回退规则

| 失败 | 回到 |
|---|---|
| 题意、范围、输出形式错了 | S1 |
| 模型路线无法辩护 | S2 |
| 字段、单位、清洗或泄漏有问题 | S3 |
| 数学表达和代码不一致，PoC 不可运行 | S4 |
| 运行不可复现、求解状态未验证、指标无来源 | S5 |
| 数字来自旧结果、聊天或截图 | S6 |
| 结论、图表、引用与证据不匹配 | S7 |
| 编译、排版、缺图、乱码、模板不合规 | S8 |
| 审计发现硬错误 | 最早失效阶段 |

## 优秀论文基准（冲奖档）

上面的门禁保证“可交付、可辩护”。要冲奖，还要满足
[../my-mathmodel-agent/references/exemplar-benchmark.md](../my-mathmodel-agent/references/exemplar-benchmark.md)
里的更高一档，它从三篇 2024 HiMCM B 题高分论文（15022 / 15502 / 16226）提炼：

- 核心量要从**可测驱动量**估计并拟合真实数据，而不是拍一个占比区间；
- 按地区 / 能源来源 / 用途 / 时间段**拆解**，不用单一全球平均；
- 预测用**多个结构不同的模型对比** + 诚实的回测误差 + 外部独立预测锚定；
- 论文里放**可检索的数据来源表**（带 URL / 引用），与冻结数字一致；
- 交付件齐全：独立敏感性章节、至少一条建议**真正并入模型并重跑**、技术+政策建议、1–2 页点名对方真实报告的信、规范引用与 AI 使用报告。

## 禁止事项

- 禁止跳过 S4、S6、S9；
- 禁止论文使用未冻结数字；
- 禁止生成者单独批准自己的工作；
- 禁止删除或修改验收标准来让门禁通过；
- 禁止把旧结果文件留着作为隐藏第二答案。

完整契约见 [../my-mathmodel-agent/references/workflow-contract.md](../my-mathmodel-agent/references/workflow-contract.md)。
