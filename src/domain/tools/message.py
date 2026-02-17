# coding utf-8


def format_message(
    title: str,
    fields: dict[str, str],
) -> str:
    lines = [f"🎉 <b>{title}</b>"]
    for label, value in fields.items():
        if value:  # пропускаем пустые значения
            lines.append(f"{label} <code>{value}</code>")
    return "\n\n".join(lines)
