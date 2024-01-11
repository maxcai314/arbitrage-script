from web3 import Web3
import os
import json
import time

from exchange_graph import ExchangeGraph, Token, Exchange

# Connect to base.org eth protocol
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))

token_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "","type": "string"}],
        "type": "function"
    },
    {
        'inputs': [],
        'name': 'totalSupply',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function', 'constant': True
    },
    {
        'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}],
        'name': 'balanceOf',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function', 'constant': True
    },
]

def tokenFor(address: str) -> Token:
    formatted_address = Web3.to_checksum_address(address)
    contract = w3.eth.contract(address=formatted_address, abi=token_abi)
    decimals = contract.functions.decimals().call()
    name = contract.functions.name().call()
    return Token(name, formatted_address, decimals)

# Get the latest block number
# latest = w3.eth.block_number
# print("Latest block number:", latest)

# Get the latest block
# block = w3.eth.get_block(latest)
# print("Latest block:", block)

contract_address = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a" # checksum address: case sensitive
filename = f"{contract_address}.json"
path = os.path.join(".", "abi", filename)

with open(path, "r") as file:
    abi = json.load(file)

contract = w3.eth.contract(address=contract_address, abi=abi)

# for function_name in contract.functions:
    # print(function_name)

usdbc = tokenFor("0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca")

weth = tokenFor("0x4200000000000000000000000000000000000006")

input_value = 1 # eth
input_int = weth.value2int(input_value) # convert to smallest decimal unit

quoter = contract.functions.quoteExactInputSingle
params = (
    weth.address, # tokenIn
    usdbc.address, # tokenOut
    input_int, # amountIn
    500, # fee tier (500, 3000, 10000)
    0, # sqrtPriceLimitX96 (0 for unused)
)

print(f"Finding the value of {input_value} eth in usdbc on uniswap")

result = quoter(params).call()
print(f"""
Amount out: {usdbc.int2value(result[0])} usdbc
Sqrt 96 price after: {result[1]}
Initialized ticks crossed: {result[2]}
Gas estimate: {result[3]}
""")