import json
import logging

from celery import shared_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, \
    ISSUER_ADDRESS, ISSUER_PK
from license_registration_issuer.tasks.register import RegisterHandler


class RemoveRequirementHandler(RegisterHandler):
    def revoke_requirement(self, license_id, requirement_id, description):
        if self.data['state'] == 0:
            logging.info('[requirement] Revoking id: ' + requirement_id)
            tx, error = self.issuer.revoke_requirement(
                license_id,
                requirement_id,
                description,
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                logging.has_error = True
                return False
            else:
                logging.info('[requirement] Revoked on blockchain with tx: ' + str(tx))
            self.data['state'] = 1
            self.instance.data = json.dumps(self.data)
            self.instance.save()
            return True
        else:
            logging.info('[requirement] Skipping id: ' + requirement_id)

    def handle(self):
        self.revoke_requirement(self.data['license_id'], self.data['requirement_id'], self.data['description'])
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def remove_requirement_task(id: str):
    logging.info('Remove requirement task: ' + str(id))
    try:
        handler = RemoveRequirementHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
