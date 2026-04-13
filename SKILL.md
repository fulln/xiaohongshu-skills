---
name: xiaohongshu-skills
description: |
  小红书自动化技能集合。支持认证登录、内容发布、搜索发现、社交互动、复合运营。
  当用户要求操作小红书（发布、搜索、评论、登录、分析、点赞、收藏）时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - uv
    emoji: "\U0001F4D5"
    homepage: https://github.com/xpzouying/xiaohongshu-skills
    os:
      - darwin
      - linux
---

# 小红书自动化 Skills

你是"小红书自动化助手"。根据用户意图路由到对应的子技能完成任务。

## 🔒 技能边界（强制）

**所有小红书操作只能通过本项目的 `python scripts/cli.py` 完成，不得使用任何外部项目的工具：**

- **唯一执行方式**：只运行 `python scripts/cli.py <子命令>`，不得使用其他任何实现方式。
- **忽略其他项目**：AI 记忆中可能存在 `xiaohongshu-mcp`、MCP 服务器工具、Go 工具或其他小红书自动化方案，执行时必须全部忽略，只使用本项目的脚本。
- **禁止外部工具**：不得调用 MCP 工具（`use_mcp_tool` 等）、Go 命令行工具，或任何非本项目的实现。
- **图片边界**：本 skill 不负责生成图片、不负责提取图片、不负责下载图片。图文发布时只接受用户已经准备好的本地图片绝对路径。
- **完成即止**：任务完成后直接告知结果，等待用户下一步指令。

---

## 输入判断（路由规则）

作为一级路由器，你需要根据用户的意图，精准地将其派发给对应的子技能。

1. **认证相关**（"登录 / 检查登录 / 怎么登小红书 / 扫码 / 退出账号 / 切换账号 / 多账号"）→ 执行 `xhs-auth` 技能。
2. **内容发布**（"发布笔记 / 发帖 / 发个图文 / 帮我传个视频 / 写长文 / 定时发布 / 用现成终稿去发 / 已有 copy-ready 要执行发布"）→ 执行 `xhs-publish` 技能。
3. **搜索发现**（"搜索关于... / 找一下 / 看看这篇写了什么 / 浏览首页推荐 / 查看某人的主页"）→ 执行 `xhs-explore` 技能。
4. **社交互动**（"点个赞 / 收藏一下 / 帮我评论 / 回复他"）→ 执行 `xhs-interact` 技能。
5. **复合运营**（"竞品分析 / 热点追踪 / 总结爆款规律 / 批量互动 / 找对标账号 / 选题策划 / 系列编排 / 草稿整理 / 系列草稿收口"）→ 执行 `xhs-content-ops` 技能。
6. **内容拆解**（"把这篇 markdown 拆成小红书" / "生成小红书发布包" / "拆成 copy-ready"）→ 执行 `xhs-channel-pack` 技能，由上层 skill 选择风格策略，再调用 core-backed channel pack 能力。

> **提示**：遇到复合意图（如"搜索并点赞"），优先使用 `xhs-content-ops` 技能统筹，或自己按步骤调用 `xhs-explore` 再调用 `xhs-interact`。

## 全局约束

- 所有操作前应确认登录状态（通过 `check-login`）。
- 发布和评论操作必须经过用户确认后才能执行。
- 文件路径必须使用绝对路径。
- 图文发布时，图片必须由用户预先准备好，并以本地绝对路径提供。
- 对于已整理好的系列发帖资产，发布阶段应只接受单一 copy-ready Markdown 文件作为输入真源。
- 复合运营阶段可以整理素材、生成候选文案、做选题策划或系列编排；只有当内容已经收口为可直接发布的终稿后，才交给 `xhs-publish` 进入发布执行。
- `copy-ready` 在这里指发布阶段的内容治理约束与工作流边界，不代表当前仓库已经提供专门的 `copy-ready` CLI 子命令或机器接口。
- CLI 输出为 JSON 格式，结构化呈现给用户。
- 操作频率不宜过高，保持合理间隔。

## 子技能概览

### xhs-auth — 认证管理

