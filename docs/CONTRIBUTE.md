# 贡献指南

感谢你的贡献！

## 报告问题

请使用 GitHub Issues，并尽量包含：

- 你的操作系统和 Python 版本
- 复现步骤
- 期望行为与实际行为
- 相关日志或截图

## 提交代码

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature/<描述>`
3. 提交变更：`git commit -m "feat: ..."`
4. 推送到分支：`git push origin feature/<描述>`
5. 提交 Pull Request

## 代码规范

- Python 代码使用 4 空格缩进
- 脚本需带 `--help` 帮助信息
- 新增脚本应包含 smoke test
- 文档更新随代码一起提交

## 扩展 Skill

新增子技能时：

1. 在 `.claude/skills/` 创建新的 SKILL.md
2. 在 `my-mathmodel-agent/` 创建对应的 Codex 入口（如适用）
3. 更新 `README.md` 中的 Skill 索引
4. 更新 `AGENTS.md` 入口说明

## 测试

```bash
python3 -m pytest tests/ -v
```

## 许可

贡献即表示你同意在 MIT 许可证下发布代码。
