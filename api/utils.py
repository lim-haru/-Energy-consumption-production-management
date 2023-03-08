from web3 import Web3
import os

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider(os.environ.get('WEB3_PROVIDER')))
    address = os.environ.get('ADDRESS')
    privateKey = os.environ.get('PRIVATE_KEY')

    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)
    
    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId