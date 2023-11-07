import logging
import json
from celery import shared_task
from verify4py.json_utils import json_wrap
from verify4py.utils import calc_hash_str

from blockchain.issuer import Issuer
from license_registration_issuer.settings import CELERY_TASK_DEFAULT_QUEUE, CELERY_TASK_DEFAULT_EXCHANGE, \
    NODE_URL, LICENSE_REGISTRATION_ADDRESS, REQUIREMENT_REGISTRATION_ADDRESS, KV_ADDRESS, ISSUER_PK, ISSUER_ADDRESS
from license_registration_issuer.models import Request

logger = logging.getLogger(__name__)


def issue_employee(issuer: Issuer, instance: Request, data: dict, req, employee: dict):
    regnum_hash = calc_hash_str(json_wrap({"regnum": employee["regnum"]}))
    employee_hash = json_wrap({"regnum": employee["regnum"],
                               "last_name": employee["last_name"],
                               "first_name": employee["first_name"],
                               "profession": employee["profession"],
                               "degree": employee["degree"]
                               })

    tx, error = issuer.set_data(regnum_hash, employee_hash, ISSUER_ADDRESS, ISSUER_PK)
    if error != '' and error is not None:
        logger.error('Error occurred: ' + str(id))
        logger.error(error)
        return
    else:
        logger.info('[kv] Issued on blockchain with tx: ' + str(tx))
    tx, error = issuer.set_evidence(
        data['license_id'],
        req['requirement_id'],
        regnum_hash,
        ISSUER_ADDRESS,
        ISSUER_PK
    )
    if error != '' and error is not None:
        logger.error('Error occurred: ' + str(id))
        logger.error(error)
        return
    else:
        logger.info('[evidence] Issued on blockchain with tx: ' + str(tx))
    employee['state'] = 1
    instance.data = json.dumps(data)
    instance.save()


@shared_task(queue=CELERY_TASK_DEFAULT_QUEUE, exchange=CELERY_TASK_DEFAULT_EXCHANGE)
def register_task(id: str):
    logger.info('Register task: ' + str(id))
    try:
        instance = Request.objects.get(id=id)
        data = json.loads(instance.data)
        issuer = Issuer(node_url=NODE_URL,
                        license_contract=LICENSE_REGISTRATION_ADDRESS,
                        requirement_contract=REQUIREMENT_REGISTRATION_ADDRESS,
                        kv_contract=KV_ADDRESS
                        )
        if data['state'] == 0:
            logger.info('[license] Issuing id: ' + data['license_id'])
            tx, error = issuer.register_license(
                data['license_id'],
                data['license_system_id'],
                data['owner_id'],
                data['owner_name'],
                data['start_date'],
                data['end_date'],
                '',
                ISSUER_ADDRESS,
                ISSUER_PK
            )
            if error != '' and error is not None:
                # db save
                logger.error('Error occurred: ' + str(id))
                logger.error(error)
                return
            logger.info('[license] Issued on blockchain with tx: ' + str(tx))
            data['state'] = 1
            instance.data = json.dumps(data)
            instance.save()
        else:
            logger.info('[license] Skipping id: ' + data['license_id'])
        for req in data['requirements']:
            if req['state'] == 0:
                logger.info('[requirement] Issuing id: ' + req['requirement_id'])
                tx, error = issuer.register_requirement(
                    data['license_id'],
                    req['requirement_id'],
                    req['requirement_system_id'],
                    '',
                    ISSUER_ADDRESS,
                    ISSUER_PK
                )
                if error != '' and error is not None:
                    logger.error('Error occurred: ' + str(id))
                    logger.error(error)
                else:
                    logger.info('[requirement] Issued on blockchain with tx: ' + str(tx))
                    data['state'] = 1
                    instance.data = json.dumps(data)
                    instance.save()

                req['state'] = 1
                instance.data = json.dumps(data)
                instance.save()
            else:
                logger.info('[requirement] Skipping id: ' + req['requirement_id'])

            for emp in req['employees']:
                if emp['state'] == 0:
                    logger.info('[employee] Issuing regnum: ' + emp['regnum'])
                    issue_employee(issuer, instance, data, req, emp)
                else:
                    logger.info('[employee] Skipping regnum: ' + emp['regnum'])

        # callback
    except Request.DoesNotExist:
        logger.error('Instance not found with id=(' + id + ')')
    except Exception as e:
        logger.error('Error occurred: ' + str(id))
        logger.error(e)
