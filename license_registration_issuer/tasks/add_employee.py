import logging

from celery import shared_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE
from license_registration_issuer.tasks.register import RegisterHandler


class AddEmployeeHandler(RegisterHandler):
    def handle(self):
        self.issue_employee(self.data, self.data['license_id'], self.data['requirement_id'])
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def add_employee_task(id: str):
    logging.info('Add employee task: ' + str(id))
    try:
        handler = AddEmployeeHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
    return
