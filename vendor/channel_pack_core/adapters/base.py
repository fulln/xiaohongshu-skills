from __future__ import annotations

from typing import Protocol

from channel_pack_core.models import ArtifactSpec, ChannelPack


class StructureAdapter(Protocol):
    channel_name: str

    def artifact_specs(self) -> list[ArtifactSpec]:
        ...

    def render_index(self, pack: ChannelPack) -> str:
        ...


class ValidationAdapter(Protocol):
    def validate(self, pack: ChannelPack, specs: list[ArtifactSpec]) -> None:
        ...
