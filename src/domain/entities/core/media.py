# coding utf-8

from pathlib import Path

from mimetypes import guess_type


class IMediaFile:
    def __init__(
        self,
        path: Path,
    ) -> None:
        self._path = path.resolve()

        if not self._path.exists() or not self._path.is_file():
            raise FileNotFoundError("Media file does not exist.")

        self._size = self._path.stat().st_size
        self._mime_type = guess_type(str(self._path))[0] or "application/octet-stream"

    @property
    def path(
        self,
    ) -> Path:
        return self._path

    @property
    def size(
        self,
    ) -> int:
        return self._size

    @property
    def mime_type(
        self,
    ) -> str:
        return self._mime_type

    @property
    def is_video(
        self,
    ) -> bool:
        return self._mime_type.startswith(
            "video/",
        )
