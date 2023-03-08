from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider(os.environ.get('WEB3_PROVIDER')))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address: {address}\nYour key: {privateKey}")