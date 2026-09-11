# 数模 Run 工作流契约

这份契约把比赛过程写成一个可恢复的状态机。它的目的不是让步骤看起来很多，而是让每一次“完成”都可证明、可复现、能交接。

## 0. 总原则

1. **先状态，后行动**：每轮先读 `state.json`、`project_manifest.json`、`PROGRESS.md` 和当前阶段产物。
2. **只推进第一个失败门禁**：不能因为后面的任务更有趣，就跳过当前证据缺口。
3. **默认失败**：任何子问题、模型路线、运行记录和门禁默认是 `false` / `pending`。
4. **证据由审查者复现**：生成者可以提交证据，但不能单方面把门禁翻成通过。
5. **数字只从冻结文件进入论文**：正文、图表、摘要和结论都遵守。
6. **失败要回退到最早失效阶段**：不能只改论文措辞掩盖模型、代码或数据问题。
7. **决策有记录**：保留、删除、推迟、换路都要进入 append-only 决策日志。
8. **文件原位更新**：用户要求更新文件时，在原路径替换当前版本；除非明确要求，不创建 `v1`、`v2`、`backup` 或并列旧稿。

## 1. 状态与门禁

推荐的项目状态：

```json
{
  "schema_version": "2.0",
  "project_name": "2026-cumcm-a",
  "contest": "CUMCM",
  "paper_format": "latex",
  "stage": "PREFLIGHT",
  "status": "not_started",
  "next_action": "inspect_problem_files",
  "gates": {
    "input_snapshot": false,
    "problem_decomposed": false,
    "model_route_selected": false,
    "data_plan_ready": false,
    "method_validated": false,
    "experiments_reproduced": false,
    "results_frozen": false,
    "paper_written": false,
    "pdf_verified": false,
    "audit_passed": false
  },
  "budget": {
    "contest_minutes": null,
    "elapsed_minutes": 0,
    "delivery_buffer_minutes": 120
  },
  "updated_at": null
}
```

状态只向后推进，门禁只在证据满足时改变：

```text
PREFLIGHT -> ANALYZE -> ROUTE -> DATA_PLAN -> METHOD_POC
-> EXPERIMENT -> FREEZE -> WRITE -> RENDER -> AUDIT -> READY
```

`stage` 记录当前正在推进的阶段名（即上面各阶段的名词形式，与 S0–S9
一一对应），而不是“已经完成的阶段”。阶段与门禁一一绑定：当前阶段的门禁
变为 `true` 时，才能推进到下一阶段。因此 `state.json` 中声明的阶段绝不允
许领先于第一个仍为 `false` 的门禁；审计会把它当作硬问题。

阶段 → 门禁映射：

| 阶段 | 完成门禁 |
|---|---|
| PREFLIGHT | `input_snapshot` |
| ANALYZE | `problem_decomposed` |
| ROUTE | `model_route_selected` |
| DATA_PLAN | `data_plan_ready` |
| METHOD_POC | `method_validated` |
| EXPERIMENT | `experiments_reproduced` |
| FREEZE | `results_frozen` |
| WRITE | `paper_written` |
| RENDER | `pdf_verified` |
| AUDIT | `audit_passed` |
| READY | 全部十个门禁 |

如果 `READY` 之前任何门禁为 `false`，当前状态就是未完成。`READY` 还要求：

- 所有十个门禁为 `true`；
- `audit/final_report.md` 的硬错误为 0；
- 论文中每个数字、表和结论都能在 `paper/evidence_map.json` 找到来源。

## 2. 一次推进的固定动作

每个阶段都按同一个循环执行：

1. **读取**：上一阶段产物、证据、未决风险和决策日志。
2. **声明**：本轮只处理哪个门禁、成功标准是什么、失败会转向哪里。
3. **执行**：生成最小可验证产物，不提前制作最终论文材料。
4. **自检**：运行命令、测试、数据检查或视觉检查。
5. **独立复核**：切换到 Reviewer 角色或新鲜上下文，从文件而不是对话复现。
6. **落盘**：更新阶段产物、`state.json`、`PROGRESS.md`、`audit/gate_evidence.json`。
7. **交接**：写出当前阶段、证据、风险和下一个精确入口。

