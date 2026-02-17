# coding utf-8

from asyncio import run

from celery.schedules import crontab

from src.domain.entities.core import ITask

from src.infrastructure.tasks.instagram import InstagramSessionCelery


app = InstagramSessionCelery()


celery = app.celery

celery.conf.update(
    timezone="UTC",
    use_timezone=True,
    beat_schedule={
        "update_sessions_data": ITask(
            task="instagram.update_sessions_data",
            schedule=crontab(minute=0, hour="*/12"),
        ).dict,
    },
)


@celery.task(name="instagram.update_sessions_data")
def update_sessions_data():
    return run(
        app.update_sessions_data(),
    )
