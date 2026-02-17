# coding utf-8

from asyncio import run

from celery.schedules import crontab

from src.domain.entities.core import ITask

from src.infrastructure.tasks.pixverse import PixverseStyleCelery


app = PixverseStyleCelery()


celery = app.celery

celery.conf.update(
    timezone="UTC",
    use_timezone=True,
    beat_schedule={
        "clean_files": ITask(
            task="pixverse.clean_style_files",
            schedule=crontab(minute=0, hour="*/24"),
        ).dict,
    },
)


@celery.task(name="pixverse.clean_style_files")
def clean_style_files():
    return run(
        app.clean_files(),
    )
