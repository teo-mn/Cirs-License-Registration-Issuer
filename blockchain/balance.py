from license_registration_issuer.settings import NODE_URL


def get_balance(address: str):
    from web3 import Web3
    web3 = Web3(Web3.HTTPProvider(NODE_URL))
    return float(web3.from_wei(web3.eth.get_balance(web3.to_checksum_address(address)), 'ether'))
