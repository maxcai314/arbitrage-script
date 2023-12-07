from graph import Graph, Node, Edge

# Create graph
graph = Graph()

# Create nodes
node_source = Node("Source")
node_1 = Node("1")
node_2 = Node("2")
node_3 = Node("3")
node_4 = Node("4")
node_5 = Node("5")


# Add nodes
graph.add_node(node_source)
graph.add_node(node_1)
graph.add_node(node_2)
graph.add_node(node_3)
graph.add_node(node_4)
graph.add_node(node_5)

# Add edges
graph.add_edge(Edge.from_nodes(node_source, node_1, 1))
graph.add_edge(Edge.from_nodes(node_source, node_5, 3))
graph.add_edge(Edge.from_nodes(node_1, node_source, 2))
graph.add_edge(Edge.from_nodes(node_2, node_1, 1.5))
graph.add_edge(Edge.from_nodes(node_1, node_2, 1.5))
graph.add_edge(Edge.from_nodes(node_2, node_3, 3))
graph.add_edge(Edge.from_nodes(node_2, node_3, -1))  # duplicate, should take better (negative) path
graph.add_edge(Edge.from_nodes(node_3, node_4, 3))
graph.add_edge(Edge.from_nodes(node_4, node_5, -5))
graph.add_edge(Edge.from_nodes(node_5, node_1, 1))

print("Graph created:")
print(f"Nodes: {graph.nodes}")
print(f"Edges: {graph.edges}")
print("Looking for cycles...")

# Find cycles
cycles = graph.find_cycles(node_source)
edge_lookup = graph.edge_dict()
for cycle in cycles:
    print("Cycle found:")
    loop_cost = 0
    for edge_taken in cycle:
        print(edge_taken)
        loop_cost += edge_taken.weight
    print(f"Total cost: {loop_cost}")
    