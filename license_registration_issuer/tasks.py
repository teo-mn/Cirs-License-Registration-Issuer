import logging

from celery import shared_task, current_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE

logger = logging.getLogger(__name__)


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def register(id: str):
    logger.info(current_task.request)
    logger.info('Register task: ' + str(id))
