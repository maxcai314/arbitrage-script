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
import time

contract_address = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a" # checksum address: case sensitive
filename = f"{contract_address}.json"
path = os.path.join(".", "abi", filename)

with open(path, "r") as file:
    abi = json.load(file)

contract = w3.eth.contract(address=contract_address, abi=abi)

# for function_name in contract.functions:
    # print(function_name)

quoter = contract.functions.quoteExactInputSingle
params = (
    Web3.to_checksum_address("0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca"), # tokenIn
    Web3.to_checksum_address("0x0000000000000000000000000000000000000000"), # tokenOut
    100, # amountIn
    500, # fee
    0, # sqrtPriceLimitX96
)

result = quoter(params).call()
print(result)