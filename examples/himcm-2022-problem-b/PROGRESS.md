# Project Progress

HiMCM 2022 Problem B：CO2 与全球变暖。

## 模板

```
At:
Stage:
Gate:
Artifacts:
Evidence:
Risks:
Next:
```

## Entries

### At: 2024-02-01T00:00:00Z
Stage: METHOD_POC
Gate: data_plan_ready
Artifacts:
- input_manifest.json
- planning/problem_analysis.json
- methods/model_route.json
- data_cleaned/data_plan.json
- audit/gate_evidence.json
Evidence:
- S0: NOAA / NASA / IPCC 资源已登记，附件路径已留位。
- S1: Q1/Q2/Q3 拆解与 acceptance_criteria 在 team meeting 上一致通过。
- S2: 每 Q  给出 baseline / primary / fallback 与拒绝理由。
- S3: 字段、单位、清洗、split、leakage 已冻结。
Risks:
- IPCC 情景依赖人工表格, 需要在 Q3 PoC 中明确中心值与区间。
- 历史 working draft 与图表未迁入本目录, 仅作参考。
Next:
- 为 Q1 跑 STL 分解的最小 PoC, 报告 R^2 与残差白噪声。
