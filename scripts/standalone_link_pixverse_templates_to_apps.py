# -*- coding: utf-8 -*-
"""
Самостоятельный скрипт: привязка шаблонов к приложениям PixVerse
через таблицу pixverse_application_templates.

Не зависит от кода репозитория — только SQLAlchemy + PyMySQL.

Важно: в связке template_id = pixverse_templates.id (PK строки в БД),
       а НЕ поле pixverse_templates.template_id (ID на платформе PixVerse),
       если только не включён режим resolve по platform id ниже.

Запуск:
  pip install sqlalchemy pymysql
  python scripts/standalone_link_pixverse_templates_to_apps.py
"""

from __future__ import annotations

from sqlalchemy import (
    Integer,
    MetaData,
    Table,
    Column,
    create_engine,
    select,
    insert,
    and_,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

# ---------------------------------------------------------------------------
# НАСТРОЙКИ
# ---------------------------------------------------------------------------

DATABASE_URL = "mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE"

# ID приложений в pixverse_applications.id (у вас 1 … 45)
APPLICATION_IDS: list[int] = list(range(1, 46))

# Режим: как интерпретировать TEMPLATE_IDS
# - "pk"       — значения = pixverse_templates.id (рекомендуется)
# - "platform" — значения = pixverse_templates.template_id (ID эффекта PixVerse), скрипт сам найдёт id строк
TEMPLATE_ID_MODE: str = "pk"

# Список ID шаблонов (смысл зависит от TEMPLATE_ID_MODE)
TEMPLATE_IDS: list[int] = [
    1,
    2,
    3,
]

# Если в режиме "platform" один platform id даёт несколько строк в БД — брать все или только первую
ON_PLATFORM_COLLISION: str = "all"  # "all" | "first"

DRY_RUN = False

# ---------------------------------------------------------------------------

metadata = MetaData()

pixverse_application_templates = Table(
    "pixverse_application_templates",
    metadata,
    Column("application_id", Integer, primary_key=True),
    Column("template_id", Integer, primary_key=True),
)

pixverse_templates = Table(
    "pixverse_templates",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("template_id", Integer),
)


def resolve_template_row_ids(engine: Engine, mode: str, raw_ids: list[int]) -> list[int]:
    if mode == "pk":
        return list(dict.fromkeys(raw_ids))

    if mode != "platform":
        raise ValueError(f"Неизвестный TEMPLATE_ID_MODE: {mode!r}, ожидается 'pk' или 'platform'")

    if not raw_ids:
        return []

    with Session(engine) as session:
        out: list[int] = []
        for platform_tid in raw_ids:
            rows = session.execute(
                select(pixverse_templates.c.id).where(
                    pixverse_templates.c.template_id == platform_tid
                )
            ).all()
            pks = [int(r[0]) for r in rows]
            if not pks:
                raise RuntimeError(
                    f"Нет строки в pixverse_templates с template_id={platform_tid}"
                )
            if ON_PLATFORM_COLLISION == "first":
                out.append(pks[0])
            elif ON_PLATFORM_COLLISION == "all":
                out.extend(pks)
            else:
                raise ValueError("ON_PLATFORM_COLLISION должен быть 'all' или 'first'")

        return list(dict.fromkeys(out))


def verify_template_pks_exist(engine: Engine, pks: list[int]) -> None:
    if not pks:
        return
    with Session(engine) as session:
        found = session.execute(
            select(pixverse_templates.c.id).where(
                pixverse_templates.c.id.in_(pks)
            )
        ).all()
        found_set = {int(r[0]) for r in found}
    missing = [i for i in pks if i not in found_set]
    if missing:
        raise RuntimeError(
            "В pixverse_templates нет id (PK): "
            + ", ".join(str(x) for x in missing)
        )


def main() -> int:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)

    template_row_ids = resolve_template_row_ids(
        engine, TEMPLATE_ID_MODE, TEMPLATE_IDS
    )
    verify_template_pks_exist(engine, template_row_ids)

    pairs_to_add: list[tuple[int, int]] = []
    for app_id in APPLICATION_IDS:
        for tmpl_row_id in template_row_ids:
            pairs_to_add.append((app_id, tmpl_row_id))

    inserted = 0
    skipped = 0

    with SessionLocal() as session:
        for application_id, template_row_id in pairs_to_add:
            exists = session.execute(
                select(1).where(
                    and_(
                        pixverse_application_templates.c.application_id
                        == application_id,
                        pixverse_application_templates.c.template_id
                        == template_row_id,
                    )
                )
            ).first()
            if exists:
                skipped += 1
                continue
            if DRY_RUN:
                print(
                    f"[DRY_RUN] INSERT application_id={application_id} "
                    f"template_id={template_row_id}"
                )
                inserted += 1
                continue
            session.execute(
                insert(pixverse_application_templates).values(
                    application_id=application_id,
                    template_id=template_row_id,
                )
            )
            inserted += 1
        if not DRY_RUN:
            session.commit()

    print(f"Режим шаблонов: {TEMPLATE_ID_MODE!r}, строк pixverse_templates.id: {template_row_ids}")
    print(f"Приложений: {len(APPLICATION_IDS)} (ids {min(APPLICATION_IDS)}…{max(APPLICATION_IDS)})")
    print(f"Добавлено связей: {inserted}")
    print(f"Уже было (пропущено): {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
