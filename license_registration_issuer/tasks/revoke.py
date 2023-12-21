import json
import logging

from celery import shared_task

from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, \
    ISSUER_ADDRESS, ISSUER_PK
from license_registration_issuer.tasks.register import RegisterHandler


class RevokeHandler(RegisterHandler):
    def revoke(self, license_id, description):
        if self.data['state'] == 0:
            logging.info('[license] Revoking id: ' + license_id)
            tx, error = self.issuer.revoke_license(
                license_id,
                description,
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                logging.has_error = True
                self.error_msg = error
                return False
            logging.info('[license] Revoked on blockchain with tx: ' + str(tx))
            self.data['state'] = 1
            self.instance.data = json.dumps(self.data)
            self.instance.save()
            return True
        else:
            logging.info('[license] Skipping id: ' + license_id)

    def handle(self):
        self.revoke(self.data['license_id'], self.data['description'])
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def revoke_task(id: str):
    logging.info('Remove license task: ' + str(id))
    try:
        handler = RevokeHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
