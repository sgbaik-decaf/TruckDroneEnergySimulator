#_____________________[PACKAGE INFORMATION]__________________

# Author:      Baik, Seung Gyu
# Contact:     seunggyb@alumni.cmu.edu
# Affiliation: Carnegie Mellon University

# Accompanying Article:
# Framework for modeling Energy Savings of Truck-drone Hybrid Deliveries in Arbitrary Cities



#_________________________[DISCLAIMER]_______________________

# This package is designed to be an "add-on" extension to the mFSTSP Solver.
# The original source code by Murray & Raj (2020) is on Github.
# https://github.com/optimatorlab/mFSTSP



#________________[DEPENDENCIES FOR THIS PROGRAM]_____________
# 1. NUMPY         https://numpy.org/install/
# 2. PANDAS        https://pandas.pydata.org/docs/getting_started/install.html
# 3. NETWORKX      https://networkx.org/documentation/stable/install.html
# 4. OSMNX         https://osmnx.readthedocs.io/en/stable/installation.html
# 5. MATPLOTLIB    https://matplotlib.org/stable/install/index.html
# 6. SEABORN       https://seaborn.pydata.org/installing.html
# 7. MFSTSP SOLVER PACKAGE (THE WHOLE THING including GUROBIPY)
# 8. "addon_OSMnxGeospatialSimulator.py",
#    "addon_EnergyConsumptionCalculator.py",
#    "addon_HaversineFunction.py",
#    "addon_GreedyGroundTSP.py"



#____________________________________________________________
# Load Dependencies

print('Loading modules and packages(dependencies)')
try:
    import sys
    import datetime
    import time
    import math
    from collections import defaultdict
    import os
    import os.path
    import random
    import multiprocessing as mp
    from subprocess import call
    import warnings
    
    import numpy as np
    import pandas as pd
    import networkx as nx
    from networkx.algorithms.approximation import greedy_tsp
    import osmnx as ox
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    from newmain import *
    from parseCSV import *
    from parseCSVstring import *
    from solve_mfstsp_IP import *
    from solve_mfstsp_heuristic import *
    import distance_functions

    from addon_OSMnxGeospatialSimulator import *
    from addon_EnergyConsumptionCalculator import *
    from addon_HaversineFunction import haversine
    from addon_GreedyGroundTSP import SolveGreedyTSP

except:
    print('One or more modules or packages(dependencies) have not been found in your environment.')

warnings.simplefilter(action='ignore', category=FutureWarning)

print('{:<20s}{:<10s}{:<20s}{:<10s}'.format(
    'NumPy version: ', np.__version__, 'Recommended:', '1.26.4'))
print('{:<20s}{:<10s}{:<20s}{:<10s}'.format(
    'Pandas version: ', pd.__version__, 'Recommended:', '2.2.3'))
print('{:<20s}{:<10s}{:<20s}{:<10s}'.format(
    'NetworkX version: ', nx.__version__, 'Recommended:', '3.3'))
print('{:<20s}{:<10s}{:<20s}{:<10s}'.format(
    'OSMnx version: ', ox.__version__, 'Recommended:', '1.9.4'))
print('{:<20s}{:<10s}{:<20s}{:<10s}'.format(
    'Gurobi version: ', '-', 'Recommended:', '11.0.3'))



#____________________________________________________________
# Get User Inputs

print('_' * os.get_terminal_size().columns)

print('SET PARAMETERS')

print('\nEnter a city name and state name to analyze\n(e.g. "Pittsburgh, PA")')
city_input = input('>>')

print('\nEnter an address for delivery depot location \n(e.g. "1723 Murray Ave, Pittsburgh, PA")')
depot_input = input('>>')

print('\nSpecify the size of you area of operations in km \n(Suggested: 5~15)')
bbox_range = int(input('>>'))

print('\nSet analysis mode\n[1]: Single Instance Simulation\n[2]: Monte Carlo Simulation')
MonteCarloIndicator = int(input('>>'))-1

print('\nSpecify city center parameter in & \n(Suggested: 0.3~0.7)')
CityCenterParam = float(input('>>'))

if MonteCarloIndicator == 1:
    print('\nSet number of simulations to run \n(Suggested: 30-100)')
    MonteCarloInstances = int(input('>>'))

elif MonteCarloIndicator == 0:
    MonteCarloInstances = 1
    print('\nDisplay intermediate data?\n[1]: No\n[2]: Yes')
    DisplayIntermediateDataFrame = bool(int(input('>>'))-1)

# Diesel truck depot to door = 4.29 kWh/mi = 2665.69 Wh/km (DoE 2020)
# EV truck depot to door = 1 kWh/mi = 621.37 Wh/km (DoE 2020)
# EV van depot to door = 0.56 kWh/mi = 347.97 Wh/km (DoE 2020)