## 3. 最少演示路径

最终交付前，必须能够按下面五步演示整条证据链：

1. 输入可读：题面和附件存在，哈希与清单一致。
2. 路线成立：每问的 baseline、primary、fallback 和验证方法齐全。
3. 最小 PoC 可运行：不依赖尚未冻结的最终结果，能复现关键计算。
4. 结果可冻结：正式运行的日志、参数、指标和来源齐全。
5. 论文可复现：用冻结数字重建图表和正文，PDF 逐页检查通过。

任一步失败就停止，不把后续步骤标成通过。

## 4. 阶段详情

### S0 PREFLIGHT

**目的**：固定输入事实和本地执行环境，避免后文在模糊题面或错误文件上返工。

**输入**

- 官方题面、附件、模板、数据字典；
- 比赛规则和交付格式；
- 当前目录和已有项目状态。

**必须做**

- 扫描题面文件、附件和模板，记录绝对路径、文件大小、SHA-256、访问日期；
- 检查 PDF、表格、文本编码是否可读；
- 运行 `doctor.py`，确认 Python、LaTeX/Typst、求解器和依赖；
- 明确这是新项目还是中断恢复项目；
- 区分官方文件、用户补充资料、网页数据、模型假设和旧结果。

**产物**

- `input_manifest.json`
- `state.json`
- `PROGRESS.md`
- `audit/gate_evidence.json` 中的 `input_snapshot` 证据

**通过标准**

- 每个输入都有路径、类型、哈希和状态；
- 无法读取的文件明确标记为阻塞，不用猜测替代；
- 环境缺失被记录为风险、替代方案或阻塞。

**失败模式**

- 文件只有模糊名称：先确认，不把未知附件当正文数据。
- 只能读取截图：记录 OCR 来源和误差风险。
- 题目规则与用户要求冲突：以比赛规则为硬约束，并记录冲突。

### S1 ANALYZE

**目的**：把题面拆成可独立验证的子问题卡，不在这里抢答模型。

**输入**

- `input_manifest.json`
- 官方题面和附件
- 比赛评分规则或往年评审偏好

**每个子问题卡必须包含**

- `id`、`question`、`deliverable`
- 研究对象、决策者、时间/空间范围
- 输入字段、单位、来源、附件依赖
- 输出形式：数值、区间、排序、策略、表格、图像、分类等
- 硬约束、软目标、评价指标
- 必须回答的正文问题
- 可验证的 `acceptance_criteria`
- `passes: false` 与空的 `evidence`

同时标记：

- `fact`：题面明确给出；
- `assumption`：为建模补充，必须说明理由和影响；
- `ambiguity`：需要用户、题目或数据裁决；
- `out_of_scope`：明确不做，防止范围失控。

**产物**

- `planning/problem_analysis.json`
- `planning/decision_log.jsonl` 中的分析决策
- `state.json` 的 `problem_decomposed`

**通过标准**

- 每一问都能映射到输入、输出、约束、指标和验收标准；
- 题面事实和模型假设没有混在一起；
- 每条验收标准都能被文件、命令、图表或人工检查证明；
- 所有子问题的总和没有偏离比赛题目。

**失败模式**

- 把“题目没给”直接写成自造数据：标成假设并说明边界。
- 多个子问题实际上是一问：合并并记录原因。
- 验收标准写成“效果好”：改写为可测指标或明确的人工判断规则。

### S2 ROUTE

**目的**：在写代码前，为每问选择能辩护的模型路线。

**输入**

- `planning/problem_analysis.json`
- 可用数据、计算预算、队伍能力和交付时间

**每条路线必须记录**

| 字段 | 含义 |
|---|---|
| `baseline` | 最简单、可解释、能作为对照的模型 |
| `primary_model` | 主模型及选择理由 |
| `fallback_model` | 主模型失败时可切换的退路 |
| `rejected` | 被考虑但拒绝的模型及具体原因 |
| `validation` | baseline -> primary、消融、敏感性和稳健性计划 |
| `required_figures` | 必须证明结论的图和表 |
| `paper_section` | 该模型进入论文的位置 |
| `acceptance_criteria` | 模型何时算“足够好” |
| `passes` | 初始为 `false` |

