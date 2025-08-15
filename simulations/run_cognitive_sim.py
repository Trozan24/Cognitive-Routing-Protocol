import random
import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crp.simulation import Network
from crp.network.node import Node, Gateway
from crp.routing.dumb_router import find_path_dijkstra
from crp.routing.cognitive_node import CognitiveNode, CognitiveGateway

# --- Simulation Parameters ---
NUM_PACKETS = 1000
MAX_HOPS = 25 # Prevents packets from looping infinitely
CONGESTION_NODE_A = "NODE_2"
CONGESTION_NODE_B = "NODE_3"
CONGESTION_CHANCE = 0.4 
CONGESTION_MULTIPLIER = 10 
REWARD_FACTOR = 100.0
RANDOM_SEED = 42

def build_network(use_cognitive_nodes=False):
    """Builds the network, using either standard or cognitive nodes."""
    depin_network = Network()

    node_factory = CognitiveNode if use_cognitive_nodes else Node
    gateway_factory = CognitiveGateway if use_cognitive_nodes else Gateway

    # Create gateways
    depin_network.nodes["GATEWAY_WEST"] = gateway_factory("GATEWAY_WEST")
    depin_network.gateways["GATEWAY_WEST"] = depin_network.nodes["GATEWAY_WEST"]
    depin_network.nodes["GATEWAY_EAST"] = gateway_factory("GATEWAY_EAST")
    depin_network.gateways["GATEWAY_EAST"] = depin_network.nodes["GATEWAY_EAST"]
    
    # Create standard nodes
    for i in range(1, 6):
        depin_network.nodes[f"NODE_{i}"] = node_factory(f"NODE_{i}")

    random.seed(RANDOM_SEED)
    # Connect all nodes
    depin_network.connect_nodes("GATEWAY_WEST", "NODE_1", latency=random.uniform(5, 10), bandwidth=random.randint(500, 1000))
    depin_network.connect_nodes("GATEWAY_WEST", "NODE_2", latency=random.uniform(10, 15), bandwidth=random.randint(200, 500))
    depin_network.connect_nodes("GATEWAY_EAST", "NODE_5", latency=random.uniform(5, 10), bandwidth=random.randint(500, 1000))
    depin_network.connect_nodes("GATEWAY_EAST", "NODE_4", latency=random.uniform(10, 15), bandwidth=random.randint(200, 500))
    depin_network.connect_nodes("NODE_1", "NODE_2", latency=random.uniform(20, 30), bandwidth=random.randint(100, 200))
    depin_network.connect_nodes("NODE_1", "NODE_3", latency=random.uniform(15, 25), bandwidth=random.randint(300, 600))
    depin_network.connect_nodes("NODE_2", "NODE_3", latency=random.uniform(5, 10), bandwidth=random.randint(800, 1000))
    depin_network.connect_nodes("NODE_3", "NODE_4", latency=random.uniform(15, 25), bandwidth=random.randint(300, 600))
    depin_network.connect_nodes("NODE_4", "NODE_5", latency=random.uniform(20, 30), bandwidth=random.randint(100, 200))
    depin_network.connect_nodes("NODE_2", "NODE_5", latency=random.uniform(40, 50), bandwidth=random.randint(50, 100))
    
    return depin_network

def get_current_latency(node_a, node_b_id):
    """Gets the latency of a link, factoring in random congestion."""
    base_latency = node_a.neighbors[node_b_id]['latency']
    if (node_a.node_id == CONGESTION_NODE_A and node_b_id == CONGESTION_NODE_B) or \
       (node_a.node_id == CONGESTION_NODE_B and node_b_id == CONGESTION_NODE_A):
        if random.random() < CONGESTION_CHANCE:
            return base_latency * CONGESTION_MULTIPLIER
    return base_latency

