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

quoter = contract.functions.quoteExactInputSingle

def exchangeRateOf(token_from: Token, token_to: Token, amount_in: float = 0.1) -> float:
    params = (
        token_from.address, # tokenIn
        token_to.address, # tokenOut
        token_from.value2int(amount_in), # amountIn
        3000, # fee tier (500, 3000, 10000)
        0, # sqrtPriceLimitX96 (0 for unused)
    )

    result = quoter(params).call()
    amount_out = token_to.int2value(result[0])
    return amount_out / amount_in


weth = tokenFor("0x4200000000000000000000000000000000000006")
usdbc = tokenFor("0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca")

tokens = {
    weth: 0.004, # roughly 10 dollars
    usdbc: 10., # roughly 10 dollars
    tokenFor("0x50c5725949a6f0c72e6c4a641f24049a917db0cb"): 10., # DAI
}

assert weth in tokens # pedantic, we need weth as a starting node

graph = ExchangeGraph()
for start_token in tokens:
    graph.add_token(start_token)
    for end_token in tokens:
        if start_token == end_token:
            continue
        graph.add_token(end_token)
        exchange_rate = exchangeRateOf(start_token, end_token, amount_in=tokens[start_token])
        graph.add_exchange(Exchange("Uniswap", start_token, end_token, exchange_rate))

print(graph)