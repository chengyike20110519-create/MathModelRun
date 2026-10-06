# HiMCM 2022 Problem B 示例：CO₂ 与全球变暖

这是一个**启动模板**，演示 MathModel Run 工作流在 HiMCM 2022 Problem B（CO₂ 与全球变暖）上的脚手架。
本仓库保留了：

- 本地数据草表（`data_cleaned/` 中以脚手架占位）；
- 历史 working draft 与既有图表模板；
- 当前完成到第四门禁 `data_plan_ready`，下一门禁 `method_validated` 仍是 `false`。

按照 [README](../../README.md) 与 [my-mathmodel-agent/SKILL.md](../../my-mathmodel-agent/SKILL.md) 的十阶段契约，
下一步是为 Q1（CO₂ 浓度趋势）、Q2（温度响应）、Q3（情景预测）补充可独立复现的最小 PoC 与基线对照。

## 阶段快照

```text
Stage:           METHOD_POC（指向 S0-S4 已通过）
gates passed:    input_snapshot / problem_decomposed / model_route_selected / data_plan_ready
first false:     method_validated
next action:     run_a_minimal_proof_of_concept
```

## 仓库期望

- `problem_files/`：放官方题面与附件（未在本仓库内分发，按需要手动放置）。
- `planning/decision_log.jsonl`：追加式记录每一项 KEEP / CUT / DEFER / PIVOT / ACCEPT_RISK 决策。
- `methods/method_validation.json`：记录 PoC 的最小输入、运行命令、指标与图。
- `audit/mechanical_report.md`：由 `python3 my-mathmodel-agent/scripts/audit_workspace.py .` 重新生成。

## 本地使用

```bash
# 重新生成机械审计报告
python3 my-mathmodel-agent/scripts/audit_workspace.py examples/himcm-2022-problem-b

# 查看阶段与下一步
python3 my-mathmodel-agent/scripts/status.py examples/himcm-2022-problem-b
```

本目录的状态字段与模板保持一致；任何人都可以在此基础上另存副本开始独立复现，
而不是直接修改这份参考脚手架。
