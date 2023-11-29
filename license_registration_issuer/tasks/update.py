import logging

from celery import shared_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE
from license_registration_issuer.tasks.register import RegisterHandler


class UpdateHandler(RegisterHandler):
    def handle(self):
        self.issue_license()
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def update_task(id: str):
    logging.info('Update license task: ' + str(id))
    try:
        handler = UpdateHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
    return
