# https://github.com/sgbaik-decaf/TruckDroneEnergySimulator

# Author:      Baik, Seung Gyu
# Contact:     sgbaik@utexas.edu

#_________________________[DISCLAIMER]_______________________

# This package is designed to be an "add-on" extension to the mFSTSP Solver by Murray & Raj (2020)
# https://github.com/optimatorlab/mFSTSP

#________________[DEPENDENCIES FOR THIS PROGRAM]_____________
# 1. Numpy         https://numpy.org/install/
# 2. Pandas        https://pandas.pydata.org/docs/getting_started/install.html
# 3. NetworkX      https://networkx.org/documentation/stable/install.html
# 4. OSMnx         https://osmnx.readthedocs.io/en/stable/installation.html
# 5. mFSTSP solver package (THE WHOLE THING including GUROBIPY)
# "addon_OSMnxGeospatialSimulator.py",
# "addon_EnergyConsumptionCalculator.py",
# "addon_HaversineFunction.py",
# "addon_GreedyGroundTSP.py"
# "newmain.py"

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

print('\nEnter a city name. \n(e.g. "Pittsburgh, PA")')
city_input = input('>>')

print('\nEnter an address for delivery depot location. \n(e.g. "4800 Forbes Ave, Pittsburgh, PA")')
depot_input = input('>>')

print('\nSpecify the size of your area of operations in kilometers. \n(Suggested: 5~15)')
bbox_range = int(input('>>'))

print('\nSpecify city center parameter. \n(Suggested: 0.3~0.8)')
CityCenterParam = float(input('>>'))

print('\nSet analysis mode. \n[1]: Single Instance Simulation\n[2]: Monte Carlo Simulation')
MonteCarloIndicator = int(input('>>'))-1

if MonteCarloIndicator == 1:
    print('\nSet number of simulations to run. \n(Suggested: 50-100)')
    MonteCarloInstances = int(input('>>'))
    print('\nSave results (energy consumption estimates) as .csv files?\n[1]: No\n[2]: Yes')
    SaveEnergyUseResults = int(input('>>'))-1
    print('\nSave nodes and solutions of each simulation instance as .csv files? \n[1]: No\n[2]: Yes')
    SaveCSV = bool(int(input('>>'))-1)

elif MonteCarloIndicator == 0:
    MonteCarloInstances = 1
    print('\nSave results (energy consumption estimates) as .csv files?\n[1]: No\n[2]: Yes')
    SaveEnergyUseResults = int(input('>>'))-1
    print('\nDisplay intermediate data? \n[1]: No\n[2]: Yes')
    DisplayIntermediateDataFrame = bool(int(input('>>'))-1)
    SaveCSV = False

# ENERGY INTENSITY VALUES (US DOE 2020, depot to door delivery scenario)
# Class 6 Diesel Truck: 4.29 kWh/mi = 2665.69 Wh/km
# Class 6 EV Truck: 1 kWh/mi = 621.37 Wh/km
# EV Van: 0.56 kWh/mi = 347.97 Wh/km

BaselineInformation = {'Diesel Truck':2665.69, 'EV Truck':621.37, 'EV Van':347.97}



#____________________________________________________________
# Initiate simulation

start_time = time.time()

print('_' * os.get_terminal_size().columns)

BaselineEnergyConsumption_DieselTruck = []
BaselineEnergyConsumption_ElecTruck = []
BaselineEnergyConsumption_ElecVan = []
HybridEnergyConsumption_DieselTruck = []
HybridEnergyConsumption_ElecTruck = []
HybridEnergyConsumption_ElecVan = []

