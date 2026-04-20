from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import tempfile

VENDOR_ROOT = Path(__file__).resolve().parent.parent / "vendor"
if str(VENDOR_ROOT) not in sys.path:
    sys.path.insert(0, str(VENDOR_ROOT))

from channel_pack_core.api import load_pack_from_payload, scaffold_xiaohongshu_pack

XAI_API_KEY = os.environ.get("XAI_API_KEY", "")


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


def _validate_request(request: ChannelPackRequest) -> None:
    if request.generate_assets:
        for offset, post in enumerate(request.posts, start=request.start_index):
            if "assets" not in post:
                raise ValueError(f"post[{offset}] 缺少字段: assets")


def scaffold_channel_pack(request: ChannelPackRequest) -> ChannelPackResult:
    _validate_request(request)
    payload = {
        "channel": request.channel_name,
        "series_slug": request.series_slug,
        "mode": request.mode,
        "posts": [
            {
                "index": request.start_index + offset,
                "slug": post["slug"],
                "title": post["title"],
                "artifacts": {
                    key: value
                    for key, value in post.items()
                    if key in {"draft", "final", "analysis", "publish_pack", "assets"}
                },
                "metadata": {},
            }
            for offset, post in enumerate(request.posts)
        ],
    }
    request.output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".payload.json",
        prefix=f".{request.series_slug}.",
        dir=request.output_root,
        delete=False,
    ) as payload_handle:
        payload_handle.write(__import__("json").dumps(payload, ensure_ascii=False))
        payload_file = Path(payload_handle.name)
    try:
        load_pack_from_payload(str(request.source_markdown), str(request.output_root), str(payload_file))
        result = scaffold_xiaohongshu_pack(str(request.source_markdown), str(request.output_root), str(payload_file))
        base_dir = Path(result.base_dir)

        # Auto-generate images for assets if enabled
        if request.generate_assets:
            for post in request.posts:
                if "assets" not in post:
                    continue
                _generate_cover_image(
                    title=post.get("title", ""),
                    slug=post.get("slug", ""),
                    assets_dir=base_dir / "assets",
                    index=post.get("index", 1),
                )

        return ChannelPackResult(base_dir=base_dir)
    finally:
        payload_file.unlink(missing_ok=True)


def _generate_cover_image(title: str, slug: str, assets_dir: Path, index: int) -> None:
    """Generate a cover image using xAI Grok Vision API."""
    # Build prompt from title/slug
    prompt = f"Create a visually appealing, colorful cover image for a Xiaohongshu post about '{title}'. "
    prompt += "Modern Chinese social media style, vibrant, attractive, no text."

    output_path = assets_dir / f"{index:02d}-cover.png"

    script_dir = Path(__file__).parent
    result = subprocess.run(
        [sys.executable, str(script_dir / "generate_image.py"), "-p", prompt, "-o", str(output_path), "-k", XAI_API_KEY],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"[AI] Generated cover image: {output_path}")
    else:
        print(f"[AI] Failed to generate image: {result.stderr}", file=sys.stderr)