**评分维度**

使用 0-5 分比较候选路线：

- 题意契合度；
- 数据可得性；
- 模型可解释性；
- 验证可执行性；
- 计算成本；
- 论文叙事能力；
- 创新性；
- fallback 完整度；
- 团队实现能力。

复杂模型只有在相对 baseline 有可测量收益时才保留。不能仅凭“高级”作为选择理由。

**产物**

- `planning/topic_scores.json`
- `methods/model_route.json`
- `state.json` 的 `model_route_selected`

**通过标准**

- 每个子问题都有 baseline、primary、fallback；
- 被拒路线有具体原因，不写“太复杂”了事；
- 验证计划能直接转化为代码和表格；
- 主模型与数据、时间和交付格式相容。

**失败模式**

- 只有主模型：拒绝进入 S3，先补 baseline 和 fallback。
- fallback 只是“再试一次”：改成不同假设、不同复杂度或已验证的替代模型。
- 选用无法验证的生成式模型：必须定义可复现实验和失败边界。

### S3 DATA_PLAN

**目的**：在清洗和绘图前，先定义字段、单位、质量规则和泄漏风险。

**输入**

- S1 子问题卡；
- S2 模型路线；
- 原始数据、附件、外部数据来源。

**必须建立**

- 字段字典：名称、含义、类型、单位、范围、缺失编码、来源；
- 清洗规则：先去重、缺失、异常、时间对齐、空间匹配、单位统一；
- 样本关系：训练/验证/测试、时间顺序、跨题依赖；
- 泄漏检查：预测任务是否使用了未来信息、目标代理或赛后数据；
- 可视化计划：每张图的 purpose、source、script、output、paper_section；
- 外部数据来源的 URL、访问日期、许可或引用方式。

**产物**

- `data_cleaned/data_plan.json`
- `figures/visualization_plan.json`
- `data_cleaned/cleaning_log.jsonl`
- `state.json` 的 `data_plan_ready`

**通过标准**

- 每个字段都能追溯到来源；
- 单位、范围和缺失编码没有冲突；
- 预测任务有明确的防泄漏切分；
- 图表先说明用途，再先生成；
- 外部数据与估计值明显区分。

**失败模式**

- 缺失值被默认填成 0：要求先解释缺失机制。
- 同一指标来自多个口径：建立映射表或拆成不同字段。
- 图先做完再补意义：返回可视化计划，重新定义图能证明什么。

### S4 METHOD_POC

**目的**：用最小样例证明模型可计算、可验证、能和 baseline 比较。

**输入**

- `methods/model_route.json`
- `data_cleaned/data_plan.json`
- `figures/visualization_plan.json`

**必须做**

- 写符号表、假设、变量、参数、目标函数、约束和求解步骤；
- 解释每个假设的必要性、边界和失败后果；
- 实现最小 PoC，而不是直接跑完整实验；
- 用少量样本或缩小问题复现关键路径；
- 如果优化：检查求解状态、目标值、变量界、约束违反量和可行性；
- 如果预测：检查训练/验证切分、基线、误差指标和随机种子；
- 如果仿真：检查参数范围、终止条件和重复实验。

**产物**

- `methods/model_design.md`
- `methods/method_validation.json`
- `code/poc_*.py` 或 `.mod` / `.dat`
- `results/poc_manifest.json`
- `state.json` 的 `method_validated`

**通过标准**

- PoC 有明确运行命令和原始日志；
- 能在相同输入下复现；
- baseline 与 primary 的比较方式已固定；
- 数学写法和代码实现一致；
- 优化问题不存在隐藏的不可行或未检查状态。

**失败模式**

- 代码先于公式：补符号和约束映射。
- 只跑一次就认为稳定：记录随机性并设置重复次数。
- 优化求解器返回成功但没有检查约束：门禁保持 false。
- 数据规模太大：缩小 PoC，不跳过验证。

### S5 EXPERIMENT

