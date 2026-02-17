# coding utf-8

import re

from os import (
    path,
    remove,
)


import asyncio
import os
import json
from pydub import AudioSegment
from pydub.effects import normalize
import edge_tts
from faster_whisper import WhisperModel
from subprocess import run

from fastapi import (
    HTTPException,
    Request,
    UploadFile,
    Form,
    Depends,
    Query,
    APIRouter,
)

from uuid import uuid4

import tempfile

from ......domain.tools import (
    transcribe_audio,
    translate_batch,
    overlay_subtitles,
    generate_srt,
    has_audio,
    check_user_tokens,
)

from ......domain.constants import (
    BASE_STATIC_DIR,
    VOICE_LANGUAGE_MAPPING,
)

from ......domain.entities.qwen import (
    IT2TBody,
    II2RBody,
    IP2BBody,
    IIT2IBody,
    IT2PBody,
)

from ......domain.entities.chatgpt import I2CBody, IBody, T2PBody, TB2PBody, R2PBody

from ......domain.entities.wan import IT2ABody

from ......interface.schemas.external import ChatGPTResp, Antiques

from ....views.v1 import (
    QwenView,
    ChatGPTView,
    WanView,
)

from ......interface.schemas.external import (
    QwenAPIResponse,
    ChatGPTInstagram,
    ChatGPTSubtitle,
    ChatGPTResp,
)

from .....factroies.api.v1 import (
    QwenViewFactory,
    ChatGPTViewFactory,
    WanViewFactory,
)


chatgpt_router = APIRouter(tags=["Photo Generator"])

tmp_dir, finl_dir = map(
    lambda p: path.join(BASE_STATIC_DIR, p), ["tmp", "video/subtitles"]
)


def split_words(text: str) -> list[str]:
    # Сохраняем пунктуацию рядом со словами (как в Whisper)
    return [w.strip() for w in re.findall(r"\S+", text) if w.strip()]


