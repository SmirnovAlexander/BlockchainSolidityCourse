import os
from dotenv import load_dotenv
from pprint import pprint

from web3 import Web3

load_dotenv()


# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545/"))
# chain_id = 1337
# my_address = "0xefba761bB041681e1D92Dd4898d0Ad835a9A4A93"
# receiver_address = "0xa243694a07E0a88b4ac9B24700CcfE33e74fC07B"

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/1320d37ae90b47dc908b06b081211f8b"))
chain_id = 4
my_address = "0xFddcDEe0116A17071FD57563d3F73727c80F9659"
receiver_address = "0x3e2F73d8Ea969607A2aE32ea406135f9B3e0Cc88"

private_key = os.getenv("PRIVATE_KEY")

print("Forming the transcation...")
transaction = {
    "from": my_address,
    "to": receiver_address,
    "value": w3.toWei(0.001, "ether"),
    "gasPrice": w3.eth.gas_price,
    "gas": 21000,
    "nonce": w3.eth.get_transaction_count(my_address)
}
print("--------------------------------------------------------")
pprint(transaction)
print("--------------------------------------------------------")

print("Signing transcation...")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = private_key)

print("Sending signed transcation...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Done! Transaction hash: {tx_receipt.transactionHash.hex()}")
