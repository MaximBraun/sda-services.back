# coding utf-8

from asyncio import run

from celery.schedules import crontab

from src.domain.entities.core import ITask

from src.infrastructure.tasks.pixverse import PixverseAccountCelery


app = PixverseAccountCelery()


celery = app.celery

celery.conf.update(
    timezone="UTC",
    use_timezone=True,
    beat_schedule={
        "update_account_balance": ITask(
            task="pixverse.update_account_balance",
            schedule=crontab(minute=0, hour="*/3"),
        ).dict,
    },
)


@celery.task(name="pixverse.update_account_balance")
def update_account_balance():
    return run(
        app.update_accounts(),
    )
