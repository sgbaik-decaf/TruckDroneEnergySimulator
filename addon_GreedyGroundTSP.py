import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms.approximation import greedy_tsp

# Columns: 'startNode', 'endNode', 'time(s)', 'dist(m)'

def SolveGreedyTSP(data):
    # Extract the unique nodes
    nodes = sorted(data['startNode'].unique())
    num_nodes = len(nodes)
    
    # Create a time matrix
    time_matrix = np.zeros((num_nodes, num_nodes))
    for _, row in data.iterrows():
        i = int(row['startNode'])
        j = int(row['endNode'])
        time = row['time(s)']
        time_matrix[i, j] = time
    
    # Create a distance matrix
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for _, row in data.iterrows():
        i = int(row['startNode'])
        j = int(row['endNode'])
        distance = row['dist(m)']
        distance_matrix[i, j] = distance
    
    # Create a directed graph and add edges
    graph = nx.DiGraph()
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                graph.add_edge(i, j, weight=time_matrix[i, j])
    
    try:
        # Solve the TSP using a greedy heuristic
        tour = greedy_tsp(graph, source=0)
        Total_time = sum(time_matrix[tour[i], tour[i+1]] for i in range(len(tour)-1))
        Total_dist = sum(distance_matrix[tour[i], tour[i+1]] for i in range(len(tour)-1))

        # Print the result
        if __name__ == '__main__':
            print(tour)
        if __name__ == '__main__':
            print("Total time:", Total_time)
        if __name__ == '__main__':
            print("Total distance:", Total_dist)
        return Total_dist

    except Exception as e:
        print("An error occurred while solving the TSP:")
