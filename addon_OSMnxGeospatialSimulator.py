import os
import random

import numpy as np
import pandas as pd
import osmnx as ox

def BuildBoxGraph(city_name, depot_addr, bbox_range, CityCenterParam):
    pd.options.display.float_format = '{:.6f}'.format
    os.makedirs('Problems/myproblem', exist_ok=True)
    if __name__ == '__main__':
        print('OSMnx version is :', ox.__version__)

    city = city_name
    city_center = ox.geocoder.geocode(city_name)
    depot_xy = ox.geocoder.geocode(depot_addr)

    if __name__ == '__main__':
        print('Building graph representation for : %s' % city)

    G = ox.graph.graph_from_point(city_center, dist=bbox_range*1000+2000, dist_type='bbox', network_type='drive', truncate_by_edge=False)
    Gp = ox.project_graph(G)

    G_cust = ox.graph.graph_from_point(city_center, dist=bbox_range*1000, dist_type='bbox', network_type='drive', truncate_by_edge=False)
    Gp_cust = ox.project_graph(G_cust)

    G_cust_mini = ox.graph.graph_from_point(city_center, dist=bbox_range*1000*CityCenterParam, dist_type='bbox', network_type='drive', truncate_by_edge=False)
    Gp_cust_mini = ox.project_graph(G_cust_mini)

    if __name__ == '__main__':
        print('Done!')

    return city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini

def SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini):
    # Create 10 sample customer locations within the graph border
    if random.random() <=0.5:
        points = ox.utils_geo.sample_points(ox.convert.to_undirected(Gp_cust), n=10)
    elif random.random() >0.5:
        points = ox.utils_geo.sample_points(ox.convert.to_undirected(Gp_cust_mini), n=10)
    X = points.x.values
    Y = points.y.values
    
    
    # Identify closest nodes for each sample locations
    cust_nodes = ox.nearest_nodes(Gp, X, Y, return_dist=False)
    if __name__ == '__main__':
        print('Nearest nodes for customers :', cust_nodes)
    depot_node = ox.nearest_nodes(Gp, depot_xy[1], depot_xy[0])
    if __name__ == '__main__':
        print('Nearest node for delivery depot :', depot_node)

    # Convert projection from X/Y to WGS84
    points_wgs84 = ox.projection.project_gdf(points, to_crs='WGS84', to_latlong=False)
    X_wgs84 = points_wgs84.x.values
    Y_wgs84 = points_wgs84.y.values
    
    # Append depot location as the last entry of the nodes
    X_wgs84 = np.append(X_wgs84, depot_xy[1])
    Y_wgs84 = np.append(Y_wgs84, depot_xy[0])
    X_wgs84 = np.round(X_wgs84, decimals=6)
    Y_wgs84 = np.round(Y_wgs84, decimals=6)

    # Create DataFrame for all nodes
    nodes_DF = pd.DataFrame([cust_nodes, X_wgs84, Y_wgs84], index=['node_no', 'x_coord', 'y_coord'])
    nodes_DF = nodes_DF.T
    nodes_DF.iloc[10,0] = depot_node
    nodes_DF['% nodeID'] = list(range(1,10+1)) + [0]
    nodes_DF['nodeType'] = [1 for _ in range(10)] + [0]
    nodes_DF['latDeg'] = nodes_DF['y_coord']
    nodes_DF['lonDeg'] = nodes_DF['x_coord']
    nodes_DF['altMeters'] = [0 for _ in range(10)] + [0]
    nodes_DF['parcelWtLbs'] = [1.1 for _ in range(8)] + [100 for _ in range(2)]+[-1]
    nodes_DF.drop(columns=['x_coord', 'y_coord'], inplace=True)
    nodes_DF = nodes_DF.reindex([10,0,1,2,3,4,5,6,7,8,9])
    nodes_DF = nodes_DF.reset_index(drop = True)

    if __name__ == '__main__':
        print(nodes_DF.to_string())

    global nodes_DF_global
    nodes_DF_global = nodes_DF

    nodes_DF_out = nodes_DF.copy()
    nodes_DF_out.drop(columns=['node_no'], inplace=True)
    nodes_DF_out.to_csv('Problems/myproblem/tbl_locations.csv', index=False)
    if __name__ == '__main__':
        print("Nodes information saved at :'Problems/myproblem/tbl_locations.csv'.\n")
    
    # Impute speed and travel time for edges in the graph
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    def dist_and_time(orig, dest):
        '''
        Returns origin node, destination node, distance in km, time in s
        Returns 0 for distance and time if nodes are self-referential
        '''
        if int(orig) == int(dest):
            route_length = 0
            route_time = 0
        else:
            route = ox.shortest_path(G, orig, dest, weight="length")
            # ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=0)
            route_length = int(sum(ox.routing.route_to_gdf(G, route, weight="length")["length"]))
            route_time = int(sum(ox.routing.route_to_gdf(G, route, weight="length")["travel_time"]))
        return (str(orig), str(dest), route_length, route_time)

    # Build DataFrame for distance & time matrix
    if __name__ == '__main__':
        print('Building distance & time matrix for nodes in : %s' % city, '\nEstimated time : 15s...')
    mFSTSP_travel_columns = [
        '% from location i',
        ' to location j',
        ' time [sec]',
        ' distance [meters]']
    
    matrix = []
    for i in range(len(nodes_DF)):
        for j in range(len(nodes_DF)):
            line = [
            i,
            j,
            dist_and_time(nodes_DF['node_no'][i], nodes_DF['node_no'][j])[3],
            dist_and_time(nodes_DF['node_no'][i], nodes_DF['node_no'][j])[2]
            ]
            matrix.append(line)
    if __name__ == '__main__':
        print('Done!\n')
    matrix_DF = pd.DataFrame(matrix, columns = mFSTSP_travel_columns)
    pd.options.display.float_format = None
    if __name__ == '__main__':
        print(matrix_DF.to_string())
    matrix_DF.to_csv('Problems/myproblem/tbl_truck_travel_data_PG.csv', index=False)
    if __name__ == '__main__':
        print("Distance & Time matrix saved at :'Problems/myproblem/tbl_truck_travel_data_PG.csv'.\n")
    matrix_DF_copy = matrix_DF.copy()
    matrix_DF_copy['startNode'] = matrix_DF_copy['% from location i']
    matrix_DF_copy['endNode'] = matrix_DF_copy[' to location j']
    matrix_DF_copy['time(s)'] = matrix_DF_copy[' time [sec]']
    matrix_DF_copy['dist(m)'] = matrix_DF_copy[' distance [meters]']
    matrix_DF_copy.drop(columns=['% from location i', ' to location j', ' time [sec]', ' distance [meters]'], inplace=True)
    return matrix_DF_copy
    if __name__ == '__main__':
        print("Distance & Time matrix returned as a global variable 'matrix_DF_copy'.")


if __name__ == '__main__':
    city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini = BuildBoxGraph("Pittsburgh, PA", '5000 Forbes Ave', 10, 0.5)
    matrix_DF = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)