BaselineInformation = {'Diesel Truck':2665.69, 'EV Truck':621.37, 'EV Van':347.97}



#____________________________________________________________
# Initiate simulation

start_time = time.time()

print('_' * os.get_terminal_size().columns)

SavingsComparedToTruck = []
SavingsComparedToEVTruck = []
SavingsComparedToEVVan = []

for iterationno in range(MonteCarloInstances):
    int_start_time = time.time()
    print(f'Running Simulation Instance #{iterationno+1}/{MonteCarloInstances}...')



    #____________________________________________________________
    # MODULE I: GEOSPATIAL SIMULATOR

    if iterationno == 0:
        print('Iteration #1 typically takes longer.')
        try:
            city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini = BuildBoxGraph(city_input, depot_input, bbox_range, CityCenterParam)
            print(f'Graph Representation for "{city}" Generated')
            ox.plot.plot_graph(G, node_size=1)
            matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
            print('Customer Batch & Travel Matrix Generated')
        except:
            try:
                print('[ WARNING ] OpenStreetMap and/or OSMnx is not working as expected.\nThe program will try executing one last time.')
                city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini = BuildBoxGraph(city_input, depot_input, bbox_range, CityCenterParam)
                print(f'Graph Representation for "{city}" Generated')
                ox.plot.plot_graph(G, node_size=1)
                matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
                print('Customer Batch & Travel Matrix Generated')
            except:
                sys.exit('[ WARNING ] There was an error with OpenStreetMap and/or OSMnx. Common causes are:\n(1) Internet connection issue\n(2) Typo in query\n(3) Disconnected node')
    elif iterationno >= 1:
        try:
            matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
            print('Customer Batch & Travel Matrix Generated')
        except:
            try:
                matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
                print('Customer Batch & Travel Matrix Generated')
            except:
                try:
                    print('[ WARNING ] OpenStreetMap and/or OSMnx is not working as expected.\nThe program will try executing one last time.')
                    matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
                    print('Customer Batch & Travel Matrix Generated')
                except:
                    warnings.warn('[ WARNING ] There was an error with OpenStreetMap and/or OSMnx. Intance this iteration will reiterate previous instance.')



    #____________________________________________________________
    # MODULE II: MFSTSP HEURISTIC SOLVER

    (a, b, c, d) = (
        missionControl().return_nodes_DF(),
        missionControl().return_sol_DF(),
        missionControl().return_UAV_DF(),
        missionControl().return_Truck_DF()
                 )
    sorties = c.copy()
    truck_tour = d.copy()
    UAV_info = missionControl().return_UAV_INFO_DF()
    if MonteCarloIndicator == 0:
        print('Routing & Scheduling Plan Retrieved')



    #____________________________________________________________
    # MODULE III: ENERGY USE CALCULATOR

    UAV_energy_DF = runDroneEnergyModule(sorties, UAV_info)
    Ground_energy_DF = runTruckEnergyModule(truck_tour, matrix_DF_copy, BaselineInformation)
    UAV_energy_sum = round(UAV_energy_DF['energy_use(Wh)'].sum(), 2)
    Truck_energy_sum = round(Ground_energy_DF['energy(Wh, Diesel Truck)'].sum(), 2)
    EVTruck_energy_sum = round(Ground_energy_DF['energy(Wh, EV Truck)'].sum(), 2)
    EVVan_energy_sum = round(Ground_energy_DF['energy(Wh, EV Van)'].sum(), 2)
    if MonteCarloIndicator == 0:
        print('Energy Use for Hybrid Scenario Calculated')



    #____________________________________________________________
    # Solve baseline TSP

    baseline_tsp_dist = SolveGreedyTSP(matrix_DF_copy)
    baseline_tsp_DF = pd.DataFrame(
    [[BaselineInformation['Diesel Truck'] * baseline_tsp_dist / 1000,
    BaselineInformation['EV Truck'] * baseline_tsp_dist / 1000,
    BaselineInformation['EV Van'] * baseline_tsp_dist / 1000]],
    columns=['energy(Wh, Diesel Truck)',
             'energy(Wh, EV Truck)',
             'energy(Wh, EV Van)']
    )

    if MonteCarloIndicator == 0:
        print('Energy Use for Baseline Scenario Calculated')



    #____________________________________________________________
    # Compare hybrid scenario to baseline scenario

    SavingsComparedToTruck.append(
        round(
              baseline_tsp_DF['energy(Wh, Diesel Truck)'][0]
          -
          (UAV_energy_sum + Truck_energy_sum),
          2)
        /1000)
    SavingsComparedToEVTruck.append(
        round(
              baseline_tsp_DF['energy(Wh, EV Truck)'][0]
          -
          (UAV_energy_sum + EVTruck_energy_sum),
          2)
        /1000)
    SavingsComparedToEVVan.append(
        round(
              baseline_tsp_DF['energy(Wh, EV Van)'][0]
          -
          (UAV_energy_sum + EVVan_energy_sum),
          2)
        /1000)

    print('Energy Savings Calculated')



    #____________________________________________________________
    # Complete this simulation instance and record its result

    int_end_time = time.time()
    int_time = round(int_end_time - int_start_time, 2)
    print('Simulation Result Noted')
    print(f'Instance #{iterationno+1} took {int_time} seconds\n')



