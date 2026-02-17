# coding utf-8

from asyncio import run

from celery.schedules import crontab

from src.domain.entities.core import ITask

from src.infrastructure.tasks.instagram import InstagramTrackingCelery


app = InstagramTrackingCelery()


celery = app.celery

celery.conf.update(
    timezone="UTC",
    use_timezone=True,
    beat_schedule={
        "update_tracking_data": ITask(
            task="instagram.update_tracking_data",
            schedule=crontab(minute="*/5"),
        ).dict,
    },
)


@celery.task(name="instagram.update_tracking_data")
def update_tracking_data():
    return run(
        app.update_tracking_data(),
    )
