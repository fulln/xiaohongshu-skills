# xiaohongshu-skills

小红书自动化 Skills，直接使用你已登录的本地浏览器和真实账号，通过 Extension Bridge 的方式操作小红书。

支持 [OpenClaw](https://github.com/anthropics/openclaw) 及所有兼容 `SKILL.md` 格式的 AI Agent 平台（如 Claude Code）。

## 项目说明

当前仓库是从更早的小红书 skills 项目延续整理并持续改进的版本。
当前安装与克隆请使用本仓库地址 `fulln/xiaohongshu-skills`。

> **⚠️ 使用建议**：虽然本项目使用真实的用户浏览器和账号环境，但仍建议控制使用频率，避免短时间内大量操作。频繁的自动化行为可能触发小红书的风控机制，导致账号受限。

## 功能概览

| 技能 | 说明 | 核心能力 |
|------|------|----------|
| **xhs-auth** | 认证管理 | 登录检查、扫码登录、多账号切换 |
| **xhs-publish** | 内容发布 | 图文 / 视频 / 长文发布、定时发布、基于现成终稿的发布执行 |
| **xhs-explore** | 内容发现 | 关键词搜索、笔记详情、用户主页、首页推荐 |
| **xhs-interact** | 社交互动 | 评论、回复、点赞、收藏 |
| **xhs-content-ops** | 复合运营 | 竞品分析、热点追踪、选题策划、系列编排、草稿整理 |

支持连贯操作，你可以用自然语言下达复合指令，Agent 会自动串联多个技能完成任务。例如：

> "搜索刺客信条最火的图文帖子，收藏它，然后告诉我讲了什么"

Agent 会自动执行：搜索 → 筛选图文 → 按点赞排序 → 收藏 → 获取详情 → 总结内容。

## 安装

### 前置条件

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) 包管理器
- Google Chrome 浏览器
- 可加载本地扩展的桌面环境

### 本地安装模型

本项目的真实使用方式是：把整个仓库安装到本机 Agent 的 skills 目录中，本地执行 `scripts/cli.py`，再通过浏览器扩展接管你当前机器上的 Chrome。

常见安装位置：

```text
# Claude Code
~/.claude/skills/xiaohongshu-skills/

# OpenClaw
<openclaw-project>/skills/xiaohongshu-skills/
```

你可以用 ZIP 或 git clone 两种方式完成安装。

### 方式一：下载 ZIP

1. 在 GitHub 仓库页面点击 **Code -> Download ZIP**。
2. 解压到你的 Agent skills 目录，目录名保持为 `xiaohongshu-skills`。
3. 在该目录执行：

```bash
uv sync
```

### 方式二：git clone

```bash
git clone https://github.com/fulln/xiaohongshu-skills.git ~/.claude/skills/xiaohongshu-skills
cd ~/.claude/skills/xiaohongshu-skills
uv sync
```

### 安装浏览器扩展

扩展让 Agent 能在你的本地浏览器里，以你的真实登录态执行操作。

1. 打开 Chrome，访问 `chrome://extensions/`
2. 开启开发者模式
3. 点击"加载已解压的扩展程序"
4. 选择本项目的 `extension/` 目录
5. 确认 **XHS Bridge** 已启用

安装完成后，CLI 会通过本地 `bridge_server.py` 与扩展通信，实际操作发生在你当前机器的 Chrome 标签页中。

## 使用方式

### 作为 AI Agent 技能使用

安装到 skills 目录后，直接用自然语言与 Agent 对话即可。Agent 会根据你的意图自动路由到对应技能。

**认证登录：**
> "登录小红书" / "检查登录状态" / "切换到另一个账号"

**搜索浏览：**
> "搜索关于露营的笔记" / "查看这条笔记的详情"

**发布内容：**
> "帮我发一条图文笔记，标题是...，配图是本地绝对路径..."

**社交互动：**
> "给这条笔记点赞" / "收藏这条帖子" / "评论：写得太好了"

**复合操作：**
> "搜索竞品账号最近的爆款笔记，分析他们的选题方向"

### 作为 CLI 工具使用

所有功能都可以通过命令行直接调用，输出 JSON 格式，便于脚本集成。

```bash
# 检查登录状态
python scripts/cli.py check-login

# 扫码登录
python scripts/cli.py login

# 搜索笔记
python scripts/cli.py search-feeds --keyword "关键词"

# 带筛选条件
python scripts/cli.py search-feeds \
  --keyword "关键词" \
  --sort-by "最多点赞" \
  --note-type "图文"

# 查看笔记详情
python scripts/cli.py get-feed-detail \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN

# 图文分步发布：填写 -> 预览 -> 确认发布
python scripts/cli.py fill-publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/abs/path/pic1.jpg" "/abs/path/pic2.jpg"
python scripts/cli.py click-publish

# 图文分步发布：填写 -> 预览 -> 保存草稿
python scripts/cli.py fill-publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/abs/path/pic1.jpg"
python scripts/cli.py save-draft

# 一步发布图文
python scripts/cli.py publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/abs/path/pic1.jpg" \
  --tags "标签1" "标签2"

# 视频发布
python scripts/cli.py publish-video \
  --title-file title.txt \
  --content-file content.txt \
  --video "/abs/path/video.mp4"

# 长文发布
python scripts/cli.py long-article \
  --title-file title.txt \
  --content-file content.txt

# 长文排版辅助
python scripts/cli.py select-template --name "模板名"
python scripts/cli.py next-step --title-file title.txt --content-file content.txt

# 点赞 / 收藏 / 评论
python scripts/cli.py like-feed --feed-id FEED_ID --xsec-token XSEC_TOKEN
python scripts/cli.py favorite-feed --feed-id FEED_ID --xsec-token XSEC_TOKEN
python scripts/cli.py post-comment --feed-id FEED_ID --xsec-token XSEC_TOKEN --content "评论内容"
```

