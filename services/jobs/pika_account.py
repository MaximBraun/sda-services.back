# coding utf-8

from asyncio import run

from celery.schedules import crontab

from src.domain.entities.core import ITask

from src.infrastructure.tasks.pika import PikaAccountCelery


app = PikaAccountCelery()


celery = app.celery

celery.conf.update(
    timezone="UTC",
    use_timezone=True,
    beat_schedule={
        "update_account_balance": ITask(
            task="pika.update_account_balance",
            schedule=crontab(minute=0, hour="*/3"),
        ).dict,
    },
)


@celery.task(name="pika.update_account_balance")
def update_account_balance():
    return run(
        app.update_accounts(),
    )
