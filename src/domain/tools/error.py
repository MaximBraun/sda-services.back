# coding utf-8

from fastapi import Request, HTTPException

from fastapi.datastructures import QueryParams


async def format_error_with_request(
    *,
    exc: HTTPException,
    status_code: int,
    request: Request,
    title: str,
    project: str,
) -> str:
    url: str = request.url.path
    params: QueryParams = request.query_params
    query = f"{url}?{params}" if params else url

    message = (
        f"⚠️ <b>Статус:</b> <code>{status_code}</code> — {title}"
        f"\n\n🛠 <b>Проект:</b> <code>{project.capitalize()}</code>"
        f"\n\n🔗 <b>Запрос:</b> <code>{request.method} {query}</code>"
    )
    custom_context = []

    if hasattr(exc, "extra") and isinstance(exc.extra, dict):
        for key, value in exc.extra.items():
            custom_context.append(f"<code>{key}:</code> <pre>{value}</pre>")

    if custom_context:
        message += "\n\n🧾 <b>Подробности:</b>\n" + "\n".join(custom_context)

    return message
