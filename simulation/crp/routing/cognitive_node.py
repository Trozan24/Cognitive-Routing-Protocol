import math
import random

from ..network.node import Node

class CognitiveNode(Node):
    """
    An intelligent version of a Node that uses a Multi-Armed Bandit (MAB) algorithm
    to make routing decisions. It learns over time which neighbors lead to the
    best outcomes (rewards).
    """
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.mab_data = {}
        self.total_pulls = 0

    def add_neighbor(self, neighbor_node: 'Node', latency: float, bandwidth: int):
        """Overrides the parent method to also initialize MAB data for the new neighbor."""
        super().add_neighbor(neighbor_node, latency, bandwidth)
        if neighbor_node.node_id not in self.mab_data:
            self.mab_data[neighbor_node.node_id] = {'counts': 0, 'values': 0.0}

    def choose_next_hop(self, prev_node_id: str = None) -> str:
        """
        Selects the next hop using the UCB1 algorithm, avoiding the previous node.
        """
        # --- FIX: Filter out the previous node to prevent immediate reversal ---
        available_neighbors = [nid for nid in self.neighbors if nid != prev_node_id]

        if not available_neighbors:
            return None # This is a dead end, packet will fail

        self.total_pulls += 1

        # First, check for any available neighbors that have never been tried
        for neighbor_id in available_neighbors:
            if self.mab_data[neighbor_id]['counts'] == 0:
                return neighbor_id

        # If all have been tried at least once, calculate UCB1 scores
        best_neighbor = None
        max_score = -1

        for neighbor_id in available_neighbors:
            arm_data = self.mab_data[neighbor_id]
            
            average_reward = arm_data['values']
            exploration_term = math.sqrt((2 * math.log(self.total_pulls)) / arm_data['counts'])
            ucb_score = average_reward + exploration_term

            if ucb_score > max_score:
                max_score = ucb_score
                best_neighbor = neighbor_id
        
        return best_neighbor

    def update_reward(self, chosen_neighbor_id: str, reward: float):
        """
        Updates the MAB data for a chosen neighbor after receiving a reward.
        """
        if chosen_neighbor_id not in self.mab_data:
            return

        arm_data = self.mab_data[chosen_neighbor_id]
        arm_data['counts'] += 1
        n = arm_data['counts']
        
        old_value = arm_data['values']
        new_value = old_value + (reward - old_value) / n
        arm_data['values'] = new_value

class CognitiveGateway(CognitiveNode):
    """A gateway that uses the CognitiveNode's AI for routing decisions."""
    def __repr__(self):
        return f"CognitiveGateway(ID='{self.node_id}')"