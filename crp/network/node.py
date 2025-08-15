# Note: This file has no dependencies other than Python's standard library.
# It defines the core structural components of the network graph.

class Node:
    """
    Represents a standard node in the DePIN network.
    It maintains a dictionary of its direct neighbors and the connection
    properties (latency, bandwidth) to them.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        # Neighbors dict format: {neighbor_node_id: {'latency': float, 'bandwidth': int}}
        self.neighbors = {}

    def add_neighbor(self, neighbor_node: 'Node', latency: float, bandwidth: int):
        """
        Adds a bidirectional connection to a neighboring node.
        This method ensures the graph is undirected by default.
        """
        if neighbor_node.node_id not in self.neighbors:
            self.neighbors[neighbor_node.node_id] = {
                'latency': latency,      # in milliseconds (ms)
                'bandwidth': bandwidth   # in Megabits per second (Mbps)
            }
            # Ensure the connection is reciprocal for a symmetric graph
            neighbor_node.add_neighbor(self, latency, bandwidth)

    def __repr__(self):
        """Provides a developer-friendly string representation of the Node."""
        return f"Node(ID='{self.node_id}')"

class Gateway(Node):
    """
    Represents a special type of Node that acts as an entry or exit point for the network.
    It inherits all properties from the base Node class and can be extended with
    specialized logic for handling traffic entering or leaving the simulation.
    """
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def __repr__(self):
        """Provides a specific string representation for Gateways."""
        return f"Gateway(ID='{self.node_id}')"