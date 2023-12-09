import os
import csv
import numpy as np
import plotly.express as px
import pandas as pd
from typing import Any
from datetime import datetime

import seabreeze

seabreeze.use("pyseabreeze")
from seabreeze.spectrometers import Spectrometer


class SpectrometerSystem:
    #wavelength key, intensity value
    skySpectrum = {}
    #wavelength key, intensity value
    seaSpectrum = {}
    #wavelength key, reflectance value
    reflectance = {}
    

    def __init__(self, skySerialNumber: int = None, seaSerialNumber: int = None) -> None:
        """
        Initialize spectrometer object class; This is a wrapper to the
        PySeaBreeze Spectrometer class to include several methods such as noise reduction
        Data correction from other spectrometer data

        Args:
            serialNumber (int, optional): if initializing spectrometer from serial number instead of through from first availvable . Defaults to None.
        """
        if skySerialNumber:
            self.device = Spectrometer.from_serial_number(skySerialNumber)
        else:
            self.skySpectrometer = Spectrometer.from_first_available()
        
        if seaSerialNumber:
            self.device = Spectrometer.from_serial_number(seaSerialNumber)
        else:
            self.seaSpectrometer = Spectrometer.from_first_available()


        self.skySpectrometer.integration_time_micros(100000)
        self.seaSpectrometer.integration_time_micros(100000)
        

        self.today = datetime.now().strftime("%m-%d-%Y")
        self.outputFile = open(
            os.getcwd() + "/Data/Spectrometer/csv/" + self.today + ".csv", "w"
        )
        self.writer = csv.writer(self.outputFile)
        _header = ["Wavelengths (nm)", "Intensities (a.u)"]
        self.writer.writerow(_header)

    def reduceNoise(self, wavelengthsBuffer, intensitiesBuffer) -> None:
        """Removes duplicate intensities values from wavelengths list and condenses them to a single entry with
        the average of the associated intensities for a given wavelength;
        Note: Uses current wavelengths and intensities buffer values;

        """
        result: dict = {}
        duplicateSum = 0
        duplicateCount = 0
        for i in range(len(wavelengthsBuffer) - 1):
            duplicateCount += 1
            duplicateSum += intensitiesBuffer[i]
            if wavelengthsBuffer[i] != self.wavelengthsBuffer[i + 1]:
                result[wavelengthsBuffer[i]] += duplicateSum / duplicateCount

                duplicateCount = 0
                duplicateSum = 0

        return result

    def fillBuffer(self) -> None:
        """
        Updates spectrum buffer with new sample

        """
        wavelengthsBuffer, intensitiesBuffer = self.skySpectrometer.spectrum()
        self.skySpectrum = self.reduceNoise(wavelengthsBuffer, intensitiesBuffer)
        
        wavelengthsBuffer, intensitiesBuffer = self.seaSpectrometer.spectrum()
        self.seaSpectrum = self.reduceNoise(wavelengthsBuffer, intensitiesBuffer)
        
        

    def plotBuffer(self) -> None:
        """
        generates plotly plot using buffered values of wavelengths and intensities
        This graph is simply a sample from the sensor; if a more comprehensive visualization is needed
        use SpectrometerWrapper.plotAll()
        """

        fig = px.line(
            self.reflectance,
            labels={"x": "Wavelength (nm)", "y": "Intensity (a.u)"},
            title="Intensity vs Wavelength Sample",
        )
        fig.show()

        filename = os.getcwd() + "/Data/Spectrometer/plots/" + self.today + ".png"
        fig.write_image(filename)
        # plt.savefig(os.getcwd() + "/Data/Spectrometer/plots/" + today + ".png")


    def calculateReflectance(self) -> None:
        
        """
        Calculates reflectance based on the intensity data measured by each spectrometer. divinging the below intensity over the light
        """
        
        for wavelength in self.skySpectrum.keys():
            
            self.reflectance[wavelength] = self.seaSpectrum[wavelength] / self.skySpectrum[wavelength]
        
        


def plot(csvpath: str):
    """
    Plot Reflectance vs wavelength using data from csv

    Args:
        csvpath (str): file path to csv
    """
    df = pd.read_csv(csvpath)
    fig = px.line(
        data_frame=df,
        labels={"x": "Wavelength (nm)", "y": "Intensity (a.u)"},
        title="Intensity vs Wavelength",
    )


def spectro():
    spec = SpectrometerSystem()
    spec.fillBuffer()
    spec.plotBuffer()


if __name__ == "__main__":
    spectro()
