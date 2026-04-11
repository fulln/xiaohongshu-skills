from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from copy_ready_parser import CopyReadyPayload, load_copy_ready_payload


def write_note(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "post-03-copy-ready.md"
    path.write_text(body, encoding="utf-8")
    return path


def test_load_copy_ready_payload_reads_required_sections(tmp_path: Path) -> None:
    path = write_note(
        tmp_path,
        """# Post 03｜可直接复制发帖版

## 发帖标题

真正的 AI Coding 高手，最后都在搭运行壳

## 正文（可直接复制）

第一段。

第二段。

## 封面文案

高手不是会更多命令，而是在搭一套运行壳

## 标签

#AICoding #ClaudeCode #AI编程

## 首评（建议发布后立刻发）

你现在最缺的，是 skill、hooks，还是验证体系？

## 配图执行

- 配图脚本：`../assets/03-首图与配图脚本.md`
- 建议张数：8 张

## 发帖前最后确认

- 标签使用本文件 `## 标签`
""",
    )

    payload = load_copy_ready_payload(path)

    assert payload.title == "真正的 AI Coding 高手，最后都在搭运行壳"
    assert payload.content == "第一段。\n\n第二段。"
    assert payload.cover_text == "高手不是会更多命令，而是在搭一套运行壳"
    assert payload.tags == ["AICoding", "ClaudeCode", "AI编程"]
    assert "skill、hooks" in payload.first_comment


def test_load_copy_ready_payload_rejects_missing_tags_section(tmp_path: Path) -> None:
    path = write_note(
        tmp_path,
        """# Post 03｜可直接复制发帖版

## 发帖标题

标题

## 正文（可直接复制）

正文

## 封面文案

封面

## 首评（建议发布后立刻发）

首评
""",
    )

    with pytest.raises(ValueError, match="缺少必填章节: 标签"):
        load_copy_ready_payload(path)


def test_load_copy_ready_payload_rejects_non_copy_ready_file(tmp_path: Path) -> None:
    path = tmp_path / "03-最终发帖版.md"
    path.write_text("# final\n", encoding="utf-8")

    with pytest.raises(ValueError, match="不是 copy-ready 文件"):
        load_copy_ready_payload(path)
