#origen: https://www.youtube.com/watch?v=f35EoGYL7A4&t=760s&ab_channel=QuitoLambda

from celery import Celery

celery = Celery('celery_app')

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    worker_concurrency=15,
    imports=(
        "tasks",
    )
)
