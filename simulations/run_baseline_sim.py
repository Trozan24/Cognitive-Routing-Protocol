import random
import sys
import os

# This adds the root directory of the project to the Python path.
# It allows us to import from the 'crp' package even when running this script
# from the 'simulations' directory or any other location.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crp.simulation import Network

def main():
    """
    The main function to set up and display the network.
    """
    print("[INIT] Building DePIN Simulation Environment...")

    # 1. Instantiate the Network from our library
    depin_network = Network()

    # 2. Create Nodes and Gateways
    depin_network.add_gateway("GATEWAY_WEST")
    depin_network.add_gateway("GATEWAY_EAST")

    for i in range(1, 6):
        depin_network.add_node(f"NODE_{i}")

    # 3. Connect nodes with variable latency and bandwidth
    print("[INFO] Creating network links...")
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

    # 4. Display the resulting topology
    depin_network.display_topology()
    
    print("\n[SUCCESS] Phase 1: Simulation environment constructed and verified.")
    print("The modular codebase is now fully functional.")

if __name__ == "__main__":
    main()