# xiaohongshu-skills

小红书自动化 Claude Code Skills，使用用户的真实浏览器和账号信息，通过 Extension Bridge 模式操作小红书。

## 维护规则

- 源仓库是唯一真源，安装到 `~/.claude/skills/xiaohongshu-skills` 的副本只用于本地运行与验证。
- 如果必须直接在已安装 skill 上做 hotfix，必须立刻同步回源仓库，避免再次漂移。
- `xhs-content-ops` 负责写作策略、选题策划、系列编排、草稿整理、运营编排与多步骤 orchestration 指导。
- `xhs-publish` 负责发布执行、发布前校验，以及图文 / 视频 / 长文 / 定时发布流程；只有内容已经收口为可直接发布的终稿时才进入这个边界。
- 对于已整理好的系列资产，`copy-ready` Markdown 是发布阶段认可的最终真源；这是工作流约束，不代表仓库里已经存在专门的 `copy-ready` CLI 子命令或独立命令面。
- 更新 README、`SKILL.md`、`ARCHITECTURE.md` 时，必须一起检查命令面、Bridge 描述与发布约束，避免文档漂移；如果子技能文档涉及这些边界，也必须同步保持一致。

## Git 工作流

- 所有代码修改必须在分支上进行，禁止直接推送 `main`/`master`
- 分支开发完成后通过 PR 合入主分支
- 未经明确要求，不要只改已安装副本而不改源仓库

## 开发命令

```bash
uv sync                    # 安装依赖
uv run ruff check .        # Lint 检查
uv run ruff format .       # 代码格式化
uv run pytest              # 运行测试
```

## 架构

双层结构：`scripts/` 是 Python Bridge 自动化引擎，`skills/` 是 Claude Code Skills 定义（`SKILL.md` 格式）。

- `scripts/xhs/` — 核心自动化库（模块化，每个功能一个文件）
- `scripts/cli.py` — 统一 CLI 入口，JSON 结构化输出，负责连接本地 Bridge
- `scripts/bridge_server.py` — 本地通信服务（连接 CLI 与浏览器扩展）
- `extension/` — Chrome 扩展，在用户的真实浏览器中执行操作
- `skills/*/SKILL.md` — 指导 Claude 如何调用 `scripts/`

### 调用方式

```bash
python scripts/cli.py check-login
python scripts/cli.py search-feeds --keyword "关键词"
python scripts/cli.py publish --title-file t.txt --content-file c.txt --images /abs/path/pic.jpg
```

> CLI 会自动检测 Bridge 与浏览器状态，必要时会启动本地依赖并等待扩展连接。

## 代码规范

- 行长度上限 100 字符
- 完整 type hints，使用 `from __future__ import annotations`
- 异常继承 `XHSError`（`xhs/errors.py`）
- CLI exit code：0=成功，1=未登录，2=错误
- 用户可见错误信息使用中文
- JSON 输出 `ensure_ascii=False`

### 安全约束

- 发布类操作必须有用户确认机制
- 文件路径必须使用绝对路径
- 图文发布只接受用户已准备好的本地图片绝对路径
- 敏感内容通过文件传递，不内联到命令行参数
- 多账号切换应通过登录态 / cookies 隔离来完成，不要混用同一会话

## CLI 子命令对照表

| CLI 子命令 | 当前状态 | 分类 |
|--|--|--|
| `check-login` | 已支持 | 认证 |
| `login` | 已支持 | 认证 |
| `get-qrcode` | 已支持 | 认证 |
| `wait-login` | 已支持 | 认证 |
| `phone-login` | 已支持 | 认证 |
| `send-code` | 已支持 | 认证 |
| `verify-code` | 已支持 | 认证 |
| `delete-cookies` | 已支持 | 认证 |
| `list-feeds` | 已支持 | 浏览 |
| `search-feeds` | 已支持 | 浏览 |
| `get-feed-detail` | 已支持 | 浏览 |
| `user-profile` | 已支持 | 浏览 |
| `post-comment` | 已支持 | 互动 |
| `reply-comment` | 已支持 | 互动 |
| `like-feed` | 已支持 | 互动 |
| `favorite-feed` | 已支持 | 互动 |
| `publish` | 已支持 | 发布 |
| `publish-video` | 已支持 | 发布 |
| `fill-publish` | 已支持 | 分步发布（图文填写） |
| `fill-publish-video` | 已支持 | 分步发布（视频填写） |
| `click-publish` | 已支持 | 分步发布（点击发布） |
| `save-draft` | 已支持 | 分步发布（保存草稿） |
| `long-article` | 已支持 | 长文发布（填写 + 排版） |
| `select-template` | 已支持 | 长文发布（选择模板） |
| `next-step` | 已支持 | 长文发布（下一步 + 描述） |
