from __future__ import annotations

from pathlib import Path

from channel_pack_core.adapters.base import ValidationAdapter
from channel_pack_core.models import ArtifactSpec, ChannelPack


VALID_MODES = {"single", "series"}


def validate_pack(pack: ChannelPack, adapter: ValidationAdapter, specs: list[ArtifactSpec]) -> None:
    if pack.mode not in VALID_MODES:
        raise ValueError(f"不支持的 mode: {pack.mode}")
    if not pack.posts:
        raise ValueError("posts 不能为空")
    if not Path(pack.source_markdown).is_file():
        raise FileNotFoundError(f"source_markdown 不存在: {pack.source_markdown}")
    adapter.validate(pack, specs)
