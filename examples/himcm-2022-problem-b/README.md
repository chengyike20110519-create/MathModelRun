# HiMCM 2022 Problem B 示例：CO₂ 与全球变暖

本目录保存已有建模实验、结构化结果、图表和可编辑论文，展示 MathModel Run 的证据链。合并时保留本地实验记录，而非重置为启动模板。

- `problem_files/himcm_data.csv`：本地数据表，官方题面需自行取得。
- `code/`：复现实验、绘图与论文构建代码。
- `results/` 与 `frozen_numbers.json`：历史运行结果与来源记录。
- `paper/` 与 `audit/`：论文源稿、证据映射和已有审查记录。

`state.json` 的完成状态是历史记录，不代表本次发布重新验证了示例论文。PDF 与日志按仓库忽略规则未分发；使用者须核实路径、依赖和输入，重跑实验、构建论文并审查实际页面后，才能认可当前完成状态。

可先检查状态与机械契约：

```bash
python3 my-mathmodel-agent/scripts/status.py examples/himcm-2022-problem-b
python3 my-mathmodel-agent/scripts/audit_workspace.py examples/himcm-2022-problem-b
```

机械检查不能替代模型验证和 PDF 视觉检查。
