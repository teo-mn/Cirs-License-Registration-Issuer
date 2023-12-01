import logging

from web3 import Web3
from web3.types import BlockData, EventData

from blockchain.abi.product_abi import product_abi
from license_registration_issuer.settings import NODE_URL_WS, PRODUCT_ADDRESS
from blockchain.abi.key_value_abi import kv_abi
from blockchain.abi.license_abi import license_abi
from blockchain.abi.requirement_abi import requirement_abi
from syncer.models import EventLog, EventType, LicenseProduct, LatestSyncedBlock

logger = logging.getLogger(__name__)


def handle_license(event: EventData, block: BlockData):
    if EventType.from_name(event['event']) == EventType.LICENSE_REGISTERED:
        pass


def handle_event(event: EventData, block: BlockData):
    if EventLog.objects.filter(tx=event['transactionHash'].hex(),
                               log_type=EventType.from_name(event['event'])).count() > 0:
        instance = EventLog.objects.get(tx=event['transactionHash'].hex(), log_type=EventType.from_name(event['event']))
    else:
        instance = EventLog.objects.create(
            tx=event['transactionHash'].hex(),
            block_number=block['number'],
            log_type=EventType.from_name(event['event']),
            timestamp=block['timestamp'],
        )
    if instance.log_type == EventType.SET_DATA:
        instance.key = event['args']['key'].decode()
        instance.value = event['args']['value'].decode()
    elif instance.log_type == EventType.LICENSE_REGISTERED:
        instance.license_id = event['args']['licenseID'].decode()
        instance.license_name = event['args']['licenseName'].decode()
        instance.owner_id = event['args']['ownerID'].decode()
        instance.owner_name = event['args']['ownerName'].decode()
        instance.start_date = event['args']['startDate']
        instance.end_date = event['args']['endDate']
        instance.additional_data = event['args']['additionalData'].decode()
    elif instance.log_type == EventType.LICENSE_REVOKED:
        instance.license_id = event['args']['licenseID'].decode()
        instance.additional_data = event['args']['additionalData'].decode()
    elif instance.log_type == EventType.REQUIREMENT_REGISTERED:
        instance.license_id = event['args']['licenseID'].decode()
        instance.requirement_id = event['args']['requirementID'].decode()
        instance.requirement_name = event['args']['requirementName'].decode()
        instance.additional_data = event['args']['additionalData'].decode()
    elif instance.log_type == EventType.REQUIREMENT_REVOKED:
        instance.license_id = event['args']['licenseID'].decode()
        instance.requirement_id = event['args']['requirementID'].decode()
        instance.additional_data = event['args']['additionalData'].decode()
    elif instance.log_type == EventType.EVIDENCE_REGISTERED:
        instance.license_id = event['args']['licenseID'].decode()
        instance.requirement_id = event['args']['requirementID'].decode()
        instance.evidence_id = event['args']['evidenceID'].decode()
        instance.additional_data = event['args']['additionalData'].decode()
    elif instance.log_type == EventType.EVIDENCE_REVOKED:
        instance.license_id = event['args']['licenseID'].decode()
        instance.requirement_id = event['args']['requirementID'].decode()
        instance.evidence_id = event['args']['evidenceID'].decode()
        instance.additional_data = event['args']['additionalData'].decode()
    instance.save()


def handle_register_product_event(event):
    logger.info('New Product found with name: ' + str(event['args']['name'].decode()))
    if LicenseProduct.objects.filter(license_address=event['args']['license_address']).count() == 0:
        LicenseProduct.objects.create(
            license_address=event['args']['license_address'],
            requirement_address=event['args']['requirement_address'],
            kv_address=event['args']['kv_address'],
            name=event['args']['name'].decode(),
        )
    else:
        instance = LicenseProduct.objects.get(license_address=event['args']['license_address'])
        instance.requirement_address = event['args']['requirement_address']
        instance.kv_address = event['args']['kv_address']
        instance.name = event['args']['name'].decode()
        instance.save()


