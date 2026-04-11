from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


_REQUIRED_SECTIONS = {
    "发帖标题": "title",
    "正文（可直接复制）": "content",
    "封面文案": "cover_text",
    "标签": "tags",
    "首评（建议发布后立刻发）": "first_comment",
}


@dataclass(frozen=True)
class CopyReadyPayload:
    path: Path
    title: str
    content: str
    cover_text: str
    tags: list[str]
    first_comment: str


def _trim(text: str) -> str:
    return text.strip()


def _parse_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[name] = _trim(text[start:end])
    return sections


def _parse_tags(raw: str) -> list[str]:
    tags = []
    for token in raw.split():
        token = token.strip()
        if not token:
            continue
        tags.append(token.lstrip("#"))
    return tags


def load_copy_ready_payload(path: str | Path) -> CopyReadyPayload:
    resolved = Path(path).resolve()
    if "copy-ready" not in resolved.name:
        raise ValueError("不是 copy-ready 文件")

    text = resolved.read_text(encoding="utf-8")
    sections = _parse_sections(text)

    missing = [name for name in _REQUIRED_SECTIONS if not _trim(sections.get(name, ""))]
    if missing:
        raise ValueError(f"缺少必填章节: {missing[0].replace('（建议发布后立刻发）', '')}")

    tags = _parse_tags(sections["标签"])
    if not tags:
        raise ValueError("缺少必填章节: 标签")

    return CopyReadyPayload(
        path=resolved,
        title=sections["发帖标题"],
        content=sections["正文（可直接复制）"],
        cover_text=sections["封面文案"],
        tags=tags,
        first_comment=sections["首评（建议发布后立刻发）"],
    )