@chatgpt_router.post(
    "/text2photo",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def text_to_photo(
    request: Request,
    body: IBody = Depends(),
    # app_id: str = Query(),
    # user_id: str = Query(),
    view: WanView = Depends(WanViewFactory.create),
) -> ChatGPTResp:
    data = await view.text_to_image(
        body,
        body.user_id,
        body.app_id,
    )

    while True:
        status = await view.fetch_media_status(
            data.media_id,
        )
        if status.media_urls == "generating":
            await asyncio.sleep(2)

            continue

        return ChatGPTResp(
            url=status.media_urls[0],
        )


@chatgpt_router.post(
    "/photo2photo",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def image_to_image(
    request: Request,
    image: UploadFile,
    body: IBody = Depends(),
    # app_id: str = Query(),
    # user_id: str = Query(),
    view: WanView = Depends(WanViewFactory.create),
) -> ChatGPTResp:
    data = await view.photo_to_photo(
        body,
        image,
        body.user_id,
        body.app_id,
    )

    while True:
        status = await view.fetch_media_status(
            data.media_id,
        )
        if status.media_urls == "generating":
            await asyncio.sleep(2)

            continue

        return ChatGPTResp(
            url=status.media_urls[0],
        )


@chatgpt_router.post(
    "/template2photo",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def template_to_photo(
    request: Request,
    image: UploadFile,
    body: T2PBody = Depends(),
    view: WanView = Depends(WanViewFactory.create),
) -> ChatGPTResp:
    data = await view.template_to_photo(
        body.id,
        image,
        body.user_id,
        body.app_id,
    )

    while True:
        status = await view.fetch_media_status(
            data.media_id,
        )
        if status.media_urls == "generating":
            await asyncio.sleep(2)

            continue

        return ChatGPTResp(
            url=status.media_urls[0],
        )


@chatgpt_router.post(
    "/template2avatar",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def template_to_avatar(
    request: Request,
    image: UploadFile,
    body: IT2ABody,
    data: T2PBody = Depends(),
    view: WanView = Depends(WanViewFactory.create),
) -> ChatGPTResp:
    data = await view.template_to_avatar(
        data.id,
        body,
        image,
        data.user_id,
        data.app_id,
    )

    while True:
        status = await view.fetch_media_status(
            data.media_id,
        )
        if status.media_urls == "generating":
            await asyncio.sleep(2)

            continue

        return ChatGPTResp(
            url=status.media_urls[0],
        )


@chatgpt_router.post(
    "/photo2toybox",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=5)
async def photo_to_toybox(
    request: Request,
    image: UploadFile,
    body: TB2PBody = Depends(),
    # app_id: str = Query(),
    # user_id: str = Query(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
) -> ChatGPTResp:
    return await view.template_toybox_to_photo(
        body,
        image,
        # app_id,
        # user_id,
    )


@chatgpt_router.post(
    "/edit2reshape",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
async def reshape_to_photo(
    image: UploadFile,
    body: R2PBody = Depends(),
    # app_id: str = Query(),
    # user_id: str = Query(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
) -> ChatGPTResp:
    return await view.reshape_photo(
        body,
        image,
        # app_id,
        # user_id,
    )


@chatgpt_router.post(
    "/text2post",
    response_model=ChatGPTInstagram,
    response_model_exclude_none=True,
)
async def text_to_post(
    body: IT2PBody = Depends(),
    app_id: str = Query(),
    user_id: str = Query(),
    view: QwenView = Depends(QwenViewFactory.create),
) -> ChatGPTInstagram:
    return await view.text_to_post(
        body,
        app_id,
        user_id,
    )


@chatgpt_router.post(
    "/face2swap",
    response_model=ChatGPTResp,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=10)
async def face_to_swap(
    request: Request,
    image: list[UploadFile],
    body: I2CBody = Depends(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
):
    return await view.face_to_swap(
        body,
        image,
    )


@chatgpt_router.post(
    "/photo2antiques",
    response_model=Antiques,
    # response_model_exclude_none=True,
)
# @check_user_tokens(method_cost=10)
async def photo_to_antiques(
    request: Request,
    image: UploadFile,
    body: I2CBody = Depends(),
    view: ChatGPTView = Depends(ChatGPTViewFactory.create),
) -> list[Antiques]:
    return await view.photo_to_antiques(
        image,
    )


@chatgpt_router.post(
    "/video2subtitle",
    response_model=ChatGPTSubtitle,
    response_model_exclude_none=True,
)
async def video_to_subtitle(
    video: UploadFile,
    target_lang: str = Form(...),
    font_name: str = Form("Arial"),
    view: QwenView = Depends(QwenViewFactory.create),
) -> ChatGPTSubtitle:
    input_path = path.join(tmp_dir, f"temp_{uuid4()}.mp4")
    srt_path = path.join(tmp_dir, f"temp_{uuid4()}.srt")
    output_filename = f"{uuid4()}.mp4"
    output_path = path.join(finl_dir, output_filename)

    with open(input_path, "wb") as f:
        f.write(await video.read())

    try:
        if not await has_audio(input_path):
            raise HTTPException(
                status_code=400,
                detail="No audio track found in the video.",
            )

        segments = await transcribe_audio(input_path)
        translated_segments = await translate_batch(segments, target_lang)
        srt_content = generate_srt(translated_segments)

        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        overlay_subtitles(input_path, srt_path, font_name, output_path)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No audio has been found in the video.",
        )

    finally:
        for tmp_file in (input_path, srt_path):
            if path.exists(tmp_file):
                remove(tmp_file)

    return ChatGPTSubtitle(
        url=output_path,
    )


@chatgpt_router.post(
    "/video2voice",
    response_model=ChatGPTSubtitle,
    response_model_exclude_none=True,
)
@check_user_tokens(method_cost=30)
async def video_to_voice(
    request: Request,
    video: UploadFile,
    app_id: str = Query(),
    user_id: str = Query(),
    target_lang: str = Form(...),
):
    voice = VOICE_LANGUAGE_MAPPING.get(target_lang)

    tmp = tempfile.gettempdir()
    input_path = os.path.join(tmp, f"in_{uuid4()}.mp4")
    output_audio_path = os.path.join(tmp, f"tts_{uuid4()}.wav")
    output_filename = f"{uuid4()}.mp4"
    output_path = os.path.join(finl_dir, output_filename)

    # 1. Сохраняем видео
    with open(input_path, "wb") as f:
        f.write(await video.read())

    try:
        # --- Длительность видео ---
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            input_path,
        ]
        result = run(cmd, capture_output=True, text=True, check=True)
        duration_sec = float(json.loads(result.stdout)["format"]["duration"])
        total_ms = int(duration_sec * 1000)

        # --- Транскрибация с word_timestamps ---
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = model.transcribe(
            input_path,
            word_timestamps=True,
            # language="ru",  # если известен
        )
        segments = list(segments)
        segments = [s for s in segments if s.words and s.text.strip()]

        if not segments:
            raise HTTPException(400, "No speech with words detected")

        from deep_translator import GoogleTranslator

        all_segments_data = []
        for seg in segments:
            translated = GoogleTranslator(source="auto", target=target_lang).translate(
                seg.text.strip()
            )
            orig_words = seg.words  # list of Word(start, end, word)
            trans_words = split_words(translated)

            all_segments_data.append(
                {
                    "seg_start": seg.start,
                    "seg_end": seg.end,
                    "orig_words": orig_words,
                    "trans_words": trans_words,
                    "translated_text": translated,
                }
            )

        timeline = AudioSegment.silent(duration=total_ms)

        for item in all_segments_data:
            orig_words = item["orig_words"]
            trans_words = item["trans_words"]
            seg_start = item["seg_start"]
            seg_end = item["seg_end"]
            translated_text = item["translated_text"]

            start_ms_global = int(seg_start * 1000)
            end_ms_global = int(seg_end * 1000)

            # --- Fallback: если количество слов не совпадает ---
            if len(orig_words) != len(trans_words):
                # Генерируем TTS для всей фразы
                tts_file = os.path.join(tmp, f"tts_fallback_{uuid4()}.mp3")
                communicate = edge_tts.Communicate(translated_text, voice)
                await communicate.save(tts_file)

                tts_audio = AudioSegment.from_file(tts_file)
                target_dur = end_ms_global - start_ms_global
                if len(tts_audio) > target_dur:
                    tts_audio = tts_audio[:target_dur]
                elif len(tts_audio) < target_dur:
                    tts_audio = tts_audio + AudioSegment.silent(
                        duration=target_dur - len(tts_audio)
                    )
                try:
                    tts_audio = normalize(tts_audio)
                except:
                    pass

                before = timeline[:start_ms_global]
                after = timeline[end_ms_global:]
                timeline = before + tts_audio + after
                os.remove(tts_file)
                continue

            # --- По словам: 1:1 сопоставление ---
            async def tts_word(word_text):
                tts_file = os.path.join(tmp, f"tts_word_{uuid4()}.mp3")
                communicate = edge_tts.Communicate(word_text, voice)
                await communicate.save(tts_file)
                return tts_file

            # Генерируем TTS для каждого слова параллельно
            tts_word_files = await asyncio.gather(*[tts_word(w) for w in trans_words])

            for i, tts_file in enumerate(tts_word_files):
                if not os.path.exists(tts_file):
                    continue
                word = orig_words[i]
                start_ms = int(word.start * 1000)
                end_ms = int(word.end * 1000)
                target_dur = end_ms - start_ms

                if target_dur <= 0 or start_ms >= total_ms:
                    os.remove(tts_file)
                    continue

                tts_audio = AudioSegment.from_file(tts_file)
                if len(tts_audio) == 0:
                    os.remove(tts_file)
                    continue

                if len(tts_audio) > target_dur:
                    tts_audio = tts_audio[:target_dur]
                elif len(tts_audio) < target_dur:
                    tts_audio = tts_audio + AudioSegment.silent(
                        duration=target_dur - len(tts_audio)
                    )

                try:
                    tts_audio = normalize(tts_audio)
                except:
                    pass

                before = timeline[:start_ms]
                after = timeline[end_ms:]
                timeline = before + tts_audio + after

                os.remove(tts_file)

        # --- Финальная длина ---
        if len(timeline) != total_ms:
            timeline = (
                timeline[:total_ms]
                if len(timeline) > total_ms
                else timeline + AudioSegment.silent(duration=total_ms - len(timeline))
            )

        # --- Экспорт ---
        timeline.export(output_audio_path, format="wav")

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-i",
            output_audio_path,
            "-c:v",
            "copy",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:a",
            "aac",
            "-t",
            str(duration_sec),
            output_path,
        ]
        run(cmd, check=True)

        return ChatGPTSubtitle(url=output_path)

    except Exception as e:
        raise HTTPException(400, "Voice conversion failed")
    finally:
        for f in [input_path, output_audio_path]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
