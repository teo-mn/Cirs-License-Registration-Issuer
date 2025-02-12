import json
import logging
from urllib.response import addinfo

import requests
from celery import shared_task

from blockchain.issuer import Issuer
from license_registration_issuer.models import Request
from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, NODE_URL, \
    LICENSE_REGISTRATION_ADDRESS, REQUIREMENT_REGISTRATION_ADDRESS, KV_ADDRESS, ISSUER_ADDRESS, ISSUER_PK, \
    CALLBACK_USERNAME, CALLBACK_PASSWORD, CALLBACK_COMMAND, LICENSE_FRONTEND_URL
from license_registration_issuer.tasks.utils import employee_data_convert


class RegisterHandler:
    has_error = False
    error_msg = ''
    qr_url = ''

    def __init__(self, request_id: str):
        self.issuer = Issuer(node_url=NODE_URL,
                             license_contract=LICENSE_REGISTRATION_ADDRESS,
                             requirement_contract=REQUIREMENT_REGISTRATION_ADDRESS,
                             kv_contract=KV_ADDRESS
                             )
        try:
            self.instance = Request.objects.get(id=request_id)
            self.data = json.loads(self.instance.data)
        except Request.DoesNotExist:
            raise Exception('Instance not found with id=(' + request_id + ')')
        except Exception as e:
            raise e

    def issue_license(self):
        data = self.data
        if data['state'] == 0:
            logging.info('[license] Issuing id: ' + data['license_id'])
            add_data = {'d': data['license_system_id'] if 'description' not in data else data['description'],
                        'is_c': 1 if data['is_consulting'] == "1" else 0}
            tx, error = self.issuer.register_license(
                data['license_id'],
                data['license_type'],
                data['owner_id'],
                data['owner_name'],
                data['start_date'],
                data['end_date'],
                json.dumps(add_data),
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                self.has_error = True
                self.error_msg = error
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                return
            logging.info('[license] Issued on blockchain with tx: ' + str(tx))
            data['state'] = 1
            self.instance.data = json.dumps(data)
            self.instance.save()
        else:
            logging.info('[license] Skipping id: ' + data['license_id'])

    def issue_requirement(self, req: dict):
        data = self.data
        if req['state'] == 0:
            logging.info('[requirement] Issuing id: ' + req['requirement_id'])
            tx, error = self.issuer.register_requirement(
                data['license_id'],
                req['requirement_id'],
                req['requirement_id'],
                req['requirement_system_id'],
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                self.has_error = True
                self.error_msg = error
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                return
            logging.info('[requirement] Issued on blockchain with tx: ' + str(tx))
            req['state'] = 1
            self.instance.data = json.dumps(data)
            self.instance.save()
        else:
            logging.info('[requirement] Skipping id: ' + req['requirement_id'])

    def handle_callback(self):
        if self.instance.callback_url != '':
            x = {
                'request_id': str(self.instance.id),
                'payload': self.data,
                'has_error': self.has_error,
                'error_msg': str(self.error_msg),
                'qr_url': self.qr_url
            }
            y = {
                'username': CALLBACK_USERNAME,
                'password': CALLBACK_PASSWORD,
                'command': CALLBACK_COMMAND,
                'parameters': x,
            }
            headers = {"Content-Type": "application/json"}
            requests.post(self.instance.callback_url, headers=headers, data=json.dumps(y))
        return

    def issue_employee(self, employee: dict, license_id: str, requirement_id: str):
        secret_hash, info = employee_data_convert(employee)
        if employee['state'] == 0:
            logging.info('[evidence] Issuing id: ' + secret_hash)
            tx, error = self.issuer.set_data(secret_hash, info, ISSUER_ADDRESS, ISSUER_PK)
            if error != '' and error is not None:
                self.has_error = True
                self.error_msg = error
                logging.error('Error occurred: ' + str(id))
                logging.error(error)
                return False
            logging.info('[kv] Issued on blockchain with tx: ' + str(tx))
            tx, error = self.issuer.set_evidence(
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
                self.error_msg = error
                self.has_error = True
                return False
            logging.info('[evidence] Issued on blockchain with tx: ' + str(tx))
            employee['state'] = 1
            self.instance.data = json.dumps(self.data)
            self.instance.save()
        else:
            logging.info('[evidence] Skipping id: ' + secret_hash)
        return True

    def handle(self):
        self.issue_license()
        for req in self.data['requirements']:
            self.issue_requirement(req)
            for emp in req['employees']:
                self.issue_employee(emp, self.data['license_id'], req['requirement_id'])
        self.qr_url = LICENSE_FRONTEND_URL + '/' + LICENSE_REGISTRATION_ADDRESS + '/' + self.data['license_id']
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def register_task(id: str):
    logging.info('Register license task: ' + str(id))
    try:
        handler = RegisterHandler(id)
        handler.handle()
    except Exception as e:
        logging.error('Error occurred: ' + str(id))
        logging.error(e)
