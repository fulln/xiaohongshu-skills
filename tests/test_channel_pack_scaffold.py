from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from channel_pack_scaffold import ChannelPackRequest, scaffold_channel_pack


def test_scaffold_channel_pack_creates_single_post_structure(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    output_root = tmp_path / "output"

    request = ChannelPackRequest(
        source_markdown=source,
        output_root=output_root,
        series_slug="claudecode-openclaw",
        mode="single",
        generate_assets=True,
        start_index=1,
        channel_name="xiaohongshu",
        posts=[
            {
                "slug": "ClaudeCode也可以是OpenClaw",
                "draft": "draft body",
                "final": "final body",
                "analysis": "analysis body",
                "publish_pack": "pack body",
                "copy_ready": "copy ready body",
                "assets": "assets body",
                "title": "Claude Code，其实也可以是 OpenClaw",
            }
        ],
    )

    result = scaffold_channel_pack(request)

    base = output_root / "claudecode-openclaw"
    assert result.base_dir == base
    assert (base / "drafts" / "01-ClaudeCode也可以是OpenClaw.md").read_text(encoding="utf-8") == "draft body"
    assert (base / "final" / "01-最终发帖版.md").read_text(encoding="utf-8") == "final body"
    assert (base / "analysis" / "post-01-analysis.md").read_text(encoding="utf-8") == "analysis body"
    assert (base / "analysis" / "post-01-publish-pack.md").read_text(encoding="utf-8") == "pack body"
    assert (base / "analysis" / "post-01-copy-ready.md").read_text(encoding="utf-8") == "copy ready body"
    assert (base / "assets" / "01-首图与配图脚本.md").read_text(encoding="utf-8") == "assets body"
    index_text = (base / "index.md").read_text(encoding="utf-8")
    assert "Claude Code，其实也可以是 OpenClaw" in index_text
    assert "状态 | 发布时间" in index_text


def test_scaffold_channel_pack_refuses_existing_target_and_supports_series(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    output_root = tmp_path / "output"

    request = ChannelPackRequest(
        source_markdown=source,
        output_root=output_root,
        series_slug="series-a",
        mode="series",
        generate_assets=False,
        start_index=1,
        channel_name="xiaohongshu",
        posts=[
            {
                "slug": "post-one",
                "draft": "draft 1",
                "final": "final 1",
                "analysis": "analysis 1",
                "publish_pack": "pack 1",
                "copy_ready": "copy 1",
                "assets": "unused 1",
                "title": "标题1",
            },
            {
                "slug": "post-two",
                "draft": "draft 2",
                "final": "final 2",
                "analysis": "analysis 2",
                "publish_pack": "pack 2",
                "copy_ready": "copy 2",
                "assets": "unused 2",
                "title": "标题2",
            },
        ],
    )

    result = scaffold_channel_pack(request)
    base = result.base_dir
    assert (base / "drafts" / "01-post-one.md").exists()
    assert (base / "drafts" / "02-post-two.md").exists()
    assert (base / "assets").exists() is False
    index_text = (base / "index.md").read_text(encoding="utf-8")
    assert "| 01 | 标题1 |" in index_text
    assert "| 02 | 标题2 |" in index_text



def test_scaffold_channel_pack_rejects_invalid_post_before_writing(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    output_root = tmp_path / "output"

    request = ChannelPackRequest(
        source_markdown=source,
        output_root=output_root,
        series_slug="broken-series",
        mode="single",
        generate_assets=True,
        start_index=1,
        channel_name="xiaohongshu",
        posts=[
            {
                "slug": "broken-post",
                "draft": "draft",
                "final": "final",
                "analysis": "analysis",
                "publish_pack": "pack",
                "copy_ready": "copy",
                "title": "标题缺 assets",
            }
        ],
    )

    with pytest.raises(ValueError, match=r"posts\[0\] 缺少字段: assets"):
        scaffold_channel_pack(request)

    assert (output_root / "broken-series").exists() is False
