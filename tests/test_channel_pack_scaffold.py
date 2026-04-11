from __future__ import annotations

import sys
from pathlib import Path

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
