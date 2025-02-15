# TruckDroneEnergySimulator

Repository Maintainer (Corresponding Author): Seung Gyu Baik [website](https://sgbaik.notion.site/BAIK-S-ONLINE-REPOSITORY-a47a903af9894120b91fdf0124b75c9f)

Contact: seunggyb@alumni.cmu.edu

Affiliation: Carnegie Mellon University

# Purpose

This package demonstrates the proposed analytic framework in
"Framework for modeling Energy Savings of Truck-drone Hybrid Deliveries in Arbitrary Cities (2025)".

# Disclaimer
This package is designed to be an "add-on" extension to the mFSTSP Solver by [Murray & Raj (2020)](https://github.com/optimatorlab/mFSTSP).

This package utilizes OSMnx by Boeing (2024) which its documentatiob is on [GitHub](https://github.com/gboeing/osmnx).

# How to Install Demonstrator
## I. Install Dependencies
Install the following directories.
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
All items must be moved inro specific directories for this package to work correctly.

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
>>1614 Glenwood Ave
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
