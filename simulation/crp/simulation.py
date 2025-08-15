# This file defines the main Network class that orchestrates the entire simulation.
# It uses the Node and Gateway classes to construct and manage the network graph.

from .network.node import Node, Gateway

class Network:
    """
    The main simulator class that manages the entire network topology and state.
    This acts as our discrete-event simulation controller, holding all nodes
    and facilitating their interactions.
    """
    def __init__(self):
        self.nodes = {}
        self.gateways = {}

    def add_node(self, node_id: str) -> Node:
        """Creates a standard Node and adds it to the network dictionary."""
        if node_id not in self.nodes:
            node = Node(node_id)
            self.nodes[node_id] = node
            return node
        return self.nodes[node_id]

    def add_gateway(self, node_id: str) -> Gateway:
        """Creates a Gateway node and adds it to the network and gateway dictionaries."""
        if node_id not in self.nodes:
            gateway = Gateway(node_id)
            self.nodes[node_id] = gateway
            self.gateways[node_id] = gateway
            return gateway
        return self.nodes[node_id]

    def get_node(self, node_id: str) -> Node:
        """Retrieves a node from the network by its ID."""
        return self.nodes.get(node_id)

    def connect_nodes(self, node1_id: str, node2_id: str, latency: float, bandwidth: int):
        """Connects two nodes in the network with specified properties."""
        node1 = self.get_node(node1_id)
        node2 = self.get_node(node2_id)
        if node1 and node2:
            node1.add_neighbor(node2, latency, bandwidth)
        else:
            # Using a print for now, will upgrade to proper logging later.
            print(f"[ERROR] Could not connect nodes. One or both IDs not found: {node1_id}, {node2_id}")

    def display_topology(self):
        """Prints a human-readable representation of the network graph and its properties."""
        print("="*40)
        print("      NETWORK TOPOLOGY VISUALIZATION")
        print("="*40)
        # Sorting keys for consistent output
        for node_id in sorted(self.nodes.keys()):
            node = self.get_node(node_id)
            print(f"-> {node}:")
            if not node.neighbors:
                print("   [No Connections]")
                continue
            for neighbor_id, properties in node.neighbors.items():
                lat = properties['latency']
                bw = properties['bandwidth']
                print(f"   -- (L: {lat:.2f}ms, BW: {bw}Mbps) --> {self.get_node(neighbor_id)}")
        print("="*40)