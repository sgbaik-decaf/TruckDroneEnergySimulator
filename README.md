# TruckDroneEnergySimulator

Repository Manager (Corresponding Author): Seung Gyu Baik

Contact: sgbaik@utexas.edu

# Purpose

This package demonstrates the proposed simulation framework in
"A Simulation Framework for Evaluating Energy Savings of Truck-drone Hybrid Last-mile Delivery in Arbitrary Cities (2025)".

# Disclaimer
This package is designed to be an "add-on" extension to the mFSTSP solver by [Murray & Raj (2020)](https://github.com/optimatorlab/mFSTSP).

This package utilizes the OSMnx package by [Boeing (2025)](https://github.com/gboeing/osmnx).

# How to Install the Demonstrator

## I. Install Dependencies

Install the following dependencies.
  1. [NumPy](https://numpy.org/install/) Suggested version: 1.26.4
  2. [Pandas](https://pandas.pydata.org/docs/getting_started/install.html) Suggested version: 2.2.3
  3. [NetworkX](https://networkx.org/documentation/stable/install.html) Suggested version: 3.3
  4. [OSMnx](https://osmnx.readthedocs.io/en/stable/installation.html) Suggested version: 1.9.4
  5. [mFSTSP solver package](https://github.com/optimatorlab/mFSTSP) (*THE WHOLE THING* including [Gurobi](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python) - Suggested version: 11.0.3)

## II. Download and Unzip Addons

Download this GitHub repository as a .zip file via the big green button that says <p style="color:green"> <> code🔻>. 

`TruckDroneEnergySimulator-main.zip` includes 8 files:
  1. `addon_main.py`
  2. `newmain.py`
  3. `addon_OSMnxGeospatialSimulator.py`
  4. `addon_EnergyConsumptionCalculator.py`
  5. `addon_HaversineFunction.py`
  6. `addon_GreedyGroundTSP.py`
  7. `tbl_vehicles_999.csv`
  8. A folder `myproblem`

## III. Move addons on top of the mFSTSP solver
All items must be moved to specific directories for this package to work correctly.

Navigate to the mFSTSP solver folder you just installed on your machine.

Move the contents of `addons.zip` into appropriate folders.

* Items 1 through 6 should go directly into `\mFSTSP-master`.
* Items 7 and 8 should go into a subfolder `\mFSTSP-master\Problems`.

You are encouraged to make a copy of `\mFSTSP-master` before importing addons (e.g. `\mFSTSP-master-copy`). 

# How to Run Demonstrator
`addon_main.py` is the script that directly interatcts with the users.

1. Open this script with a modern integrated devleopment environment (IDE) like Visual Studio Code or Spyder.
Make sure your IDE is running on `\mFSTSP-master` (or wherever the other files are).
2. Run the script.
3. Define parameters via your console.

## Parameters

There are a few parameters for users to set. Below is an example for you to follow.

Enter parameters directly to your console.

1. City Name
```
Enter a city name. 
(e.g. "Pittsburgh, PA")
>>Kuala Lumpur
```

2. Depot Location
* Note that input text does not have to be a street address, as long as it's a unique OpenStreetMap feature.
```
Enter an address for delivery depot location. 
(e.g. "4800 Forbes Ave, Pittsburgh, PA")
>>KLCC Park Running Track, Lorong Kuda, Kuala Lumpur City Centre (KLCC), Kampung Cendana, Kuala Lumpur, 50088, Malaysia
```

3. Boundary Box Parameter
```
Specify the size of your area of operations in kilometers. 
(Suggested: 5~15)
>>5
```

4. City Center Parameter
```
Specify city center parameter. 
(Suggested: 0.3~0.8)
>>0.5
```

5. Monte Carlo Simulation
```
Set analysis mode. 
[1]: Single Instance Simulation
[2]: Monte Carlo Simulation
>>2
```

6. Number of Simulations (only available in *Monte Carlo Simulation* mode)
```
Set number of simulations to run. 
(Suggested: 50-100)
>>10
```

7. Save Results as a .csv file
```
Save results (energy consumption estimates) as .csv files?
[1]: No
[2]: Yes
>>2
```

8. Save Customer Node Locations and mFSTSP Solution as a .csv file (only available in *Monte Carlo Simulation* mode)
```
Save nodes and solutions of each simulation instance as .csv files? 
[1]: No
[2]: Yes
>>1
```

9. Intermediate UAV sorties & Energy Use Display (only available in *Single Instance Simulation* mode)
```
Display intermediate data?
[1]: No
[2]: Yes
>>1
```



## Results

If everything goes well, you will see a summary statistic of energy consumption estimates on your conole.

You may opt to save the results as a .csv file.

## Testing for a specific drone or truck model

By default, the demonstrator mimics a personal sUAV similar to [DJI Matrice 100](https://www.dji.com/support/product/matrice100) which has been used to build the energy model by [Rodrigues et al. (2022)](https://doi.org/10.1016/j.patter.2022.100569).

Specifications are in `tbl_vehicles_999.csv`.

You can alter the values in this file to test for a specific drone model of your choice.

You can also alter the baseline energy consumption of the ground vehicle (Wh/km) by changing the variable `BaselineInformation` in `addon_main.py`.

# Troubleshooting

## I need help in general.

Please shoot an email to me. I will help.

## Do I need to install libraries of specific versions?

No. However, it is recommended to prevent unforeseen errors.

OSMnx, especially, is under active development and the code syntax may differ significantly between versions.

As of February 2025, newest versions of standard libraries are not expected to cause an error.

## It takes to long.

Yes, you are correct.

This is because the package downloads data from OpenStreetMap API.

In a medium-sized city, the first instance takes around 2 minutes (to build the graph), and the following instances each takes around 1 minute.

## The file size became too large.

This is because all mFSTSP solution data are cached and stored in your working directory.

You may delete those files (i.e. `tbl_solutions_999_3_Heuristic.csv`) as necessary.

## OpenStreetMap and/or OSMnx is not working.

If this is the case, your console will state that it is.

There are 3 common causes you should first check out.

### 1. OSM query input issue

<p style="color:red">The is known to be the most frequent cause of error.</p>

Although the geocoder provided by OSMnx provides some flexibility, a typo in addresses are not automatically fixed.

If you suspect this is the case, and if you are unsure about the address format of a foreign city, it is recommended to check that your address exists as a feature at [OpenStreetMap](https://www.openstreetmap.org/).

Then, using the OpenStreetMap interface:

1. Locate the place you would put a depot.

2. Right click the screen and select "show address" or "query features".

3. Copy the feature name and use that in lieu of street address.

### 2. Internet connection issue

Make sure you are connected to the internet with no restrictions.

Certain public networks (e.g. Dunkin Donuts Guest Wi-Fi) may prohibit retriving information from OpenStreepMap API.

In rare cases, the OpenStreetMap itself may be 'down' at the moment.

### 3. Disconnected node

This happens because OSMnx cannot find a working route between a pair of nodes due to a disconnected graph (road network).

The graph representation of OSMnx don't capture every single detail in the roads, and this occationally result in some nodes being isolated from other nodes.

If you suspect this is the case, you can simply run the script again hoping that newly generated customer nodes are fully connected.

If problem persists, your desired depot location may be isolated from the remaining part of the graph.

If this is the case, adjust your *Boundary Box Range* and make the graph cover a larger area.

In cities with very complex jurisdictions and municipal boundaries, the demonstrator can fail to build a working graph.

It is feasible to set the *city name* to a higher level (i.e. County) to fix this issue, but this will dramatically increase the time it takes to run the package.

As appropriate, you may modify `addon_OSMnxGeospatialSimulator.py`, after consulting [OSMnx documentation](https://osmnx.readthedocs.io/en/stable/).