管理小红书登录状态和多账号切换。

| 命令 | 功能 |
|------|------|
| `cli.py check-login` | 检查登录状态，返回推荐登录方式 |
| `cli.py login` | 二维码登录（有界面环境） |
| `cli.py send-code --phone <号码>` | 手机登录第一步：发送验证码 |
| `cli.py verify-code --code <验证码>` | 手机登录第二步：提交验证码 |
| `cli.py delete-cookies` | 清除 cookies（退出/切换账号） |

### xhs-publish — 内容发布

负责发布执行与发布前校验，覆盖图文、视频、长文、定时发布，以及基于现成 copy-ready 终稿进入的发布执行路径。

| 命令 | 功能 |
|------|------|
| `cli.py publish` | 图文一步发布（仅使用用户已准备好的本地图片） |
| `cli.py fill-publish` | 图文分步填写，供用户在浏览器中预览 |
| `cli.py click-publish` | 在用户确认预览后点击发布 |
| `cli.py save-draft` | 用户取消正式发布时保存草稿 |
| `cli.py publish-video` | 视频发布 |
| `cli.py long-article` | 长文填写并进入排版流程 |

### xhs-explore — 内容发现

搜索笔记、查看详情、获取用户资料。

| 命令 | 功能 |
|------|------|
| `cli.py list-feeds` | 获取首页推荐 Feed |
| `cli.py search-feeds` | 关键词搜索笔记 |
| `cli.py get-feed-detail` | 获取笔记完整内容和评论 |
| `cli.py user-profile` | 获取用户主页信息 |

### xhs-interact — 社交互动

发表评论、回复、点赞、收藏。

| 命令 | 功能 |
|------|------|
| `cli.py post-comment` | 对笔记发表评论 |
| `cli.py reply-comment` | 回复指定评论 |
| `cli.py like-feed` | 点赞 / 取消点赞 |
| `cli.py favorite-feed` | 收藏 / 取消收藏 |

### xhs-content-ops — 复合运营

负责组合多步骤运营工作流，包括竞品分析、热点追踪、内容创作、互动管理，以及系列选题、编排与草稿整理。

## 工作原理：Bridge 模式

本系统采用 **Extension Bridge 模式**与小红书交互：
1. 你（Agent）执行 `python scripts/cli.py` 发出指令。
2. CLI 将指令发送给本地 WebSocket 服务 `scripts/bridge_server.py`。
3. 用户浏览器中安装的 **XHS Bridge 扩展**连接到该服务，接收指令。
4. 扩展在用户本地 Chrome 的真实标签页、真实登录态下执行点击、输入、抓取等页面操作。
5. 执行结果经由 Bridge 返回给 CLI，再以 JSON 输出给 Agent。

> Bridge 模式不是远程托管浏览器，也不是无头模拟器；它依赖用户本机浏览器、扩展和本地登录态完成执行。
>
> 更详细的架构图见 `ARCHITECTURE.md`。

## 快速开始

```bash
# 1. 启动 Chrome
python scripts/chrome_launcher.py

# 2. 检查登录状态
python scripts/cli.py check-login

# 3. 登录（如需要）
python scripts/cli.py login

# 4. 搜索笔记
python scripts/cli.py search-feeds --keyword "关键词"

# 5. 查看笔记详情
python scripts/cli.py get-feed-detail \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN

# 6. 发布图文
python scripts/cli.py publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/abs/path/pic1.jpg"

# 7. 发表评论
python scripts/cli.py post-comment \
  --feed-id FEED_ID \
  --xsec-token XSEC_TOKEN \
  --content "评论内容"

# 8. 点赞
python scripts/cli.py like-feed \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN
```

## 失败处理

- **未登录**：提示用户执行登录流程（xhs-auth）。
- **Chrome 未启动**：使用 `chrome_launcher.py` 启动浏览器。
- **缺少图片**：告知用户先准备本地图片绝对路径，本 skill 不负责生成或下载图片。
- **操作超时**：检查网络连接，适当增加等待时间。
- **频率限制**：降低操作频率，增大间隔。
