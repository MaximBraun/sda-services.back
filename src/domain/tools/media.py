# coding utf-8

from typing import (
    Any,
    Generator,
)

from json import (
    loads,
    JSONDecodeError,
)

from subprocess import CompletedProcess, run

from fastapi.responses import StreamingResponse

from ..entities.core import IMediaFile

from ..constants import CHUNK_SIZE, SUBTITLE_COMMAND


def read_file_chunked(
    path: str,
    start: int = 0,
    end: int | None = None,
) -> Generator[bytes, Any, None]:
    with open(path, "rb") as f:
        f.seek(start)
        remaining = (end - start + 1) if end is not None else None

        while True:
            read_len = min(CHUNK_SIZE, remaining) if remaining else CHUNK_SIZE
            data = f.read(read_len)
            if not data:
                break
            yield data
            if remaining:
                remaining -= len(data)
                if remaining <= 0:
                    break


def parse_range(
    range_header: str,
    file_size: int,
) -> tuple[int, int]:
    if not range_header.lower().startswith("bytes="):
        raise ValueError("Invalid Range header format")

    parts = range_header.removeprefix("bytes=").split("-")
    try:
        start = int(parts[0])
        end = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
    except (IndexError, ValueError):
        raise ValueError("Invalid Range values")

    if start > end or end >= file_size:
        raise ValueError("Range out of bounds")

    return start, end


def stream_media(
    media: IMediaFile, range_header: str | None = None
) -> StreamingResponse:
    if media.is_video and range_header:
        start, end = parse_range(range_header, media.size)
        length = end - start + 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{media.size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
            "Content-Type": media.mime_type,
        }

        return StreamingResponse(
            read_file_chunked(media.path, start, end),
            status_code=206,
            headers=headers,
            media_type=media.mime_type,
        )

    else:
        headers = {
            "Accept-Ranges": "bytes" if media.is_video else "none",
            "Content-Length": str(media.size),
            "Content-Type": media.mime_type,
        }

        return StreamingResponse(
            read_file_chunked(media.path),
            status_code=200,
            headers=headers,
            media_type=media.mime_type,
        )


def overlay_subtitles(
    input_path: str,
    subtitle_path: str,
    font_name: str,
    output_path: str,
) -> CompletedProcess[bytes]:
    command = [
        arg.format(
            input_path=input_path,
            subtitle_path=subtitle_path,
            font_name=font_name,
            output_path=output_path,
        )
        for arg in SUBTITLE_COMMAND
    ]

    return run(command, check=True)


async def has_audio(filepath: str) -> bool:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "json",
        filepath,
    ]
    result = run(cmd, capture_output=True, text=True)
    try:
        info = loads(result.stdout or "{}")
    except JSONDecodeError:
        return False
    return bool(info.get("streams"))
