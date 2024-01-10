from web3 import Web3

# Connect to base.org eth protocol
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))

# Get the latest block number
# latest = w3.eth.block_number
# print("Latest block number:", latest)

# Get the latest block
# block = w3.eth.get_block(latest)
# print("Latest block:", block)

import os
import json

contract_address = "0x2626664c2603336E57B271c5C0b26F421741e481"
filename = f"{contract_address}.json"
path = os.path.join(".", "abi", filename)

with open(path, "r") as file:
    abi = json.load(file)

contract = w3.eth.contract(address=contract_address, abi=abi)

for function_name in contract.functions:
    print(function_name)