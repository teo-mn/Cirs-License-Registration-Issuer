import logging

from celery import shared_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE
from license_registration_issuer.tasks.register import RegisterHandler


class AddRequirementHandler(RegisterHandler):
    def handle(self):
        for req in self.data['requirements']:
            self.issue_requirement(req)
            for emp in req['employees']:
                self.issue_employee(emp, self.data['license_id'], req['requirement_id'])
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def add_requirement_task(id: str):
    logging.info('Add requirement task: ' + str(id))
    try:
        handler = AddRequirementHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
    return