#____________________________________________________________
# Display Simulation Result

if MonteCarloIndicator == 0 and DisplayIntermediateDataFrame == True:
    print('_' * os.get_terminal_size().columns)
    print('[INTERMEDIATE DATAFRAME]')
    print(UAV_energy_DF)

print('_' * os.get_terminal_size().columns)
print('[RESULT]')

end_time = time.time()
print("\nTotal elapsed time: ",round(end_time-start_time, 2), "seconds")

print('\nEnergy Savings from Hybrid system compared to Diesel Truck (kWh):')
print('MEAN:', round(np.average(SavingsComparedToTruck), 2))
print('MEDIAN:', round(np.median(SavingsComparedToTruck), 2))
print('SD:', round(np.std(SavingsComparedToTruck), 2))
print('MIN~MAX:', round(np.min(SavingsComparedToTruck), 2), '~', round(np.max(SavingsComparedToTruck), 2))

print('\nEnergy Savings from Hybrid system compared to EV Truck (kWh):')
print('MEAN:', round(np.average(SavingsComparedToEVTruck), 2))
print('MEDIAN:', round(np.median(SavingsComparedToEVTruck), 2))
print('SD:', round(np.std(SavingsComparedToEVTruck), 2))
print('MIN~MAX:', round(np.min(SavingsComparedToEVTruck), 2), '~', round(np.max(SavingsComparedToEVTruck), 2))

print('\nEnergy Savings from Hybrid system compared to EV Van (kWh):')
print('MEAN:', round(np.average(SavingsComparedToEVVan), 2))
print('MEDIAN:', round(np.median(SavingsComparedToEVVan), 2))
print('SD:', round(np.std(SavingsComparedToEVVan), 2))
print('MIN~MAX:', round(np.min(SavingsComparedToEVVan), 2), '~', round(np.max(SavingsComparedToEVVan), 2))



#____________________________________________________________
# Visualize Simulation Result

print('\nPlot and save results?\n[1]: No\n[2]: Yes')
viz = int(input('>>'))-1

if viz == 1:
    MC_sim_output_DF = pd.DataFrame(
        {
            'vs Truck' : SavingsComparedToTruck,
            'vs EV Truck' : SavingsComparedToEVTruck,
            'vs EV Van' : SavingsComparedToEVVan
        }
    )
    
    sns.catplot(
        data = pd.melt(MC_sim_output_DF),
        x = 'variable',
        hue = 'variable', legend = False,
        y = 'value',
        palette = ['royalblue', 'springgreen', 'orange']
        )
    plt.subplots_adjust(top = 0.9)
    plt.suptitle(f'Energy Savings for {city_input} (kWh/tour)')
    plt.ylabel('')
    plt.savefig('output_datapoints.png', dpi=300)
    plt.show()
    plt.close()
    
    fig, axs = plt.subplots(1, 3, figsize=(5, 3))
    sns.boxplot(
        data = MC_sim_output_DF,
        y = 'vs Truck',
        notch = True,
        color = 'royalblue',
        medianprops={"color": "black", "linewidth": 1},
        ax = axs[0])
    sns.boxplot(
        data = MC_sim_output_DF,
        y = 'vs EV Truck',
        notch = True,
        color = 'springgreen',
        medianprops={"color": "black", "linewidth": 1},
        ax = axs[1])
    sns.boxplot(
        data = MC_sim_output_DF,
        y = 'vs EV Van',
        notch = True,
        color = 'orange',
        medianprops={"color": "black", "linewidth": 1},
        ax = axs[2])
    
    plt.tight_layout()
    plt.subplots_adjust(top = 0.9)
    plt.suptitle(f'Energy Savings for {city_input.upper()} (kWh/tour)')
    plt.savefig('output_adjusted.png', dpi=300)
    plt.show()
    plt.close()
    
    MC_sim_output_DF.to_csv('output_DataFrame.csv', index=False)

    print('Predicted energy savings saved as "output_DataFrame.csv".')

    print('Thanks for running this script. Bye.')

else:
    print('Thanks for running this script. Bye.')