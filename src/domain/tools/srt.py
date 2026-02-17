# coding utf-8

from typing import Any

from srt import (
    Subtitle,
    compose,
)

from datetime import timedelta


def generate_srt(
    segments: list[dict[str, Any]],
) -> str:
    subtitles: list[Subtitle] = [
        Subtitle(
            index=i,
            start=timedelta(seconds=seg.get("start", 0)),
            end=timedelta(seconds=seg.get("end", 0)),
            content=seg.get("text", "").strip(),
        )
        for i, seg in enumerate(segments, 1)
        if seg.get("text", "").strip()
    ]

    return compose(subtitles)
