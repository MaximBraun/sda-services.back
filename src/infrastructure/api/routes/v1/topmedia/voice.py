# coding utf-8

from fastapi import (
    APIRouter,
    Depends,
)


from ....views.v1 import TopmediaVoiceView

from ......interface.schemas.api import Voice

from .....factroies.api.v1 import TopmediaVoiceViewFactory


topmedia_voice_router = APIRouter(tags=["Voices"])


@topmedia_voice_router.get(
    "/voices",
    response_model=list[Voice],
    response_model_exclude_none=True,
)
async def fetch_voices(
    view: TopmediaVoiceView = Depends(TopmediaVoiceViewFactory.create),
) -> list[Voice]:
    return await view.fetch_voices()
