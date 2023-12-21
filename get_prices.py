from web3 import Web3

# Connect to base.org eth protocol
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))

# demo code? idk
print(
    w3.eth.get_block("latest")
)
