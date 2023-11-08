import logging

from web3 import Web3

from license_registration_issuer.models import LatestSyncedBlock
from license_registration_issuer.settings import NODE_URL_WS, KV_ADDRESS, \
    REQUIREMENT_REGISTRATION_ADDRESS, LICENSE_REGISTRATION_ADDRESS
from blockchain.abi.key_value_abi import kv_abi
from blockchain.abi.license_abi import license_abi
from blockchain.abi.requirement_abi import requirement_abi
logger = logging.getLogger(__name__)


def handle_event(event: dict):
    print(event['args'])
    print(event['event'])
    print(event['transactionHash'])
    print(event['address'])
    # TODO save db


class KvSyncer:
    contract_address = KV_ADDRESS
    abi = kv_abi
    name = 'KV'

    def __init__(self):
        self.web3 = Web3(Web3.WebsocketProvider(NODE_URL_WS))
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        self.worker_stopped = True
        self.from_block_object = None

    def connect_web3(self):
        if not self.web3.is_connected():
            self.web3 = Web3(Web3.WebsocketProvider(NODE_URL_WS))
            self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def get_latest_block_object(self):
        self.from_block_object = LatestSyncedBlock.objects.filter(id=1).first()
        if self.from_block_object is None:
            self.from_block_object = LatestSyncedBlock.objects.create(id=1)
        return self.from_block_object

    def calc_sync_block_numbers(self):
        block_object = self.get_latest_block_object()
        last_block = self.web3.eth.get_block_number()
        from_block = block_object.last_synced_block_kv + 1
        return from_block, last_block

    def save_block_number(self, last_block):
        self.from_block_object.last_synced_block_kv = last_block
        self.from_block_object.save()

    def get_events(self):
        return [self.contract.events.SetData]

    def sync_new_events(self):
        self.connect_web3()
        from_block, last_block = self.calc_sync_block_numbers()
        while from_block <= last_block:
            logger.info('[' + self.name + '] ' + 'Syncer starting from block: ' + str(from_block))
            to_block = min(last_block, from_block + 1000)
            event_functions = self.get_events()
            for event_function in event_functions:
                event_filter = event_function.create_filter(
                    fromBlock=self.web3.to_hex(from_block),
                    toBlock=self.web3.to_hex(to_block)
                )
                for event in event_filter.get_all_entries():
                    handle_event(event)

            self.save_block_number(to_block)
            if to_block == last_block:
                break
            from_block = to_block + 1

        logger.info('[' + self.name + '] ' + 'Syncer ended in block: ' + str(last_block))
        self.save_block_number(last_block)


class LicenseSyncer(KvSyncer):
    contract_address = LICENSE_REGISTRATION_ADDRESS
    abi = license_abi
    name = 'License'

    def calc_sync_block_numbers(self):
        block_object = self.get_latest_block_object()
        last_block = self.web3.eth.get_block_number()
        from_block = block_object.last_synced_block_license + 1
        return from_block, last_block

    def get_events(self):
        return [self.contract.events.LicenseRegistered, self.contract.events.LicenseRevoked]

    def save_block_number(self, last_block):
        self.from_block_object.last_synced_block_license = last_block
        self.from_block_object.save()


class RequirementSyncer(KvSyncer):
    contract_address = REQUIREMENT_REGISTRATION_ADDRESS
    abi = requirement_abi
    name = 'Requirement'

    def calc_sync_block_numbers(self):
        block_object = self.get_latest_block_object()
        last_block = self.web3.eth.get_block_number()
        from_block = block_object.last_synced_block_requirement + 1
        return from_block, last_block

    def save_block_number(self, last_block):
        self.from_block_object.last_synced_block_requirement = last_block
        self.from_block_object.save()

    def get_events(self):
        return [self.contract.events.LicenseRequirementRegistered, self.contract.events.LicenseRequirementRevoked,
                self.contract.events.EvidenceRegistered, self.contract.events.EvidenceRevoked]
