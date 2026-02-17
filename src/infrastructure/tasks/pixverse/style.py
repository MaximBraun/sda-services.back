# coding utf-8

from typing import Any

from os import remove

from pathlib import Path

from .core import PixverseCelery

from ....domain.repositories import IDatabase

from ...orm.database.models import PixverseStyles

from ...orm.database.repositories import PixverseStyleRepository


class PixverseStyleCelery(PixverseCelery):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._repository = PixverseStyleRepository(
            IDatabase(self._conf),
        )

    def get_static_files(
        self,
        directory: str = "uploads",
    ) -> list[str]:
        return [
            str(file)
            for file in Path(
                directory,
            ).rglob("*")
            if file.is_file()
        ]

    def delete_file(
        self,
        filename: str,
    ) -> None:
        return remove(
            Path(filename),
        )

    def database_files_list(
        self,
        database_files: list[PixverseStyles],
    ) -> list[str]:
        return [
            f.preview_large.split("/")[-1]
            for f in database_files
            if f.preview_large is not None
        ] + [
            f.preview_small.split("/")[-1]
            for f in database_files
            if f.preview_small is not None
        ]

    def clean_static_files(
        self,
        filename: str,
        database_files: list[str],
    ) -> Any:
        if filename not in database_files:
            return self.delete_file(
                filename,
            )

    async def clean_files(
        self,
    ) -> Any:
        database_files: list[PixverseStyles] = await self._repository.fetch_all()
        files: list[str] = self.get_static_files()
        for file in files:
            return self.clean_static_files(
                file,
                self.database_files_list(
                    database_files,
                ),
            )
