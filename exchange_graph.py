from graph import Graph, Node, Edge
from math import log


# An ETH token, represented by a node
class Token(Node):
    pass


SWAP_FEE = 0.005  # 0.5%


# An ETH decentralized exchange, represented by an edge
class Exchange(Edge):
    def __init__(self, name, from_token: Token, to_token: Token, rate: float):
        super().__init__(name, from_token, to_token, -log(rate) + log(1 + SWAP_FEE))
        self.from_token = from_token
        self.to_token = to_token
        self.rate = rate

    def __repr__(self):
        return f"{self.name}: {self.from_token} -> {self.to_token} ({self.rate})"


# Network of ETH tokens and decentralized exchanges
class ExchangeGraph:
    def __init__(self):
        self.graph = Graph()
        self.tokens = set()
        self.exchanges = set()

    def add_token(self, token: Token):
        self.tokens.add(token)
        self.graph.add_node(token)

    def add_exchange(self, exchange: Exchange):
        self.exchanges.add(exchange)
        self.graph.add_edge(exchange)

    def reset(self):
        self.graph.reset()

    def num_tokens(self):
        return len(self.tokens)

    def num_exchanges(self):
        return len(self.exchanges)

    def find_arbitrage(self, source: Token):
        return self.graph.find_cycles(source)

    def __repr__(self):
        return f"Tokens: {self.tokens}; Exchanges: {self.exchanges}\nGraph: {self.graph}"


if __name__ == "__main__":
    network = ExchangeGraph()

    # Create tokens
    eth = Token("ETH")
    usdc = Token("USDC")  # worth 1/2000 ETH
    curry = Token("CurryCoin")  # worth 1/500 ETH
    chop = Token("ChopCoin")  # worth 1/1000 ETH

    # Add tokens
    network.add_token(eth)
    network.add_token(usdc)
    network.add_token(curry)
    network.add_token(chop)

    # Create exchanges
    network.add_exchange(Exchange("Uniswap", eth, usdc, 2000))
    network.add_exchange(Exchange("Uniswap", usdc, eth, 1/2000))
    network.add_exchange(Exchange("Forgswap", eth, curry, 500))
    network.add_exchange(Exchange("Forgswap", curry, chop, 2))

    # With only SensibleSwap, no arbitrage opportunities are found
    # With TrashSwap, arbitrage opportunities are found
    network.add_exchange(Exchange("TrashSwap", chop, usdc, 1.5))  # supposed to be 2, like SensibleSwap
    network.add_exchange(Exchange("TrashSwap", usdc, chop, 1/1.5))  # supposed to be 1/2, like SensibleSwap
    # network.add_exchange(Exchange("SensibleSwap", chop, usdc, 2))
    # network.add_exchange(Exchange("SensibleSwap", usdc, chop, 1/2))

    network.add_exchange(Exchange("ChopExchange", chop, curry, 0.5))
    network.add_exchange(Exchange("ChopExchange", curry, usdc, 4))

    print("Graph created:")
    print(network)
    print("Looking for arbitrage opportunities...")

    opportunities = network.find_arbitrage(eth)
    for opportunity in opportunities:
        print("Arbitrage opportunity found:")
        exchange_rate = 1
        for swap_taken in opportunity:
            print(swap_taken)
            exchange_rate *= swap_taken.rate
        print(f"Overall exchange rate: {exchange_rate}")
