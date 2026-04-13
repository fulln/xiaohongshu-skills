from __future__ import annotations

from pathlib import Path

from channel_pack_core.adapters.base import StructureAdapter, ValidationAdapter
from channel_pack_core.models import ChannelPack, ChannelPackResult
from channel_pack_core.validators import validate_pack


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_pack(pack: ChannelPack, structure: StructureAdapter, validation: ValidationAdapter) -> ChannelPackResult:
    specs = structure.artifact_specs()
    validate_pack(pack, validation, specs)

    base_dir = Path(pack.output_root) / pack.series_slug
    if base_dir.exists():
        raise FileExistsError(f"输出目录已存在: {base_dir}")

    base_dir.mkdir(parents=True, exist_ok=False)
    for post in pack.posts:
        for spec in specs:
            if spec.name not in post.artifacts:
                continue
            relative_path = spec.path_pattern.format(index=post.index, slug=post.slug)
            _write(base_dir / relative_path, post.artifacts[spec.name])
    _write(base_dir / "index.md", structure.render_index(pack))
    return ChannelPackResult(base_dir=str(base_dir))
