import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crp.simulation import Network
# --- NEW: Import our dumb router ---
from crp.routing.dumb_router import find_path_dijkstra

def main():
    """
    The main function to set up, run, and display the simulation.
    """
    print("[INIT] Building DePIN Simulation Environment...")

    depin_network = Network()

    depin_network.add_gateway("GATEWAY_WEST")
    depin_network.add_gateway("GATEWAY_EAST")
    for i in range(1, 6):
        depin_network.add_node(f"NODE_{i}")

    print("[INFO] Creating network links...")
    # Using a fixed seed for the random number generator ensures that the network
    # topology is the same every time we run the simulation. This is crucial for
    # comparing different routing algorithms fairly.
    random.seed(42)
    
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

    depin_network.display_topology()
    
    # --- NEW: Run the Dumb Router and display its chosen path ---
    print("\n" + "="*40)
    print("      RUNNING BASELINE ROUTER (DIJKSTRA)")
    print("="*40)
    
    start_gw = "GATEWAY_WEST"
    end_gw = "GATEWAY_EAST"
    
    print(f"Finding shortest path from {start_gw} to {end_gw} based on latency...")
    
    path, total_latency = find_path_dijkstra(depin_network, start_gw, end_gw)
    
    if path:
        print(f"\n[SUCCESS] Path found!")
        print(f"  -> Route: {' -> '.join(path)}")
        print(f"  -> Total Latency: {total_latency:.2f}ms")
    else:
        print(f"\n[FAILED] No path could be found from {start_gw} to {end_gw}.")

    print("\n[SUCCESS] Phase 2: Baseline 'Dumb' Router executed.")


if __name__ == "__main__":
    main()