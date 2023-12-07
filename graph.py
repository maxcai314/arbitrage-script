class Node:
    def __init__(self, name):
        self.name = name
        self.distance = float("inf")
        self.predecessor = None

    def reset(self):
        self.distance = float("inf")
        self.predecessor = None

    def is_traversed(self):
        return self.distance != float("inf")

    def __repr__(self):
        return f"Node {self.name}: {self.distance}"


class Edge:
    def __init__(self, from_node: Node, to_node: Node, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    def can_traverse(self) -> bool:
        return self.from_node.is_traversed() and self.from_node.distance + self.weight < self.to_node.distance

    def traverse(self):
        self.to_node.distance = self.from_node.distance + self.weight
        self.to_node.predecessor = self.from_node

    def __repr__(self):
        return f"Edge from {self.from_node.name} to {self.to_node.name}: {self.weight}"


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node: Node):
        self.nodes.add(node)

    def add_edge(self, edge: Edge):
        if edge.from_node not in self.nodes:
            self.add_node(edge.from_node)
        if edge.to_node not in self.nodes:
            self.add_node(edge.to_node)
        self.edges.add(edge)

    def reset(self):
        for node in self.nodes:
            node.reset()

    def num_nodes(self):
        return len(self.nodes)

    def num_edges(self):
        return len(self.edges)

    def find_cycles(self, start_node: Node):
        # uses the Bellman-Ford algorithm to find negative cycles
        self.reset()
        start_node.distance = 0

        # create a lookup table for edges
        edge_dict = dict.fromkeys(self.nodes, [])
        for edge in self.edges:
            edge_dict[edge.from_node].append(edge)

        # relax all edges n-1 times
        update_nodes = [start_node]
        for i in range(self.num_nodes() - 1):
            new_update_nodes = []
            for node in update_nodes:
                for edge in edge_dict[node]:
                    if edge.can_traverse():
                        edge.traverse()
                        new_update_nodes.append(edge.to_node)
            update_nodes = new_update_nodes

        # check for any possible updates
        cycles_found = []
        for node in update_nodes:
            for edge in edge_dict[node]:
                if edge.can_traverse():
                    # trace back the predecessors: should find circular path
                    current_cycle = [edge.to_node, edge.from_node]

                    current_node = edge.from_node.predecessor
                    for i in range(self.num_nodes()):  # max iterations
                        if current_node in current_cycle:
                            break

                        current_cycle.append(current_node)
                        current_node = current_node.predecessor
                    else:  # theoretically impossible, but just in case
                        raise "Max iteration reached during cycle traceback"
                    current_cycle.append(current_node)

                    # prune the cycle to remove the part before the cycle
                    current_cycle.reverse()
                    current_cycle = current_cycle[current_cycle.index(current_node):]
                    cycles_found.append(current_cycle)
        return cycles_found


if __name__ == "__main__":
    # Create graph
    graph = Graph()

    # Create nodes
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")

    # Add nodes
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)

    # Add edges
    graph.add_edge(Edge(node_a, node_b, 2))
    graph.add_edge(Edge(node_b, node_c, -5))
    graph.add_edge(Edge(node_c, node_a, 2))

    # Find cycles
    cycles = graph.find_cycles(node_a)

    for cycle in cycles:
        output = "Cycle found: "
        for node in cycle[:-1]:
            output += node.name + " -> "
