# Graph Utility for Echo Sounder Data

## Overview
This Python module provides utility functions for visualizing depth data collected by an echo sounder. It utilizes the Plotly and Matplotlib libraries to generate 2D and 3D contour plots, as well as a map overlay with depth information.

## Features
- **2D Contour Plot:** Visualizes depth data in a 2D contour plot.
- **3D Contour Plot:** Generates a 3D contour plot of the depth data.
- **Map Overlay:** Creates a heatmap overlay on a map with depth information.

## Requirements
- NumPy: Install using `pip install numpy`.
- Matplotlib: Install using `pip install matplotlib`.
- Pandas: Install using `pip install pandas`.
- Plotly: Install using `pip install plotly`.
- os: Standard library module.
- datetime: Standard library module.
- scipy: Install using `pip install scipy`.

## Usage
1. Import the `graphs.py` module into your main script or Jupyter notebook.
2. Call the desired function with the path to the CSV file containing depth data.
   ```py
   from utils.graphs import plotlyGraph, MapOverlay

   csvpath = "path/to/your/data.csv"

   # Generate 2D and 3D contour plots
   plotlyGraph(csvpath)

   # Create a map overlay with depth information
   MapOverlay(csvpath)
   ```

## Output

- 2D Plots are stored in `/Data/Graphs/{date}TowDMap.png`
- 3D Plots are stored in `/Data/Graphs/{date}ThreeDMap.png`
- Map overlay maps are stored in `/Data/Graphs/{date}MapOverlay.png`
   