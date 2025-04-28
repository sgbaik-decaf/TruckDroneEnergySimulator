# TruckDroneEnergySimulator

Repository Maintenance Manager (Corresponding Author): Seung Gyu Baik (Call me Baik if too long.)

Contact: sgbaik@utexas.edu / seunggyb@alumni.cmu.edu

# Purpose

This package demonstrates the proposed analytic framework in
"Framework for modeling Energy Savings of Truck-drone Hybrid Deliveries in Arbitrary Cities (2025)".

# Disclaimer
This package is designed to be an "add-on" extension to the mFSTSP Solver by [Murray & Raj (2020)](https://github.com/optimatorlab/mFSTSP).

This package utilizes OSMnx by [Boeing (2024)](https://github.com/gboeing/osmnx).

# How to Install the Demonstrator

## I. Install Dependencies

Install the following dependencies.
  1. [NumPy](https://numpy.org/install/) Suggested version: 1.26.4
  2. [Pandas](https://pandas.pydata.org/docs/getting_started/install.html) Suggested version: 2.2.3
  3. [NetworkX](https://networkx.org/documentation/stable/install.html) Suggested version: 3.3
  4. [OSMnx](https://osmnx.readthedocs.io/en/stable/installation.html) Suggested version: 1.9.4
  5. [Matplotlib](https://matplotlib.org/stable/install/index.html)
  6. [Seaborn](https://seaborn.pydata.org/installing.html)
  7. [mFSTSP solver package](https://github.com/optimatorlab/mFSTSP) (*THE WHOLE THING* including [Gurobi](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python) - Suggested version: 11.0.3)

## II. Download and Unzip Addons
`addons.zip` includes 8 files:
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
Enter a city name and state name to analyze
(e.g. "Pittsburgh, PA")
>>Raleigh, NC
```

2. Depot Location
```
Enter an address for delivery depot location 
(e.g. "1723 Murray Ave, Pittsburgh, PA")
>>11 W Jones St, Raleigh, NC
```

3. Boundary Box Range
```
Specify the size of you area of operations in km 
(Suggested: 5~15)
>>7
```

4. Monte Carlo Simulation
```
Set analysis mode
[1]: Single Instance Simulation
[2]: Monte Carlo Simulation
>>1
```

5. City Center Parameter
```
Specify city center parameter in & 
(Suggested: 0.3~0.7)
>>0.5
```

6. Intermediate UAV sorties & Energy Use Display (only available in *Single Instance Simulation* mode)
```
Display intermediate data?
[1]: No
[2]: Yes
>>2
```

7. Number of Simulations (only available in *Monte Carlo Simulation* mode)
```
Set number of simulations to run 
(Suggested: 30-100)
>>50
```

## Results

If everything goes well, you will see a summary statistic of potential energy savings on your conole.

You may opt to save the results as a .csv file.

## Testing for a specific drone or truck model

By default, the demonstrator mimics a personal sUAV.

Specifications are in `tbl_vehicles_999.csv`.

You can alter the numbers in this file to test for a specific drone model of your choice.

You can also alter the baseline energy consumption of the ground vehicle (Wh/km) by changing the parameters in `addon_main.py`.

# Troubleshooting

## I need help in general.

Please shoot an email to seunggyb@alumni.cmu.edu and describe what is happening.

## Do I need to install libraries of specific versions?

No. However, it is recommended to do so to prevent unforeseen errors.

OSMnx, especially, is under active development and the code syntax may differ significantly between versions.

As of February 2025, newest versions of standard libraries are not expected to cause an error.

## It takes to long.

Yes, you are correct.

This is because the package downloads data from OpenStreetMap API.

In a medium-sized city, the initial instance lasts around 2 minutes (to build the graph), and the following instances each last around 1 minute.

Graphs are cached in the folder to slightly expedite the next simulation.

## The file size became too large.

This is because graphs and mFSTSP results are cached and/or stored somewhere in your working directory.

You may delete those files (i.e. `tbl_solutions_999_3_Heuristic.csv`).

## OpenStreetMap and/or OSMnx is not working

If this is the case, your console will state that this is the case.

There are 3 common causes you should first check out.

### 1. Internet connection issue

Make sure you are connected to the internet with no restrictions.

Certain public wi-fi environments (e.g. Dunkin Donuts) may prohibit retriving information from the OpenStreepMap API.

In rare cases, the OpenStreetMap itself may be 'down' at the moment.

### 2. Typo in query

Although the geocoder provided by OSMnx provides some flexibility, a typo in addresses are not automatically fixed.

### 3. Disconnected node

<p style="color:red">The is known to be the most frequent cause of error.</p>

This happens because OSMnx cannot find a working route between a pair of nodes due to a disconnected graph (road network).

It is understood that the graph representation of OSMnx cannot capture every single detail in the roads, and this occationally result in some nodes being isolated from other nodes.

Unless you modify `addon_OSMnxGeospatialSimulator.py` with expert knowledge in the both the library and the actual city, you can simply run the script again hoping newly generated customer nodes to be fully connected.

You may adjust the *City Center Parameter* to increase customer generation in the city center, where the road network is more 'square'.

If problem persists, your desired depot location may be located outside of the graph.

If this is the case, adjust your *Boundary Box Range*

In cities with very complex jurisdictions and municipal boundaries, the demonstrator can fail to build a working graph.

It is feasible to set the *city name* to a higher level (i.e. County) to fix this issue, but this will dramatically increase the time it takes to run the package.