> 图文发布只接受用户已准备好的本地图片绝对路径，不负责生成、提取或下载图片。
>
> 系列内容的选题策划、系列编排、草稿整理归 `xhs-content-ops`；只有当你已经有可直接发布的终稿时，才交给 `xhs-publish` 进入发布执行。
>
> 对于已经整理完成的系列发帖资产，建议在发布阶段只保留单一 `copy-ready` Markdown 作为最终真源，再由 `xhs-publish` 执行填充和发布。
>
> 当前仓库尚未提供名为 `publish-copy-ready` 或 `fill-publish-copy-ready` 的独立 CLI 子命令；`copy-ready` 是系列发布流程约束，而不是现成命令名或专门命令面。
>
> 维护说明：如果后续子技能文档调整了这些边界，README、`SKILL.md`、`CLAUDE.md`、`ARCHITECTURE.md` 也需要同步更新；子技能文档本身也必须在对应任务里单独同步，避免顶层说明与子技能定义不一致。

## CLI 命令参考

| 子命令 | 说明 |
|--------|------|
| `check-login` | 检查当前是否已登录；未登录时会给出二维码登录信息或提示后续等待登录结果 |
| `login` | 发起二维码登录并阻塞等待结果；返回登录成功或等待超时等状态 |
| `get-qrcode` | 获取登录二维码截图（非阻塞） |
| `wait-login` | 等待扫码登录完成 |
| `phone-login` | 手机号 + 验证码登录（交互式） |
| `send-code` | 分步登录第一步：发送手机验证码 |
| `verify-code` | 分步登录第二步：填写验证码 |
| `delete-cookies` | 清除 cookies（退出登录 / 切换账号） |
| `list-feeds` | 获取首页推荐 Feed |
| `search-feeds` | 关键词搜索笔记（支持排序 / 类型 / 时间 / 范围 / 位置筛选） |
| `get-feed-detail` | 获取笔记完整内容和评论 |
| `user-profile` | 获取用户主页信息和帖子列表 |
| `post-comment` | 对笔记发表评论 |
| `reply-comment` | 回复指定评论 |
| `like-feed` | 点赞 / 取消点赞 |
| `favorite-feed` | 收藏 / 取消收藏 |
| `publish` | 一步发布图文 |
| `publish-video` | 一步发布视频 |
| `fill-publish` | 填写图文表单（不发布，供预览） |
| `fill-publish-video` | 填写视频表单（不发布，供预览） |
| `click-publish` | 确认发布（点击发布按钮） |
| `save-draft` | 保存为草稿 |
| `long-article` | 长文模式：填写 + 一键排版 |
| `select-template` | 选择长文排版模板 |
| `next-step` | 长文下一步 + 填写描述 |

退出码：`0` 成功，`1` 未登录，`2` 错误。

## 项目结构

```text
xiaohongshu-skills/
├── extension/                      # Chrome 扩展
│   ├── manifest.json
│   ├── background.js
│   └── content.js
├── scripts/                        # Python 自动化引擎
│   ├── xhs/                        # 核心自动化包
│   │   ├── bridge.py               # 扩展通信客户端
│   │   ├── selectors.py            # CSS 选择器（集中管理）
│   │   ├── login.py                # 登录 + 用户信息获取
│   │   ├── feeds.py                # 首页 Feed
│   │   ├── search.py               # 搜索 + 筛选
│   │   ├── feed_detail.py          # 笔记详情 + 评论加载
│   │   ├── user_profile.py         # 用户主页
│   │   ├── comment.py              # 评论、回复
│   │   ├── like_favorite.py        # 点赞、收藏
│   │   ├── publish.py              # 图文发布
│   │   ├── publish_video.py        # 视频发布
│   │   ├── publish_long_article.py # 长文发布
│   │   ├── types.py                # 数据类型
│   │   ├── errors.py               # 异常体系
│   │   ├── urls.py                 # URL 常量
│   │   ├── cookies.py              # Cookie 持久化
│   │   └── human.py                # 行为模拟
│   ├── cli.py                      # 统一 CLI 入口
│   ├── bridge_server.py            # 本地通信服务
│   ├── title_utils.py              # UTF-16 标题长度计算
│   └── run_lock.py                 # 单实例锁
├── skills/                         # Claude Code Skills 定义
│   ├── xhs-auth/SKILL.md
│   ├── xhs-publish/SKILL.md
│   ├── xhs-explore/SKILL.md
│   ├── xhs-interact/SKILL.md
│   └── xhs-content-ops/SKILL.md
├── SKILL.md                        # 技能统一入口（路由到子技能）
├── CLAUDE.md                       # 项目开发指南
├── ARCHITECTURE.md                 # Bridge 架构说明
├── pyproject.toml
└── README.md
```

## 开发

```bash
uv sync
uv run ruff check .
uv run ruff format .
uv run pytest
```

## License

MIT

## Star History

[![Star History Chart](https://api.star-history.com/image?repos=fulln/xiaohongshu-skills&type=date&legend=top-left)](https://www.star-history.com/?repos=fulln%2Fxiaohongshu-skills&type=date&legend=top-left)
