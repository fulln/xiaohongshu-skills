from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import channel_pack_scaffold
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


def test_scaffold_channel_pack_uses_unique_temp_payload_filename(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source.md"
    source.write_text("# Source\n", encoding="utf-8")
    output_root = tmp_path / "output"
    payload_paths: list[Path] = []

    def fake_load_pack_from_payload(source_path: str, output_root_path: str, payload_path: str) -> None:
        payload_paths.append(Path(payload_path))
        assert Path(source_path) == source
        assert Path(output_root_path) == output_root
        assert Path(payload_path).parent == output_root
        assert Path(payload_path).name != ".claudecode-openclaw.payload.json"
        json.loads(Path(payload_path).read_text(encoding="utf-8"))

    def fake_scaffold_xiaohongshu_pack(source_path: str, output_root_path: str, payload_path: str):
        payload_paths.append(Path(payload_path))
        return type("Result", (), {"base_dir": str(output_root / "claudecode-openclaw")})()

    monkeypatch.setattr(channel_pack_scaffold, "load_pack_from_payload", fake_load_pack_from_payload)
    monkeypatch.setattr(channel_pack_scaffold, "scaffold_xiaohongshu_pack", fake_scaffold_xiaohongshu_pack)

    request = ChannelPackRequest(
        source_markdown=source,
        output_root=output_root,
        series_slug="claudecode-openclaw",
        mode="single",
        generate_assets=False,
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
                "title": "Claude Code，其实也可以是 OpenClaw",
            }
        ],
    )

    scaffold_channel_pack(request)

    assert len(payload_paths) == 2
    assert payload_paths[0] == payload_paths[1]
    assert not payload_paths[0].exists()


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

    with pytest.raises(ValueError, match=r"post\[1\] 缺少字段: assets"):
        scaffold_channel_pack(request)
