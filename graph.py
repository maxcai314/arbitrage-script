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
        return self.name


class Edge:
    def __init__(self, name, from_node: Node, to_node: Node, weight: float):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    
    @classmethod
    def from_nodes(cls, from_node: Node, to_node: Node, weight: float):
        return cls(f"Edge", from_node, to_node, weight)

    def can_traverse(self) -> bool:
        return self.from_node.is_traversed() and self.from_node.distance + self.weight < self.to_node.distance

    def traverse(self):
        self.to_node.distance = self.from_node.distance + self.weight
        self.to_node.predecessor = self.from_node

    def __repr__(self):
        return f"{self.name}: {self.from_node} -> {self.to_node} ({self.weight:+})"


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

    def edge_dict(self):
        edge_dict = dict.fromkeys(self.nodes)
        for entry in edge_dict:
            edge_dict[entry] = []
        for edge in self.edges:
            edge_dict[edge.from_node].append(edge)
        return edge_dict

    def find_cycles(self, start_node: Node):
        # uses the Bellman-Ford algorithm to find negative cycles
        self.reset()
        start_node.distance = 0

        # create a lookup table for edges
        edge_lookup_dict = self.edge_dict()

        # relax all edges n-1 times
        update_nodes = [start_node]
        for i in range(self.num_nodes() - 1):
            new_update_nodes = []
            for node in update_nodes:
                for edge in edge_lookup_dict[node]:
                    if edge.can_traverse():
                        edge.traverse()
                        new_update_nodes.append(edge.to_node)
            update_nodes = new_update_nodes

        # check for any possible updates
        cycles_found = []
        for node in update_nodes:
            for edge in edge_lookup_dict[node]:
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
                    # convert to edge list
                    current_cycle = [min([edge for edge in edge_lookup_dict[current_cycle[i]] if edge.to_node == current_cycle[i+1]], key=lambda x: x.weight) for i in range(len(current_cycle)-1)]
                    cycles_found.append(current_cycle)
        return cycles_found

    def __repr__(self):
        return f"Graph: {self.nodes}; {self.edges}"


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
    graph.add_edge(Edge("Edge 1",node_a, node_b, 2))
    graph.add_edge(Edge("Edge 2", node_b, node_c, -5))
    graph.add_edge(Edge("Edge 3", node_c, node_a, 2))

    print("Graph created:")
    print(graph)
    print("Looking for cycles...")

    # Find cycles
    cycles = graph.find_cycles(node_a)
    edge_lookup = graph.edge_dict()
    for cycle in cycles:
        print("Cycle found:")
        loop_cost = 0
        for edge_taken in cycle:
            print(edge_taken)
            loop_cost += edge_taken.weight
        print(f"Total cost: {loop_cost}")
