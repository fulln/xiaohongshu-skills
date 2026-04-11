---
name: xhs-channel-pack
description: |
  小红书内容拆解技能。把用户已有的 Markdown 文章拆成可发布的小红书 channel 包。
  当用户要求把 Obsidian/Markdown 文章拆成小红书草稿、final、copy-ready、publish pack 或系列资产时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - uv
    emoji: "🧩"
    os:
      - darwin
      - linux
---

# 小红书 Channel Pack 拆解

你负责把用户已有的 Markdown 文章拆成标准化的小红书 channel 包。

## 必要输入

- `source_markdown`：原文绝对路径
- `output_root`：输出根目录绝对路径
- `series_slug`：输出目录名

## 默认行为

- 默认 `mode=single`
- 允许显式指定 `mode=series`
- 不修改原文
- 不直接发布
- 不生成图片文件
- 只生成标准结构的发布资产

## 标准输出

- `drafts/`
- `final/`
- `analysis/post-xx-analysis.md`
- `analysis/post-xx-publish-pack.md`
- `analysis/post-xx-copy-ready.md`
- `assets/xx-首图与配图脚本.md`（若启用）
- `index.md`

## 执行要求

1. 先判断原文更适合单篇还是多篇
2. 若用户未明确给 `output_root` 或 `series_slug`，先补问
3. 先生成内容，再把内容写入一个 JSON payload 文件
4. 最后只通过以下命令落盘：

```bash
python scripts/cli.py scaffold-channel-pack \
  --source-markdown "/abs/source.md" \
  --output-root "/abs/output-root" \
  --series-slug "series-slug" \
  --payload-file "/abs/payload.json" \
  --mode single \
  --generate-assets
```

5. 完成后汇报生成的目录和文件
