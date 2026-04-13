from __future__ import annotations

from channel_pack_core.adapters.base import StructureAdapter, ValidationAdapter
from channel_pack_core.models import ArtifactSpec, ChannelPack


class XiaohongshuStructureAdapter(StructureAdapter):
    channel_name = "xiaohongshu"

    def artifact_specs(self) -> list[ArtifactSpec]:
        return [
            ArtifactSpec("draft", "drafts/{index:02d}-{slug}.md", True, "markdown", "Draft content"),
            ArtifactSpec("final", "final/{index:02d}-最终发帖版.md", True, "markdown", "Final content"),
            ArtifactSpec("analysis", "analysis/post-{index:02d}-analysis.md", True, "markdown", "Analysis"),
            ArtifactSpec("publish_pack", "analysis/post-{index:02d}-publish-pack.md", True, "markdown", "Publish pack"),
            ArtifactSpec("copy_ready", "analysis/post-{index:02d}-copy-ready.md", True, "markdown", "Copy-ready"),
            ArtifactSpec("assets", "assets/{index:02d}-首图与配图脚本.md", False, "asset-note", "Asset note"),
        ]

    def render_index(self, pack: ChannelPack) -> str:
        lines = [
            f"# {pack.series_slug}｜小红书系列",
            "",
            f"- 来源文章：`{pack.source_markdown}`",
            f"- 渠道目录：`{pack.output_root}/{pack.series_slug}`",
            "",
            "## 当前发布台账（唯一真源）",
            "",
            "| 篇次 | 标题 | final | copy-ready | assets | 状态 | 发布时间 |",
            "|---|---|---|---|---|---|---|",
        ]
        for post in pack.posts:
            number = f"{post.index:02d}"
            assets = f"`assets/{number}-首图与配图脚本.md`" if "assets" in post.artifacts else "-"
            lines.append(
                f"| {number} | {post.title} | `final/{number}-最终发帖版.md` | `analysis/post-{number}-copy-ready.md` | {assets} | 待发送 | - |"
            )
        return "\n".join(lines) + "\n"


class XiaohongshuValidationAdapter(ValidationAdapter):
    def validate(self, pack: ChannelPack, specs: list[ArtifactSpec]) -> None:
        if pack.mode == "single" and len(pack.posts) != 1:
            raise ValueError("single 模式只能包含 1 篇文章")
        required_names = {spec.name for spec in specs if spec.required}
        for post in pack.posts:
            missing = sorted(required_names - set(post.artifacts))
            if missing:
                raise ValueError(f"post[{post.index}] 缺少字段: {', '.join(missing)}")
