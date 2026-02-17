# coding utf-8

from pathlib import Path

from fastapi import (
    APIRouter,
    Header,
    HTTPException,
)

from fastapi.responses import StreamingResponse

from ......domain.entities.core import IMediaFile

from ......domain.tools import stream_media

media_router = APIRouter(tags=["Media"])


@media_router.get(
    "/media/{full_path:path}",
    include_in_schema=False,
)
async def get_media(
    full_path: str,
    range: str | None = Header(default=None),
) -> StreamingResponse:
    try:
        full_path = full_path.replace("uploads/", "")

        file = IMediaFile(Path("uploads") / full_path)
        return stream_media(file, range)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
