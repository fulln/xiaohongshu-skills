from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cli


@pytest.fixture
def tmp_copy_ready(tmp_path: Path) -> Path:
    path = tmp_path / "post-03-copy-ready.md"
    path.write_text(
        """# Post 03｜可直接复制发帖版

## 发帖标题

真正的 AI Coding 高手，最后都在搭运行壳

## 正文（可直接复制）

第一段。

## 封面文案

高手不是会更多命令，而是在搭一套运行壳

## 标签

#AICoding #ClaudeCode #AI编程

## 首评（建议发布后立刻发）

你现在最缺的，是 skill、hooks，还是验证体系？

## 配图执行

- 配图脚本：`../assets/03-首图与配图脚本.md`
""",
        encoding="utf-8",
    )
    return path


def test_copy_ready_parser_command_outputs_required_fields(tmp_copy_ready: Path, capsys: pytest.CaptureFixture[str]) -> None:
    args = SimpleNamespace(copy_ready_file=str(tmp_copy_ready))

    with pytest.raises(SystemExit) as exc:
        cli.cmd_parse_copy_ready(args)

    assert exc.value.code == 0
    output = capsys.readouterr().out
    assert '"title": "真正的 AI Coding 高手，最后都在搭运行壳"' in output
    assert '"tags": [' in output


def test_build_parser_registers_copy_ready_commands() -> None:
    parser = cli.build_parser()

    parse_args = parser.parse_args(["parse-copy-ready", "--copy-ready-file", "/tmp/post-03-copy-ready.md"])
    assert parse_args.command == "parse-copy-ready"

    fill_args = parser.parse_args([
        "fill-publish-copy-ready",
        "--copy-ready-file",
        "/tmp/post-03-copy-ready.md",
        "--images",
        "/tmp/1.jpg",
    ])
    assert fill_args.command == "fill-publish-copy-ready"

    publish_args = parser.parse_args([
        "publish-copy-ready",
        "--copy-ready-file",
        "/tmp/post-03-copy-ready.md",
        "--images",
        "/tmp/1.jpg",
    ])
    assert publish_args.command == "publish-copy-ready"


def test_fill_publish_copy_ready_rejects_non_copy_ready_path(tmp_path: Path) -> None:
    wrong = tmp_path / "03-最终发帖版.md"
    wrong.write_text("# final\n", encoding="utf-8")
    args = SimpleNamespace(
        copy_ready_file=str(wrong),
        images=["/tmp/1.jpg"],
        schedule_at=None,
        original=False,
        visibility=None,
    )

    with pytest.raises(ValueError, match="不是 copy-ready 文件"):
        cli._load_copy_ready_publish_args(args)


def test_fill_publish_copy_ready_cleans_temp_files_on_downstream_error(tmp_copy_ready: Path) -> None:
    captured: dict[str, Path] = {}

    def fake_fill_publish(args: SimpleNamespace) -> None:
        captured["title_file"] = Path(args.title_file)
        captured["content_file"] = Path(args.content_file)
        assert captured["title_file"].exists()
        assert captured["content_file"].exists()
        raise RuntimeError("boom")

    args = SimpleNamespace(
        copy_ready_file=str(tmp_copy_ready),
        images=["/tmp/1.jpg"],
        schedule_at=None,
        original=False,
        visibility=None,
    )

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(cli, "cmd_fill_publish", fake_fill_publish)
    try:
        with pytest.raises(RuntimeError, match="boom"):
            cli.cmd_fill_publish_copy_ready(args)
    finally:
        monkeypatch.undo()

    assert captured["title_file"].exists() is False
    assert captured["content_file"].exists() is False
