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

1. 在 `skills/<skill-name>/SKILL.md` 创建通用 Skill，并只保留实际需要的
   `references/`、`scripts/` 或 `assets/`。
2. 运行 skill creator 的 `quick_validate.py`，确认 frontmatter、命名和
   TODO 检查通过。
3. 如果该 Skill 需要独立的 Claude Code 入口，再添加
   `.claude/skills/<skill-name>/`，不要复制旧版本或保留废弃入口。
4. 用 skills CLI 的 `add . --list --full-depth` 验证仓库可以发现新 Skill。
5. 更新 `README.md`、`docs/INSTALL.md` 和 `AGENTS.md` 中的入口说明。

## 测试

```bash
python3 -m pytest tests/ -v
```

## 许可

贡献即表示你同意在 MIT 许可证下发布代码。
