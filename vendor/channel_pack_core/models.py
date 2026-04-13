from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtifactSpec:
    name: str
    path_pattern: str
    required: bool
    kind: str
    description: str


@dataclass(frozen=True)
class ChannelPost:
    index: int
    slug: str
    title: str
    artifacts: dict[str, str]
    metadata: dict[str, str]


@dataclass(frozen=True)
class LedgerEntry:
    post_index: str
    title: str
    artifacts: dict[str, str]
    status: str
    published_at: str
    extra: dict[str, str]


@dataclass(frozen=True)
class ChannelPack:
    source_markdown: str
    output_root: str
    channel: str
    series_slug: str
    mode: str
    posts: list[ChannelPost]
    ledger: list[LedgerEntry]


@dataclass(frozen=True)
class ChannelPackResult:
    base_dir: str
