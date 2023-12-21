import json
import logging

from celery import shared_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, \
    ISSUER_ADDRESS, ISSUER_PK
from license_registration_issuer.tasks.register import RegisterHandler
from license_registration_issuer.tasks.utils import employee_data_convert


class RemoveEmployeeHandler(RegisterHandler):
    def remove_employee(self, employee: dict, license_id: str, requirement_id: str):
        secret_hash, info = employee_data_convert(employee)
        if employee['state'] == 0:
            logging.info('[evidence] Revoking id: ' + secret_hash)
            tx, error = self.issuer.revoke_evidence(
                license_id,
                requirement_id,
                secret_hash,
                '' if 'description' not in employee else employee['description'],
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                logging.has_error = True
                self.error_msg = error
                return False
            logging.info('[evidence] Revoked on blockchain with tx: ' + str(tx))
            employee['state'] = 1
            self.instance.data = json.dumps(self.data)
            self.instance.save()
            return True
        else:
            logging.info('[evidence] Skipping id: ' + secret_hash)

    def handle(self):
        self.remove_employee(self.data, self.data['license_id'], self.data['requirement_id'])
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def remove_employee_task(id: str):
    logging.info('Remove employee task: ' + str(id))
    try:
        handler = RemoveEmployeeHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
    return
