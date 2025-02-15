# TruckDroneEnergySimulator

Repository Maintainer (Corresponding Author): Seung Gyu Baik [https://sgbaik.notion.site/BAIK-S-ONLINE-REPOSITORY-a47a903af9894120b91fdf0124b75c9f](website)

Contact: seunggyb@alumni.cmu.edu

Affiliation: Carnegie Mellon University

# Purpose

This package demonstrates the proposed analytic framework in
"Framework for modeling Energy Savings of Truck-drone Hybrid Deliveries in Arbitrary Cities (2025)".

# Disclaimer
This package is designed to be an "add-on" extension to the mFSTSP Solver.

The original source code by Murray & Raj (2020) is on [GitHub](https://github.com/optimatorlab/mFSTSP).

This package utilizes OSMnx by Boeing (2024) which its documentatiob is on [GitHub](https://github.com/gboeing/osmnx).

# How to run the Demonstrator Package
## Install Dependencies
Install the following directories.
1. [NumPy](https://numpy.org/install/) Suggested version: 1.26.4
2. [Pandas](https://pandas.pydata.org/docs/getting_started/install.html) Suggested version: 2.2.3
3. [NetworkX](https://networkx.org/documentation/stable/install.html) Suggested version: 3.3
4. [OSMnx](https://osmnx.readthedocs.io/en/stable/installation.html) Suggested version: 1.9.4
5. [Matplotlib](https://matplotlib.org/stable/install/index.html)
6. [Seaborn](https://seaborn.pydata.org/installing.html)
7. MFSTSP SOLVER PACKAGE (THE WHOLE THING including [Gurobi](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python))

## Download and extract addons.zip
1. "addon_main.py"
2. "addon_OSMnxGeospatialSimulator.py"
3. "addon_EnergyConsumptionCalculator.py",
4. "addon_HaversineFunction.py"
5. "addon_GreedyGroundTSP.py"

## Move addons on top of the mFSTSP solver
