from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cli


def test_build_parser_registers_scaffold_channel_pack_command() -> None:
    parser = cli.build_parser()

    args = parser.parse_args(
        [
            "scaffold-channel-pack",
            "--source-markdown",
            "/tmp/source.md",
            "--output-root",
            "/tmp/out",
            "--series-slug",
            "demo-series",
            "--mode",
            "single",
            "--payload-file",
            "/tmp/payload.json",
        ]
    )

    assert args.command == "scaffold-channel-pack"
    assert args.mode == "single"


def test_cmd_scaffold_channel_pack_outputs_created_base_dir(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.md"
    payload = tmp_path / "payload.json"
    source.write_text("# Source\n", encoding="utf-8")
    payload.write_text(
        json.dumps(
            {
                "posts": [
                    {
                        "slug": "post-one",
                        "draft": "draft",
                        "final": "final",
                        "analysis": "analysis",
                        "publish_pack": "pack",
                        "copy_ready": "copy",
                        "assets": "assets",
                        "title": "标题1",
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    args = SimpleNamespace(
        source_markdown=str(source),
        output_root=str(tmp_path / "out"),
        series_slug="demo-series",
        mode="single",
        generate_assets=True,
        start_index=1,
        channel_name="xiaohongshu",
        payload_file=str(payload),
    )

    with pytest.raises(SystemExit) as exc:
        cli.cmd_scaffold_channel_pack(args)

    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert '"base_dir":' in out
    assert '"post_count": 1' in out
