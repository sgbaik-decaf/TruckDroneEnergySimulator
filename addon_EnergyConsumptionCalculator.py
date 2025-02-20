import pandas as pd
import osmnx as ox

def runDroneEnergyModule(sorties, UAV_info):
    # create an indicator whether the parcel is onboard or not
    new_description_column = []
    for row in sorties['Description']:
        if 'UAV' in row:
            new_description_column.append('parcel')
        elif 'truck' in row:
            new_description_column.append('nothing')
        elif 'depot' in row:
            new_description_column.append('nothing')
    sorties['Description'] = pd.Series(new_description_column)
    
    # pre-fitted values from Rodrigues et al
    beta_1_TO = 80.4 # no unit
    beta_0_TO = 13.8 # no unit
    beta_1_CRZ = 68.9 # no unit
    beta_0_CRZ = 16.8 # no unit
    beta_1_LND = 71.5 # no unit
    beta_0_LND = -24.3 # no unit
    dronemass = 2.4 # (kg), assumed
    parcelmass = 0.5 # (kg), assumed
    mass = dronemass + parcelmass
    dronespeed = UAV_info.iloc[-1,3] #(m/s)
    ro = 1.225 # at sea level (kg/m^3)
    
    TO_speed = UAV_info.iloc[-1,2] # takeoff speed (m/s)
    LND_speed = UAV_info.iloc[-1,4] # landing speed (m/s)
    CRZ_alt = UAV_info.iloc[-1,6] # cruise alt (m), usually 50m
    CRZ_speed = dronespeed # cruise speed (m/s)

    sorties['dist_in_m'] = sorties['euclid_dist'] * 1000 # (km) -> (m)

    sorties['total_time'] = sorties['dist_in_m'] / dronespeed # (s)

    TO_time = CRZ_alt/TO_speed # (s)
    sorties['TO_time'] = pd.Series([TO_time for _ in range(len(sorties))]) # (s)
    LND_time = CRZ_alt/LND_speed # (s)
    sorties['LND_time'] = pd.Series([LND_time for _ in range(len(sorties))]) # (s)

    sorties['CRZ_time'] = sorties['total_time'] # (s)
    
    energy_cruise = []
    for i in range(len(sorties['Description'])):
        if sorties['Description'][i] == 'parcel':
            energy_cruise.append((beta_1_CRZ * (mass**1.5 / ro**0.5) + beta_0_CRZ) * sorties['CRZ_time'][i])
        elif sorties['Description'][i] == 'nothing':
            energy_cruise.append((beta_1_CRZ * (dronemass**1.5 / ro**0.5) + beta_0_CRZ) * sorties['CRZ_time'][i])
    sorties['energy_cruise'] = pd.Series(energy_cruise)

    energy_takeoff = []
    for i in range(len(sorties['Description'])):
        if sorties['Description'][i] == 'parcel':
            energy_takeoff.append((beta_1_TO * (mass**1.5 / ro**0.5) + beta_0_TO) * sorties['TO_time'][i])
        elif sorties['Description'][i] == 'nothing':
            energy_takeoff.append((beta_1_TO * (dronemass**1.5 / ro**0.5) + beta_0_TO) * sorties['TO_time'][i])
    sorties['energy_takeoff'] = pd.Series(energy_takeoff)

    energy_land = []
    for i in range(len(sorties['Description'])):
        if sorties['Description'][i] == 'parcel':
            energy_land.append((beta_1_LND * (mass**1.5 / ro**0.5) + beta_0_LND) * sorties['LND_time'][i])
        elif sorties['Description'][i] == 'nothing':
            energy_land.append((beta_1_LND * (dronemass**1.5 / ro**0.5) + beta_0_LND) * sorties['LND_time'][i])
    sorties['energy_land'] = pd.Series(energy_land)

    sorties['energy_use(Wh)'] = (
        sorties['energy_takeoff']
        + sorties['energy_cruise']
        + sorties['energy_land']
        )/3600 # total energy consumption from J to Wh

    sorties.drop(columns = [
        'energy_takeoff',
        'energy_cruise',
        'energy_land',
        'euclid_dist',
        'TO_time',
        'LND_time'], inplace = True)
    
    sorties = sorties.round(2)

    UAV_energy_DF = sorties
    return UAV_energy_DF


def runTruckEnergyModule(truck_tour, matrix_DF_copy, BaselineInformation):
    truck_tour_with_dist = pd.merge(truck_tour, matrix_DF_copy, on=['startNode', 'endNode'])

    truck_tour_with_dist['energy(Wh, Diesel Truck)'] = BaselineInformation['Diesel Truck'] * truck_tour_with_dist['dist(m)'] / 1000
    truck_tour_with_dist['energy(Wh, EV Truck)'] = BaselineInformation['EV Truck'] * truck_tour_with_dist['dist(m)'] / 1000
    truck_tour_with_dist['energy(Wh, EV Van)'] = BaselineInformation['EV Van'] * truck_tour_with_dist['dist(m)'] / 1000
    truck_tour_with_dist.drop(columns = ['Description', 'time(s)'], inplace = True)

    Ground_energy_DF = truck_tour_with_dist
    return Ground_energy_DF

# Diesel truck depot to door = 4.29 kWh/mi = 2665.69 Wh/km (DoE 2020)
# EV truck depot to door = 1 kWh/mi = 621.37 Wh/km (DoE 2020)
# EV van depot to door = 0.56 kWh/mi = 347.97 Wh/km (DoE 2020)









