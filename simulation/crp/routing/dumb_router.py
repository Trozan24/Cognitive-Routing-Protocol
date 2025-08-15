import heapq

def find_path_dijkstra(network, start_node_id: str, end_node_id: str):
    """
    Finds the shortest path between two nodes using Dijkstra's algorithm.

    The "cost" of traversing an edge is defined purely by its latency.

    Args:
        network: The Network object containing the full graph.
        start_node_id: The ID of the starting node.
        end_node_id: The ID of the target node.

    Returns:
        A tuple containing:
        - A list of node IDs representing the shortest path.
        - The total accumulated latency of that path.
        Returns (None, float('inf')) if no path is found.
    """
    # Priority queue stores tuples of (total_latency, current_node_id, path_list)
    pq = [(0, start_node_id, [])]
    visited = set()
    
    # Using a dictionary to store the shortest path found so far to each node
    # Format: {node_id: (total_latency, path_list)}
    shortest_paths = {start_node_id: (0, [])}

    while pq:
        (latency, current_node_id, path) = heapq.heappop(pq)

        if current_node_id in visited:
            continue
        
        # Add the current node to the path history
        path = path + [current_node_id]
        visited.add(current_node_id)

        if current_node_id == end_node_id:
            return path, latency

        current_node = network.get_node(current_node_id)
        if not current_node:
            continue

        for neighbor_id, properties in current_node.neighbors.items():
            if neighbor_id not in visited:
                new_latency = latency + properties['latency']
                
                # If we found a shorter path to this neighbor, update it
                if new_latency < shortest_paths.get(neighbor_id, (float('inf'), None))[0]:
                    shortest_paths[neighbor_id] = (new_latency, path)
                    heapq.heappush(pq, (new_latency, neighbor_id, path))

    return None, float('inf') # No path found