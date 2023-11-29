import json
import logging

from celery import shared_task
from verify4py.json_utils import json_wrap
from verify4py.utils import calc_hash_str

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, \
    ISSUER_ADDRESS, ISSUER_PK
from license_registration_issuer.tasks.register import RegisterHandler


class RemoveEmployeeHandler(RegisterHandler):
    def remove_employee(self, employee: dict, license_id: str, requirement_id: str):
        if employee['state'] == 0:
            logging.info('[evidence] Revoking id: ' + employee['license_id'])
            regnum_hash = calc_hash_str(json_wrap({"regnum": employee["regnum"]}))
            tx, error = self.issuer.revoke_evidence(
                license_id,
                requirement_id,
                regnum_hash,
                '' if 'description' not in employee else employee['description'],
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                logging.has_error = True
                return False
            else:
                logging.info('[evidence] Revoked on blockchain with tx: ' + str(tx))
            employee['state'] = 1
            self.instance.data = json.dumps(self.data)
            self.instance.save()
            return True
        else:
            logging.info('[evidence] Skipping id: ' + employee['license_id'])

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
