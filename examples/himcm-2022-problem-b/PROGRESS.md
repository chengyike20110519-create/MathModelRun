# Project Progress

This file is the durable handoff log for fresh agent contexts. Append one
compact entry whenever a gate changes or a blocker is discovered.

## Template

```text
At:
Stage:
Gate:
Artifacts:
Evidence:
Risks:
Next:
```

## Entries

At: 2026-09-12T13:00:00+08:00
Stage: METHOD_POC
Gate: input_snapshot, problem_decomposed, model_route_selected, data_plan_ready
Artifacts: input_manifest.json; planning/problem_analysis.json; methods/model_route.json; data_cleaned/data_plan.json; figures/visualization_plan.json; audit/gate_evidence.json
Evidence: 本地 CSV 快照、历史 working draft、五张既有图表已接入并记录来源；四个前置门禁有可定位证据。
Risks: 历史数字未由当前可运行脚本独立重算；Python 3.13.5 环境缺少 sklearn；官方题面文件尚未纳入案例。
Next: 实现 code/reproduce_himcm.py，完成最小 PoC 后再推进 method_validated。

At: 2026-09-12T13:30:00+08:00
Stage: EXPERIMENT
Gate: method_validated
Artifacts: code/reproduce_himcm.py; results/runs/run-002/metrics.json; results/run_manifest.json
Evidence: Q1 使用时间顺序末端十年回测成功；线性 RMSE=10.8935 ppm，指数 RMSE=8.5843 ppm；最大十年增量为 2011-2021 的 24.60 ppm。
Risks: 当前只验证线性和指数模型；Logistic、ARIMA、Q2 统计检验、图形重生成和正式冻结仍未完成。
Next: 扩展 Q1 正式实验，加入 Logistic/ARIMA 或可解释 fallback，并独立复现 Q2 温度分析。

At: 2026-09-12T13:45:00+08:00
Stage: EXPERIMENT
Gate: method_validated remains passed; experiments_reproduced remains open
Artifacts: code/reproduce_himcm.py; results/runs/run-002/metrics.json; results/run_manifest.json
Evidence: 同一可运行脚本已补充 Q2：温度线性趋势阈值年份为 2044.24、2059.39、2089.71；共享年份 Pearson r=0.96117；Granger 因果检验因缺少 statsmodels 明确未运行。
Risks: run-002 仍是 PoC，不是覆盖全部选定路线的正式实验；尚未重生成全部图表、冻结结果或写最终论文。
Next: 补齐 Q1 的 Logistic 与可解释 ARIMA fallback，随后做统一模型比较和敏感性实验。

At: 2026-09-12T14:00:00+08:00
Stage: EXPERIMENT
Gate: method_validated passed; experiments_reproduced remains open
Artifacts: code/reproduce_himcm.py; results/runs/run-002/metrics.json; results/run_manifest.json; methods/method_validation.json
Evidence: Q1 Logistic 网格拟合已加入并运行；末端十年 RMSE=8.9124 ppm，2100 预测=555.7445 ppm，未优于指数模型 RMSE=8.5843 ppm。复杂模型没有被自动视为更好。
Risks: ARIMA 与 Granger 仍未独立实现；当前 run-002 是覆盖主要透明路径的实验候选，不足以通过 experiments_reproduced。
Next: 实现不依赖 statsmodels 的 ARIMA(1,1,0) 差分回归和 Granger F 统计量，或明确降级为可解释 fallback 并更新路线。

At: 2026-09-12T21:23:49+08:00
Stage: EXPERIMENT
Gate: method_validated, experiments_reproduced passed; results_frozen, paper_written, pdf_verified, audit_passed remain open
Artifacts: code/reproduce_himcm.py; results/runs/run-002/metrics.json; results/run_manifest.json; methods/method_validation.json; audit/gate_evidence.json
Evidence: 同一 run-002 已用最新脚本真实重跑并通过编译；ARIMA(1,1,0) 末端十年 RMSE=5.8837 ppm；Granger p 值为 CO2→温度 4.31e-8、温度→CO2 0.7886；阈值年份及标准误/95%区间已写入 metrics；五张必需 PNG 均已重生成并视觉检查。
Risks: Granger p 值来自本地不完全 Beta 实现，仍只作探索性统计；趋势外推不是物理气候模型。最终结果尚未冻结，论文/PDF/总审计尚未开始。
Next: 进入结果冻结前的审计检查，确认指标、图表、模型路线和验收标准完全一致；通过后再原位更新 frozen_numbers.json 并开始正式论文。

At: 2026-09-12T22:10:00+08:00
Stage: WRITE
Gate: input_snapshot, problem_decomposed, model_route_selected, data_plan_ready, method_validated, experiments_reproduced, results_frozen, paper_written passed; pdf_verified remains open
Artifacts: paper/working-draft.md; paper/evidence_map.json; paper/main.tex; paper/render_log.json
Evidence: working-draft.md 已原位替换旧数字和过时的双向反馈表述；main.tex 已由 pandoc 生成。标准 LaTeX 编译入口调用 MiKTeX 时连续无输出阻塞，未生成 PDF，故没有虚报 pdf_verified。
Risks: 当前阻塞属于本机 MiKTeX 初始化/字体运行时问题；最终 PDF、逐页视觉检查和 audit_passed 仍未完成。
Next: 先修复或切换可用 LaTeX 运行时，再编译 paper/main.tex、逐页渲染检查并更新 render_log.json。

At: 2026-09-13T08:00:00+08:00
Stage: READY
Gate: all ten gates passed
Artifacts: paper/main.pdf; paper/render_log.json; audit/final_report.md; audit/gate_evidence.json; audit/acceptance.json; project_manifest.json; state.json
Evidence: 原路径 paper/main.pdf 已直接替换为 24 页 Letter 版本，SHA-256 为 91c18e225b5d0dd9d0fce577847316409d9345d9492a12f2b0d8280d265b38f7。首页与目录为单栏，目录后的正文切换为双栏；Summary Sheet、五张图、References、Appendix A-D、页眉和 Page 24 of 24 均通过文字层与结构核验。
Risks: 当前环境的 fontconfig 缓存目录不可写，Poppler 像素级逐页渲染未完成；MiKTeX 编译入口仍受初始化阻塞。论文结果、实验和 PDF 结构不受该限制影响。
Next: package_and_submit；如需进一步提升，只应替换为可用 TeX/字体环境后做像素级视觉复核，不重跑 run-002。
