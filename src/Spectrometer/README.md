# Spectrometer Data Analysis Tool
## Overview

#### This Python script provides a simple yet effective tool for working with spectrometer data. It utilizes the PySeaBreeze library for interfacing with spectrometers, and Plotly Express for generating interactive plots.

## Features

- SpectrometerSystem Class: This class serves as a wrapper for PySeaBreeze's Spectrometer class, offering additional functionalities for noise reduction and data visualization.
- Noise Reduction: The script includes a method (reduceNoise) to remove duplicate intensity values associated with the same wavelength, condensing them into a single entry with the average intensity.
- Data Collection: The script can fetch a spectrum from the spectrometer and update a buffer with the wavelength and intensity values.
- Plotting: The tool can generate a Plotly Express line plot using the buffered wavelength and intensity values. The plot is saved both as an interactive display and as a PNG file.

## Usage

Spectrometer Initialization:
Create an instance of the SpectrometerSystem class.
The spectrometer can be initialized either by specifying a serial number or using the first available device.

This class takes into account both spectrometers necessary for study. It contain two spectrum attributes buffers which store the latest measure from each spectrometer called skySpectrum and seaSpectrum respectively. These are dictionaries that have wavelengths as keys and measured intensities as values. 

The class also calculates reflectance from the latest sample internally with automatically each time the buffer is filled.




```py 
spec = SpectrometerSystem()  # Initialize with the first available spectrometer

# OR
spec = SpectrometerSystem(skySerialNumber=12345,  seaSerialNumber=12346)  # Initialize with a specific serial number
```
## Data Collection
Use the fillBuffer method to update the buffer with a new sample from both spectrometers.This function fills the spectrum attributes of each spectrometer and calculates the reflectance for each wavelength measurement.



```py


spec.fillBuffer()

print(spec.skySpectrum)
print(spec.seaSpectrum)
print(spec.reflectance)
```

Each time the fillBuffer function is called, the sample is appended to a csv that stores the wavelength, skyIntensity, seaIntensity, and timestamp. Alternatively you can manually append the buffered data to the csv using the following mehtod:

```py

spec.appendToCSV()

```
## Plotting Data
Plotting:
Use the plotBuffer method to generate and display a plot based on the buffered data.



```py
spec.plotBuffer()
```
Additional Functionality:
The script includes a static method plot that can be used to generate plots from existing CSV files. This can be useful for analyzing previously collected data. The data stored 

```py
SpectrometerSystem.plot('path/to/your/data.csv')
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

- First derivative of reflectance curve and analysis of data
- Determine wavelength range of interest for specific object detection such as sargassum or specific algae
