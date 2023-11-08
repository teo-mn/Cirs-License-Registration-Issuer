import logging
import json
from celery import shared_task
from verify4py.json_utils import json_wrap
from verify4py.utils import calc_hash_str
import requests

from blockchain.issuer import Issuer
from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, \
    NODE_URL, LICENSE_REGISTRATION_ADDRESS, REQUIREMENT_REGISTRATION_ADDRESS, KV_ADDRESS, ISSUER_PK, ISSUER_ADDRESS
from license_registration_issuer.models import Request

logger = logging.getLogger(__name__)


class RegisterHandler:
    has_error = False

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
            logger.info('[license] Issuing id: ' + data['license_id'])
            tx, error = self.issuer.register_license(
                data['license_id'],
                data['license_system_id'],
                data['owner_id'],
                data['owner_name'],
                data['start_date'],
                data['end_date'],
                '' if 'description' not in data else data['description'],
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                self.has_error = True
                logger.error('Error occurred: ' + str(id))
                logger.error(error)
                return
            logger.info('[license] Issued on blockchain with tx: ' + str(tx))
            data['state'] = 1
            self.instance.data = json.dumps(data)
            self.instance.save()
        else:
            logger.info('[license] Skipping id: ' + data['license_id'])

    def issue_requirement(self, req: dict):
        data = self.data
        if req['state'] == 0:
            logger.info('[requirement] Issuing id: ' + req['requirement_id'])
            tx, error = self.issuer.register_requirement(
                data['license_id'],
                req['requirement_id'],
                req['requirement_system_id'],
                '',
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                self.has_error = True
                logger.error('Error occurred: ' + str(id))
                logger.error(error)
            else:
                logger.info('[requirement] Issued on blockchain with tx: ' + str(tx))
                data['state'] = 1
                self.instance.data = json.dumps(data)
                self.instance.save()

            req['state'] = 1
            self.instance.data = json.dumps(data)
            self.instance.save()
        else:
            logger.info('[requirement] Skipping id: ' + req['requirement_id'])

    def handle_callback(self):
        if self.instance.callback_url != '':
            x = {
                'request_id': str(self.instance.id),
                'payload': self.data,
                'has_error': self.has_error
            }
            requests.post(self.instance.callback_url, json.dumps(x), )
            headers = {"Content-Type": "application/json"}
            requests.request("POST", self.instance.callback_url, headers=headers, data=json.dumps(x))
        return

    def issue_employee(self, employee: dict, license_id: str, requirement_id: str):
        regnum_hash = calc_hash_str(json_wrap({"regnum": employee["regnum"]}))
        employee_hash = calc_hash_str(json_wrap({"regnum": employee["regnum"],
                                                 "last_name": employee["last_name"],
                                                 "first_name": employee["first_name"],
                                                 "profession": employee["profession"],
                                                 "degree": employee["degree"]
                                                 }))
        tx, error = self.issuer.set_data(regnum_hash, employee_hash, ISSUER_ADDRESS, ISSUER_PK)
        if error != '' and error is not None:
            self.has_error = True
            logger.error('Error occurred: ' + str(id))
            logger.error(error)
            return False
        else:
            logger.info('[kv] Issued on blockchain with tx: ' + str(tx))
        tx, error = self.issuer.set_evidence(
            license_id,
            requirement_id,
            regnum_hash,
            '' if 'description' not in employee else employee['description'],
            ISSUER_ADDRESS,
            ISSUER_PK
        )
        if error != '' and error is not None:
            logger.error('Error occurred: ' + str(id))
            logger.error(error)
            self.has_error = True
            return False
        else:
            logger.info('[evidence] Issued on blockchain with tx: ' + str(tx))
        employee['state'] = 1
        self.instance.data = json.dumps(self.data)
        self.instance.save()
        return True

    def handle(self):
        self.issue_license()
        for req in self.data['requirements']:
            self.issue_requirement(req)
            for emp in req['employees']:
                self.issue_employee(emp, self.data['license_id'], req['requirement_id'])
        self.handle_callback()


class UpdateHandler(RegisterHandler):
    def handle(self):
        self.issue_license()
        self.handle_callback()


class AddEmployeeHandler(RegisterHandler):
    def handle(self):
        self.issue_employee(self.data, self.data['license_id'], self.data['requirement_id'])
        self.handle_callback()


class RemoveEmployeeHandler(RegisterHandler):
    def remove_employee(self, employee: dict, license_id: str, requirement_id: str):
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
            logger.error('Error occurred: ' + str(id))
            logger.error(error)
            self.has_error = True
            return False
        else:
            logger.info('[evidence] Issued on blockchain with tx: ' + str(tx))
        employee['state'] = 1
        self.instance.data = json.dumps(self.data)
        self.instance.save()
        return True

    def handle(self):
        self.remove_employee(self.data, self.data['license_id'], self.data['requirement_id'])
        self.handle_callback()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def register_task(id: str):
    logger.info('Register task: ' + str(id))
    try:
        handler = RegisterHandler(id)
        handler.handle()
    except Exception as e:
        logger.error('Error occurred: ' + str(id))
        logger.error(e)


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def add_employee_task(id: str):
    logger.info('Add employee task: ' + str(id))
    try:
        handler = AddEmployeeHandler(id)
        handler.handle()
    except Exception as e:
        logger.error('Error occurred: ' + str(id))
        logger.error(e)
    return


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def remove_employee_task(id: str):
    logger.info('Remove employee task: ' + str(id))
    try:
        handler = RemoveEmployeeHandler(id)
        handler.handle()
    except Exception as e:
        logger.error('Error occurred: ' + str(id))
        logger.error(e)
    return


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def update_task(id: str):
    logger.info('Remove employee task: ' + str(id))
    try:
        handler = UpdateHandler(id)
        handler.handle()
    except Exception as e:
        logger.error('Error occurred: ' + str(id))
        logger.error(e)
    return
