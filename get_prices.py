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

token_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    }
]

usdbc_address = Web3.to_checksum_address("0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca")
usdbc_contract = w3.eth.contract(address=usdbc_address, abi=token_abi)
usdbc_decimals = usdbc_contract.functions.decimals().call()
print(f"usdbc uses {usdbc_decimals} decimals")

weth_address = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")
weth_contract = w3.eth.contract(address=weth_address, abi=token_abi)
weth_decimals = weth_contract.functions.decimals().call()
print(f"weth uses {weth_decimals} decimals")

input_amount = 1.0 # eth
input_value = int(input_amount * 10 ** weth_decimals) # convert to smallest decimal unit

quoter = contract.functions.quoteExactInputSingle
params = (
    weth_address, # tokenIn
    usdbc_address, # tokenOut
    input_value, # amountIn
    500, # fee
    0, # sqrtPriceLimitX96 (0 for unused)
)

print(f"Finding the value of {input_amount} eth in usdbc on uniswap")

result = quoter(params).call()
print(f"""
Amount out: {result[0] / 10 ** usdbc_decimals} usdbc
Sqrt 96 price after: {result[1]}
Initialized ticks crossed: {result[2]}
Gas estimate: {result[3]}
""")