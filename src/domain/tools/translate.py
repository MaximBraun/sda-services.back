# coding utf-8

from typing import Any

import whisper

from openai import OpenAI

from deep_translator import GoogleTranslator

from ..conf import app_conf

from ..constants import SEPARATOR


config = app_conf()


client = OpenAI(api_key=config.chatgpt_token)


async def gpt_translate_auto(text: str, target_lang: str) -> str:
    if not text.strip():
        return text

    prompt = f"""
Translate the following text to {target_lang}.
Detect the source language automatically.
Return ONLY the translated text.

Text:
{text}
"""

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=300,
    )

    return resp.output_text.strip()


async def translate_batch(
    segments: list[dict[str, Any]], target_lang: str
) -> list[dict[str, Any]]:
    combined_text = SEPARATOR.join(seg["text"] for seg in segments)

    translated_combined = await gpt_translate_auto(combined_text, target_lang)

    translated_texts = translated_combined.split(SEPARATOR)

    translated_texts = [t.strip() for t in translated_texts[: len(segments)]]

    return [
        {"start": seg["start"], "end": seg["end"], "text": translated_texts[i]}
        for i, seg in enumerate(segments)
    ]


async def transcribe_audio(
    filepath: str,
) -> str | list:
    model = whisper.load_model("base")

    result = model.transcribe(
        filepath,
        verbose=False,
    )
    return result["segments"]
