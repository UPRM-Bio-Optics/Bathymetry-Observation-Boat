# Spectrometer Data Analysis Tool
## Overview

#### This Python script provides a simple yet effective tool for working with spectrometer data. It utilizes the PySeaBreeze library for interfacing with spectrometers, and Plotly Express for generating interactive plots.

## Features

- SpectrometerWrapper Class: This class serves as a wrapper for PySeaBreeze's Spectrometer class, offering additional functionalities for noise reduction and data visualization.
- Noise Reduction: The script includes a method (reduceNoise) to remove duplicate intensity values associated with the same wavelength, condensing them into a single entry with the average intensity.
- Data Collection: The script can fetch a spectrum from the spectrometer and update a buffer with the wavelength and intensity values.
- Plotting: The tool can generate a Plotly Express line plot using the buffered wavelength and intensity values. The plot is saved both as an interactive display and as a PNG file.

## Usage

Spectrometer Initialization:
Create an instance of the SpectrometerWrapper class.
The spectrometer can be initialized either by specifying a serial number or using the first available device.



```py 
spec = SpectrometerWrapper()  # Initialize with the first available spectrometer

# OR
spec = SpectrometerWrapper(serialNumber=12345)  # Initialize with a specific serial number
```
## Data Collection:
Use the fillBuffer method to update the buffer with a new sample from the spectrometer.

```py


spec.fillBuffer()
```

Plotting:
Use the plotBuffer method to generate and display a plot based on the buffered data.



```py
spec.plotBuffer()
```
Additional Functionality:
The script includes a static method plot that can be used to generate plots from existing CSV files. This can be useful for analyzing previously collected data.

```py
SpectrometerWrapper.plot('path/to/your/data.csv')
```



## File Organization

Data/Spectrometer/csv: This directory contains CSV files where spectrometer data is saved.
Data/Spectrometer/plots: This directory stores PNG files of the generated plots.

## Requirements

- Python 3.x
- PySeaBreeze
- Plotly Express
- Pandas


## TO-DO 

- use other spectrometer to divide data to obtain reflectance
- plot reflectance over wavelength
- first derivative of curve and analysis of data