GeneratedNodes = []

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
            ox.plot.plot_graph(G, node_size=0.5)
            matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
            print('Customer Batch & Travel Matrix Generated')
        except:
            try:
                print('[ WARNING ] OpenStreetMap and/or OSMnx is not working as expected.\nThe program will try executing one last time.')
                city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini = BuildBoxGraph(city_input, depot_input, bbox_range, CityCenterParam)
                print(f'Graph Representation for "{city}" Generated')
                ox.plot.plot_graph(G, node_size=0.5)
                matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
                print('Customer Batch & Travel Matrix Generated')
            except:
                sys.exit('[ EXCEPTION ] There was an error with OpenStreetMap and/or OSMnx. Common causes are: \n(1) OSM query input issue \n(2) Internet connection issue \n(3) Disconnected node')
    elif iterationno >= 1:
        try:
            matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
        except:
            try:
                matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
            except:
                try:
                    print('[ WARNING ] OpenStreetMap and/or OSMnx is not working as expected.\nThe program will try executing one last time.')
                    matrix_DF_copy = SimulateCustomers(city,depot_xy,G,Gp,Gp_cust,Gp_cust_mini)
                except:
                    warnings.warn('[ EXCEPTION ] There was an error with OpenStreetMap and/or OSMnx. The program reiterate previous instance.')


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
        
    if SaveCSV == True:
        a.to_csv(f'Simulation_Instances_CSV/Customer_Nodes{iterationno}.csv')
        b.to_csv(f'Simulation_Instances_CSV/mFSTSP_Solution{iterationno}.csv')



    #____________________________________________________________
    # MODULE III: ENERGY USE CALCULATOR

    UAV_energy_DF = runDroneEnergyModule(sorties, UAV_info)
    Ground_energy_DF = runTruckEnergyModule(truck_tour, matrix_DF_copy, BaselineInformation)
    UAV_energy_sum = round(UAV_energy_DF['energy_use(Wh)'].sum(), 4)
    Truck_energy_sum = round(Ground_energy_DF['energy(Wh, Diesel Truck)'].sum(), 4)
    EVTruck_energy_sum = round(Ground_energy_DF['energy(Wh, EV Truck)'].sum(), 4)
    EVVan_energy_sum = round(Ground_energy_DF['energy(Wh, EV Van)'].sum(), 4)
    
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
    # Complete this simulation instance and record its result
    
    BaselineEnergyConsumption_DieselTruck.append(
        round(
            baseline_tsp_DF['energy(Wh, Diesel Truck)'][0]
            /1000,
            4)
        )
    HybridEnergyConsumption_DieselTruck.append(
        round(
            (UAV_energy_sum + Truck_energy_sum)
            /1000,
            4)
        )
    
    BaselineEnergyConsumption_ElecTruck.append(
        round(
            baseline_tsp_DF['energy(Wh, EV Truck)'][0]
            /1000,
            4)
        )
    HybridEnergyConsumption_ElecTruck.append(
        round(
            (UAV_energy_sum + EVTruck_energy_sum)
            /1000,
            4)
        )
    
    BaselineEnergyConsumption_ElecVan.append(
        round(
            baseline_tsp_DF['energy(Wh, EV Van)'][0]
            /1000,
            4)
        )
    HybridEnergyConsumption_ElecVan.append(
        round(
            (UAV_energy_sum + EVVan_energy_sum)
            /1000,
            4)
        )
    
    int_end_time = time.time()
    int_time = round(int_end_time - int_start_time, 2)
    print(f"Baseline(Diesel Truck): {round(baseline_tsp_DF['energy(Wh, Diesel Truck)'][0]/1000,4)} kWh")
    print(f"Truck-Drone Hybrid(Diesel Truck): {round((UAV_energy_sum + Truck_energy_sum)/1000,4)} kWh")
    print('Simulation Result Noted')
    print(f'Instance #{iterationno+1} took {int_time} seconds\n')



#____________________________________________________________
# Display Simulation Result

if MonteCarloIndicator == 0 and DisplayIntermediateDataFrame == True:
    print('_' * os.get_terminal_size().columns)
    print('[LAST MILE DILIVERY TOUR SOLUTION]')
    print(UAV_energy_DF)

print('_' * os.get_terminal_size().columns)
print('[RESULT]')

end_time = time.time()
print("\nTotal elapsed time: ",round(end_time-start_time, 2), "seconds")

print('\nEnergy consumptions of Hybrid Delivery and Conventional Delivery Baseline - Diesel Truck (kWh):')
print('BASELINE:', round(np.average(BaselineEnergyConsumption_DieselTruck), 4))
print('HYBRID:', round(np.average(HybridEnergyConsumption_DieselTruck), 4))

print('\nEnergy consumptions of Hybrid Delivery and Conventional Delivery Baseline - EV Truck (kWh):')
print('BASELINE:', round(np.average(BaselineEnergyConsumption_ElecTruck), 4))
print('HYBRID:', round(np.average(HybridEnergyConsumption_ElecTruck), 4))

print('\nEnergy consumptions of Hybrid Delivery and Conventional Delivery Baseline - EV Van (kWh):')
print('BASELINE:', round(np.average(BaselineEnergyConsumption_ElecVan), 4))
print('HYBRID:', round(np.average(HybridEnergyConsumption_ElecVan), 4))


#____________________________________________________________
# Save Simulation Result



if SaveEnergyUseResults == 1:
    MC_sim_output_DF = pd.DataFrame(
        {
            'Baseline (Diesel Truck)' : BaselineEnergyConsumption_DieselTruck,
            'Hybrid (Diesel Truck)' : HybridEnergyConsumption_DieselTruck,
            'Baseline (EV Truck)' : BaselineEnergyConsumption_ElecTruck,
            'Hybrid (EV Truck)' : HybridEnergyConsumption_ElecTruck,
            'Baseline (EV Van)' : BaselineEnergyConsumption_ElecVan,
            'Hybrid (EV Van)' : HybridEnergyConsumption_ElecVan
        }
    ) 
    
    MC_sim_output_DF.to_csv('Results/output_DataFrame.csv', index=False)

    print('Predicted energy consumption saved as "Results/output_DataFrame.csv".')

    print('Thanks for running this script. Bye.')

else:
    print('Thanks for running this script. Bye.')
