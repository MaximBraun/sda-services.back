# coding utf-8

from typing import Callable


def auto_docs(
    path: str,
    method: str,
    description: str | None = None,
    params: dict[str, dict[str, str]] | None = None,
) -> Callable:
    """Декоратор для автоматического создания документации API эндпоинтов.

    Генерирует стандартизированную документацию в формате Markdown прямо в docstring,
    включая информацию о методе, пути и параметрах эндпоинта.

    Args:
        path (str): URL путь эндпоинта (например, "/api/v1/users")
        method (str): HTTP метод ("GET", "POST", "PUT", "DELETE")
        description (str | None): Описание функциональности эндпоинта
        params (dict[str, dict[str, str]] | None): Словарь параметров в формате:
            {
                "param_name": {
                    "type": "str",  # Тип параметра
                    "description": "Описание"  # Назначение параметра
                }
            }

    Returns:
        Callable: Декорированная функция с автоматически сгенерированным docstring
    """

    def decorator(func: Callable) -> Callable:
        param_docs = "\n".join(
            f"| {name} | {info['type']} | {info['description']} |"
            for name, info in (params or {}).items()
        )
        func.__doc__ = (
            f"- **{method.upper()} `{path}`**\n\n{description or ''}\n"
            f"### Parameters:\n\n"
            f"| Parameter | Type | Description |\n|-----------|------|-------------|\n{param_docs}"
        )
        return func

    return decorator