**目的**：把验证计划转成完整、可重跑、可审计的实验。

**固定顺序**

```text
baseline -> primary -> ablation/control -> sensitivity -> robustness -> figures
```

**每次运行必须记录**

- `run_id`；
- 精确命令；
- 输入文件和哈希；
- 参数、初值、边界、随机种子；
- 环境与依赖版本；
- stdout/stderr、警告和耗时；
- 指标、表格和输出文件；
- 失败、回退或排除原因。

**产物**

- `results/run_manifest.json`
- `results/runs/<run_id>/...`
- `results/metrics.*`
- `figures/*` 和生成脚本
- `state.json` 的 `experiments_reproduced`

**通过标准**

- baseline、primary、对照、敏感性和稳健性都有记录；
- 指标可由保存的代码和日志重建；
- 图由脚本生成，不手工改数字；
- 优化问题报告可行性、约束余量和求解状态；
- 预测问题没有时间泄漏或测试集调参。

**失败模式**

- 只保留最好结果：保留所有正式运行和失败原因。
- 手工改图或表格：返回代码重生成。
- 结果只在聊天里：一律视为未完成。

### S6 FREEZE

**目的**：把最终会被论文引用的数字，变成带来源、可校验、不会再漂移的证据快照。

**输入**

- 已复核的正式实验；
- `results/run_manifest.json`；
- 论文所需数字、图表和结论清单。

**冻结规则**

每个值至少包含：

```json
{
  "name": "CO2_2021",
  "value": 414.2,
  "unit": "ppm",
  "source_file": "results/runs/run-003/metrics.json",
  "source_run": "run-003",
  "subproblem": "Q1",
  "notes": "annual global mean; verified against original data"
}
```

如果模型、数据、参数、种子或代码改变，旧冻结值立即失效，必须重新运行并重新冻结。

**产物**

- `frozen_numbers.json`
- `state.json` 的 `results_frozen`

**通过标准**

- 每个论文数字都能追溯到 `source_file` 和 `source_run`；
- 每个冻结值属于明确子问题；
- `frozen_at`、源文件哈希和 schema 版本存在；
- 估计值、模拟值、公开数据和手工设定值没有混写。

**失败模式**

- 数字来自聊天、截图或手工计算：拒绝冻结。
- 多个运行产生不同值：选择规则必须先写清楚。
- 只冻结摘要数字，正文还需临时计算：把派生数字也纳入冻结或生成可重现的派生表。

### S7 WRITE

**目的**：按证据组织论文，而不是先写漂亮叙事再找数字。

**输入**

- `frozen_numbers.json`
- `methods/model_design.md`
- `results/run_manifest.json`
- 图表和图表计划

**论文顺序**

1. 摘要
2. 问题重述与分析
3. 模型假设与符号
4. 模型建立
5. 求解算法
6. 实验结果
7. 敏感性、稳健性和模型比较
8. 结论、限制和推广

**写作文本规则**

- LaTeX 与 Typst 二选一，禁止混写；
- 正文每个结论必须绑定冻结数字、图表或运行记录；
- 图表先引用后出现；
- 公式中的符号必须在符号表出现；
- 单位统一，范围与数据口径一致；
- 不虚构文献、不伪造专家意见、不把假设写成事实；
- 摘要中的每个数字也必须来自冻结文件。

**产物**

- `paper/main.tex` 或 `paper/main.typ`
- `paper/evidence_map.json`
- `paper/claim_index.json`
- `state.json` 的 `paper_written`

**通过标准**

- 论文的每个数字、结论、图表都能映射到证据；
- 题目每一问都有清楚回答；
- 没有未冻结的最终数字；
- 模型创新与 baseline 的差异可量化解释。

**失败模式**

- 正文比证据更早完成：返回 S6 补冻结，或先写证据映射骨架。
- 只展示 primary 结果：加入 baseline、消融和失败边界。
- 用“显著提升”但不给数值：改成具体指标和区间。

### S8 RENDER

**目的**：把论文变成可逐页交付的 PDF，并检查排版与结构。

**必须做**