def main():
    start_time = time.time()
    # --- Part 1: Simulate the Dumb Router ---
    print("\n" + "="*50)
    print("  PERFORMANCE ANALYSIS: DUMB ROUTER (DIJKSTRA)")
    print("="*50)
    dumb_network = build_network(use_cognitive_nodes=False)
    dumb_stats = {'total_latency': 0, 'congested_trips': 0}
    
    static_path, _ = find_path_dijkstra(dumb_network, "GATEWAY_WEST", "GATEWAY_EAST")
    print(f"Dumb Router has chosen a static path: {' -> '.join(static_path)}")
    
    for i in range(NUM_PACKETS):
        packet_latency = 0
        is_congested_trip = False
        for j in range(len(static_path) - 1):
            current_node = dumb_network.get_node(static_path[j])
            next_node_id = static_path[j+1]
            link_latency = get_current_latency(current_node, next_node_id)
            if link_latency != current_node.neighbors[next_node_id]['latency']:
                is_congested_trip = True
            packet_latency += link_latency
        dumb_stats['total_latency'] += packet_latency
        if is_congested_trip:
            dumb_stats['congested_trips'] += 1

    # --- Part 2: Simulate the Cognitive Router ---
    print("\n" + "="*50)
    print("  PERFORMANCE ANALYSIS: COGNITIVE ROUTER (MAB)")
    print("="*50)
    cognitive_network = build_network(use_cognitive_nodes=True)
    cognitive_stats = {'total_latency': 0, 'congested_trips': 0, 'successful_packets': 0, 'failed_packets': 0}

    for i in range(NUM_PACKETS):
        packet_latency = 0
        is_congested_trip = False
        
        current_node = cognitive_network.get_node("GATEWAY_WEST")
        previous_node_id = None
        packet_successful = True
        hop_count = 0
        
        while current_node.node_id != "GATEWAY_EAST":
            if hop_count > MAX_HOPS:
                packet_successful = False
                break

            next_node_id = current_node.choose_next_hop(previous_node_id)
            
            if next_node_id is None:
                packet_successful = False
                break

            link_latency = get_current_latency(current_node, next_node_id)
            if link_latency != current_node.neighbors[next_node_id]['latency']:
                is_congested_trip = True
            
            packet_latency += link_latency
            reward = REWARD_FACTOR / link_latency
            current_node.update_reward(next_node_id, reward)
            
            previous_node_id = current_node.node_id
            current_node = cognitive_network.get_node(next_node_id)
            hop_count += 1
        
        if packet_successful:
            cognitive_stats['total_latency'] += packet_latency
            cognitive_stats['successful_packets'] += 1
            if is_congested_trip:
                cognitive_stats['congested_trips'] += 1
        else:
            cognitive_stats['failed_packets'] += 1
            
        if (i + 1) % 100 == 0:
            print(f"  ... {i+1}/{NUM_PACKETS} packets routed.")

    # --- Part 3: Final Results ---
    print("\n" + "="*50)
    print("              COMPARATIVE ANALYSIS RESULTS")
    print("="*50)
    
    avg_dumb_latency = dumb_stats['total_latency'] / NUM_PACKETS
    print(f"--- DUMB ROUTER (BASELINE) ---")
    print(f"  Success Rate: 100.00% ({NUM_PACKETS}/{NUM_PACKETS})")
    print(f"  Average Packet Latency: {avg_dumb_latency:.2f}ms")
    print(f"  Trips through Congested Link: {dumb_stats['congested_trips']}/{NUM_PACKETS}")
    
    print(f"\n--- COGNITIVE ROUTER (CRP) ---")
    success_rate = (cognitive_stats['successful_packets'] / NUM_PACKETS) * 100
    avg_cognitive_latency = cognitive_stats['total_latency'] / cognitive_stats['successful_packets'] if cognitive_stats['successful_packets'] > 0 else 0
    print(f"  Success Rate: {success_rate:.2f}% ({cognitive_stats['successful_packets']}/{NUM_PACKETS})")
    print(f"  Average Packet Latency (successful packets): {avg_cognitive_latency:.2f}ms")
    print(f"  Trips through Congested Link: {cognitive_stats['congested_trips']}/{NUM_PACKETS}")
    
    print("\n" + "-"*50)
    if avg_dumb_latency > 0 and avg_cognitive_latency > 0:
        performance_gain = ((avg_dumb_latency - avg_cognitive_latency) / avg_dumb_latency) * 100
        print(f"Performance Improvement (Lower Latency): {performance_gain:.2f}%")
    print("-"*50)
    print(f"\nTotal simulation time: {time.time() - start_time:.2f} seconds")
    print("\n[SUCCESS] Phase 4: Comparative analysis complete.")

if __name__ == "__main__":
    main()