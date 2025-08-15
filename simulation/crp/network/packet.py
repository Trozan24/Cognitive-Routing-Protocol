import time

class Packet:
    """
    Represents a single data packet traversing the network.
    This object is a stateful data carrier, designed to hold information
    about its journey for performance analysis.

    Attributes:
        packet_id (int): A unique identifier for the packet.
        source_id (str): The ID of the originating node.
        destination_id (str): The ID of the final destination node.
        creation_time (float): The timestamp when the packet was created.
        current_location_id (str): The ID of the node where the packet currently resides.
        path_taken (list): A list of node IDs representing the path traversed so far.
        total_latency (float): The accumulated latency during its journey.
    """
    def __init__(self, packet_id: int, source_id: str, destination_id: str):
        self.packet_id = packet_id
        self.source_id = source_id
        self.destination_id = destination_id
        self.creation_time = time.time()
        self.current_location_id = source_id
        self.path_taken = [source_id]
        self.total_latency = 0.0

    def __repr__(self):
        """Provides a developer-friendly string representation of the Packet."""
        return (f"Packet(ID={self.packet_id}, "
                f"From='{self.source_id}', To='{self.destination_id}', "
                f"Path={len(self.path_taken)} hops)")

    def log_hop(self, next_node_id: str, latency_incurred: float):
        """Updates the packet's state after traversing one link."""
        self.current_location_id = next_node_id
        self.path_taken.append(next_node_id)
        self.total_latency += latency_incurred