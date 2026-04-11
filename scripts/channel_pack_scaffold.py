from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChannelPackResult:
    base_dir: Path


@dataclass(frozen=True)
class ChannelPackRequest:
    source_markdown: Path
    output_root: Path
    series_slug: str
    mode: str
    generate_assets: bool
    start_index: int
    channel_name: str
    posts: list[dict[str, str]]


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _validate_request(request: ChannelPackRequest) -> None:
    if request.mode not in {"single", "series"}:
        raise ValueError(f"不支持的 mode: {request.mode}")
    if request.start_index < 1:
        raise ValueError("start_index 必须 >= 1")
    if not request.posts:
        raise ValueError("posts 不能为空")
    if request.mode == "single" and len(request.posts) != 1:
        raise ValueError("single 模式只能包含 1 篇文章")


def scaffold_channel_pack(request: ChannelPackRequest) -> ChannelPackResult:
    _validate_request(request)
    base_dir = request.output_root / request.series_slug
    if base_dir.exists():
        raise FileExistsError(f"输出目录已存在: {base_dir}")
    if not request.source_markdown.is_file():
        raise FileNotFoundError(f"source_markdown 不存在: {request.source_markdown}")

    base_dir.mkdir(parents=True, exist_ok=False)

    for offset, post in enumerate(request.posts, start=request.start_index):
        number = f"{offset:02d}"
        _write(base_dir / "drafts" / f"{number}-{post['slug']}.md", post["draft"])
        _write(base_dir / "final" / f"{number}-最终发帖版.md", post["final"])
        _write(base_dir / "analysis" / f"post-{number}-analysis.md", post["analysis"])
        _write(base_dir / "analysis" / f"post-{number}-publish-pack.md", post["publish_pack"])
        _write(base_dir / "analysis" / f"post-{number}-copy-ready.md", post["copy_ready"])
        if request.generate_assets:
            _write(base_dir / "assets" / f"{number}-首图与配图脚本.md", post["assets"])

    lines = [
        f"# {request.series_slug}｜小红书系列",
        "",
        f"- 来源文章：`{request.source_markdown}`",
        f"- 渠道目录：`{base_dir}`",
        "",
        "## 当前发布台账（唯一真源）",
        "",
        "| 篇次 | 标题 | final | copy-ready | assets | 状态 | 发布时间 |",
        "|---|---|---|---|---|---|---|",
    ]
    for offset, post in enumerate(request.posts, start=request.start_index):
        number = f"{offset:02d}"
        assets = f"`assets/{number}-首图与配图脚本.md`" if request.generate_assets else "-"
        lines.append(
            f"| {number} | {post['title']} | `final/{number}-最终发帖版.md` | `analysis/post-{number}-copy-ready.md` | {assets} | 待发送 | - |"
        )
    _write(base_dir / "index.md", "\n".join(lines) + "\n")

    return ChannelPackResult(base_dir=base_dir)
