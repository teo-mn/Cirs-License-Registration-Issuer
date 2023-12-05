import logging

from web3 import Web3
from web3.auto import w3

from blockchain.abi.key_value_abi import kv_abi
from blockchain.abi.license_abi import license_abi
from blockchain.abi.requirement_abi import requirement_abi
from license_registration_issuer.settings import GAS_FEE_GWEI, DEFAULT_GAS_LIMIT

logger = logging.getLogger(__name__)


def decrypt_account(passphrase: str, path: str):
    from web3.auto import w3
    with open(path) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, passphrase)
        return w3.toHex(private_key)


class Issuer:
    def __init__(self, node_url: str, license_contract, requirement_contract, kv_contract):
        self.node_url = node_url
        self.license_contract_address = w3.to_checksum_address(license_contract)
        self.requirement_contract_address = w3.to_checksum_address(requirement_contract)
        self.kv_contract_address = w3.to_checksum_address(kv_contract)
        self.__client = Web3(Web3.HTTPProvider(node_url))
        self.__license_contract = self.__client.eth.contract(address=self.license_contract_address, abi=license_abi)
        self.__requirement_contract = self.__client.eth.contract(address=self.requirement_contract_address,
                                                                 abi=requirement_abi)
        self.__kv_contract = self.__client.eth.contract(address=self.kv_contract_address, abi=kv_abi)

    def register_license(self,
                         license_id: str,
                         license_name: str,
                         owner_id: str,
                         owner_name: str,
                         start_date: int,
                         end_date: int,
                         additional_data: str,
                         issuer_address: str,
                         pk: str):
        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__license_contract.functions.register(
                license_id.encode('utf-8'),
                license_name.encode('utf-8'),
                owner_id.encode('utf-8'),
                owner_name.encode('utf-8'),
                start_date,
                end_date,
                additional_data.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)
        except Exception as e:
            return '', e

    def revoke_license(self,
                       license_id: str,
                       additional_data: str,
                       issuer_address: str,
                       pk: str):
        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__license_contract.functions.revoke(
                license_id.encode('utf-8'),
                additional_data.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)
        except Exception as e:
            return '', e

    def register_requirement(self,
                             license_id: str,
                             requirement_id: str,
                             requirement_name: str,
                             additional_data: str,
                             issuer_address: str,
                             pk: str):

        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__requirement_contract.functions.register(
                license_id.encode('utf-8'),
                requirement_id.encode('utf-8'),
                requirement_name.encode('utf-8'),
                additional_data.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)
        except Exception as e:
            return '', e

    def revoke_requirement(self,
                           license_id: str,
                           requirement_id: str,
                           additional_data: str,
                           issuer_address: str,
                           pk: str):

        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__requirement_contract.functions.revoke(
                license_id.encode('utf-8'),
                requirement_id.encode('utf-8'),
                additional_data.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)
        except Exception as e:
            return '', e

    def set_data(self, key: str, value: str, issuer_address: str, pk: str):
        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__kv_contract.functions.setData(
                key.encode('utf-8'),
                value.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)
        except Exception as e:
            return '', e

    def set_evidence(self,
                     license_id: str,
                     requirement_id: str,
                     evidence_id: str,
                     additional_data: str,
                     issuer_address: str,
                     pk: str):
        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__requirement_contract.functions.registerEvidence(
                license_id.encode('utf-8'),
                requirement_id.encode('utf-8'),
                evidence_id.encode('utf-8'),
                additional_data.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)

        except Exception as e:
            return '', e

    def revoke_evidence(self,
                        license_id: str,
                        requirement_id: str,
                        evidence_id: str,
                        description: str,
                        issuer_address: str,
                        pk: str,
                        ):
        nonce = self.__client.eth.get_transaction_count(self.__client.to_checksum_address(issuer_address))
        try:
            func = self.__requirement_contract.functions.revokeEvidence(
                license_id.encode('utf-8'),
                requirement_id.encode('utf-8'),
                evidence_id.encode('utf-8'),
                description.encode('utf-8')
            )
            return self.__tx_send(func, issuer_address, nonce, pk)

        except Exception as e:
            return '', e

    def __tx_send(self, func, issuer_address, nonce, pk):
        tx = func.build_transaction(
            {'from': issuer_address, 'gasPrice': self.__client.to_wei(GAS_FEE_GWEI, 'gwei'),
             'nonce': nonce, 'gas': DEFAULT_GAS_LIMIT})
        signed = self.__client.eth.account.sign_transaction(tx, pk)
        tx_hash = self.__client.eth.send_raw_transaction(signed.rawTransaction)
        tx_res = self.__client.eth.wait_for_transaction_receipt(tx_hash)
        if tx_res.status == 1:
            return self.__client.to_hex(tx_hash), None
        return '', 'Failed on blockchain'
