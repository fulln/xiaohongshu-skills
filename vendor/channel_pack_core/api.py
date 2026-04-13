from __future__ import annotations

import json
from pathlib import Path

from channel_pack_core.adapters.xiaohongshu import XiaohongshuStructureAdapter, XiaohongshuValidationAdapter
from channel_pack_core.models import ChannelPack, ChannelPost
from channel_pack_core.writer import write_pack


def load_pack_from_payload(source_markdown: str, output_root: str, payload_file: str) -> ChannelPack:
    data = json.loads(Path(payload_file).read_text(encoding="utf-8"))
    posts = [
        ChannelPost(
            index=post["index"],
            slug=post["slug"],
            title=post["title"],
            artifacts=post["artifacts"],
            metadata=post.get("metadata", {}),
        )
        for post in data["posts"]
    ]
    return ChannelPack(
        source_markdown=source_markdown,
        output_root=output_root,
        channel=data["channel"],
        series_slug=data["series_slug"],
        mode=data["mode"],
        posts=posts,
        ledger=[],
    )


def scaffold_xiaohongshu_pack(source_markdown: str, output_root: str, payload_file: str):
    pack = load_pack_from_payload(source_markdown, output_root, payload_file)
    if pack.channel != "xiaohongshu":
        raise ValueError(f"expected payload channel 'xiaohongshu', got {pack.channel!r}")
    return write_pack(pack, XiaohongshuStructureAdapter(), XiaohongshuValidationAdapter())