class BlockSyncer:
    web3 = None

    def __init__(self):
        self.web3 = Web3(Web3.WebsocketProvider(NODE_URL_WS))
        self.current_block = self.web3.eth.get_block(1)
        self.products = LicenseProduct.objects.all()

    def connect_web3(self):
        if not self.web3.is_connected():
            self.web3 = Web3(Web3.WebsocketProvider(NODE_URL_WS))

    def get_last_synced_block(self):
        if LatestSyncedBlock.objects.count() == 0:
            return LatestSyncedBlock.objects.create(last_synced_block_number=0).last_synced_block_number
        return LatestSyncedBlock.objects.first().last_synced_block_number

    def set_last_synced_block(self, block: int):
        instance, _ = LatestSyncedBlock.objects.get_or_create()
        instance.last_synced_block_number = block
        instance.save()

    def get_latest_block(self):
        return self.web3.eth.get_block_number()

    def handle_event(self, event: EventData):
        logger.debug('Syncer found new event: ')
        logger.debug(event)
        print(event)
        print(self.current_block)
        # handle_event(event, self.current_block)

    def sync_products(self, from_block, to_block):
        logger.debug('Syncing product contract from: ' + str(from_block) + ' to: ' + str(to_block))
        prod_contract = self.web3.eth.contract(address=PRODUCT_ADDRESS, abi=product_abi)
        event_filter = prod_contract.events.Register.create_filter(fromBlock=from_block, toBlock=to_block)
        for event in event_filter.get_all_entries():
            handle_register_product_event(event)
        self.products = LicenseProduct.objects.all()

    def sync_licenses(self, from_block, to_block):
        logger.debug('Syncing license contract from: ' + str(from_block) + ' to: ' + str(to_block))
        for product in self.products:
            license_contract = self.web3.eth.contract(address=product.license_address, abi=license_abi)
            self.sync_events(from_block, to_block, self.handle_event,
                             [license_contract.events.LicenseRegistered, license_contract.events.LicenseRevoked])

    def sync_requirements(self, from_block, to_block):
        logger.debug('Syncing requirement contract from: ' + str(from_block) + ' to: ' + str(to_block))
        for product in self.products:
            requirement_contract = self.web3.eth.contract(address=product.requirement_address, abi=requirement_abi)
            self.sync_events(from_block, to_block, self.handle_event,
                             [requirement_contract.events.LicenseRequirementRegistered,
                              requirement_contract.events.LicenseRequirementRevoked,
                              requirement_contract.events.EvidenceRegistered,
                              requirement_contract.events.EvidenceRevoked])

    def sync_kv(self, from_block, to_block):
        logger.debug('Syncing kv contract from: ' + str(from_block) + ' to: ' + str(to_block))
        for product in self.products:
            kv_contract = self.web3.eth.contract(address=product.kv_address, abi=kv_abi)
            self.sync_events(from_block, to_block, self.handle_event, [kv_contract.events.SetData])

    def sync_events(self, from_block, to_block, handler, event_functions):
        for event_function in event_functions:
            event_filter = event_function.create_filter(
                fromBlock=self.web3.to_hex(from_block),
                toBlock=self.web3.to_hex(to_block)
            )
            for event in event_filter.get_all_entries():
                handler(event)

    def sync_new_block_range(self, from_block, to_block):
        logger.info('Syncing block from: ' + str(from_block) + ', to: ' + str(to_block))

        self.sync_products(from_block, to_block)
        self.sync_licenses(from_block, to_block)
        self.sync_requirements(from_block, to_block)
        self.sync_kv(from_block, to_block)

    def syn_new_blocks(self):
        self.connect_web3()
        from_block = self.get_last_synced_block() + 1
        to_block = self.get_latest_block()
        logger.info('Syncer starting from block: ' + str(to_block))
        while from_block <= to_block:
            x = min(from_block + 1000, to_block)
            self.sync_new_block_range(from_block, x)
            from_block = x + 1
            self.set_last_synced_block(x)
        self.set_last_synced_block(to_block)
        logger.info('Syncer ends in block: ' + str(to_block))