- 选择并锁定一个编译链；
- 编译到成功，且检查日志中的错误和关键警告；
- 渲染每页图片，逐页检查；
- 检查溢出、空白页、断图、缺图、乱码、公式断行和交叉引用；
- 检查图表编号、目录、页码、参考文献和附录；
- 检查文件名、字体和模板是否符合比赛规则；
- 如比赛要求匿名，检查作者、路径、元数据是否泄漏。

**产物**

- `paper/main.pdf`
- `paper/render_log.json`
- 页面截图或渲染图目录
- `state.json` 的 `pdf_verified`

**通过标准**

- PDF 可打开且页数与预期一致；
- 没有硬编译错误、缺图、裁切、乱码或无法阅读的表格；
- 图表编号、正文引用、单位和结论一致；
- 官方模板和提交格式合规。

**失败模式**

- 只看编译成功：仍需逐页视觉检查。
- 局部表格溢出：优先修排版，不删证据。
- 字体或编码异常：返回 S7 修源文件，不直接编辑 PDF。

### S9 AUDIT

**目的**：把前三层证据作为审查对象，而不是重新相信生成者摘要。

**输入**

- 全部状态、产物、日志、图表和论文；
- `audit/gate_evidence.json`；
- `planning/decision_log.jsonl`；
- `paper/evidence_map.json`。

**独立审查动作**

- 复现关键命令，不只看结果截图；
- 从论文抽取数字，反查 `frozen_numbers.json` 和运行记录；
- 从每条核心结论反查证据和假设；
- 检查 baseline、消融、敏感性、稳健性是否真的支持结论；
- 检查数据泄漏、过拟合、不合理单位、不可行解和边界情况；
- 检查图表视觉结果与正文数字一致；
- 检查 PDF 逐页表现；
- 输出硬错误与软风险，并给出回退阶段。

**产物**

- `audit/final_report.md`
- `audit/acceptance.json`
- `state.json` 的 `audit_passed`

**通过标准**

- 硬错误为 0；
- 所有门禁有可复现证据；
- 每个关键结论有来源；
- 软风险被明确记录，不假装不存在；
- 审查者没有修改被审查的代码或论文来让结果通过。

**失败模式**

- 审查者就是生成者且无法独立复现：至少换一次上下文或执行真实命令。
- 把格式错误当轻微问题忽略：凡影响阅读或提交合规的都算硬错误。
- 数字对不上：返回 S6，不从 PDF 里手改。

## 5. 决策日志

每次范围、模型、数据或路线变化，追加一行 JSON：

```json
{
  "at": "2026-09-10T12:00:00Z",
  "subject": "Q2-primary-model",
  "classification": "PIVOT",
  "rationale": "The primary route cannot satisfy the hard time constraint.",
  "author": "analyst",
  "relates_to": "methods/model_route.json"
}
```

允许的分类：

- `KEEP`：保留；
- `CUT`：删除；
- `DEFER`：推迟；
- `PIVOT`：换路线；
- `ACCEPT_RISK`：明确接受已知风险，并写明影响和补救。

日志只追加，不覆盖。若结论改变，写新一条，不修改旧理由。

## 6. 交接格式

每轮结束时用短而具体的交接：

```text
Stage:
Gate opened:
Artifacts:
Evidence reproduced:
Open risks:
Next exact action:
```

示例：

```text
Stage: S4 METHOD_POC
Gate opened: method_validated
Artifacts: methods/model_design.md, methods/method_validation.json, code/poc_q1.py
Evidence reproduced: python3 code/poc_q1.py -> exit 0; baseline MAE=..., primary MAE=...
Open risks: February anomaly not yet explained; sensitivity begins in S5.
Next exact action: run S5 baseline -> primary -> ablation for Q1.
```

## 7. 禁止事项

- 禁止跳过 S4、S6、S9；
- 禁止把“模型很合理”当验证；
- 禁止在论文中使用未冻结数字；
- 禁止删除或修改验收标准来让门禁通过；
- 禁止让生成者单独批准自己的工作；
- 禁止用旧结果覆盖新结果而不更新冻结和证据映射；
- 禁止保留同名旧稿或 `backup` 文件作为隐藏的第二答案。
