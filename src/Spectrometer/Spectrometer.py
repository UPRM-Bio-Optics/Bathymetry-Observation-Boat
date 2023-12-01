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


class SpectrometerWrapper:
    wavelengthsBuffer = []
    intensitiesBuffer = []

    device = None
    outputFile = None
    writer = None

    def __init__(self, serialNumber: int = None) -> None:
        """
        Initialize spectrometer object class; This is a wrapper to the
        PySeaBreeze Spectrometer class to include several methods such as noise reduction
        Data correction from other spectrometer data

        Args:
            serialNumber (int, optional): if initializing spectrometer from serial number instead of through from first availvable . Defaults to None.
        """
        if serialNumber:
            self.device = Spectrometer.from_serial_number(serialNumber)
        else:
            self.device = Spectrometer.from_first_available()

        self.device.integration_time_micros(100000)

        self.today = datetime.now().strftime("%m-%d-%Y")
        self.outputFile = open(
            os.getcwd() + "/Data/Spectrometer/csv/" + self.today + ".csv", "w"
        )
        self.writer = csv.writer(self.outputFile)
        _header = ["Wavelengths (nm)", "Intensities (a.u)"]
        self.writer.writerow(_header)

    def reduceNoise(self) -> None:
        """Removes duplicate intensities values from wavelengths list and condenses them to a single entry with
        the average of the associated intensities for a given wavelength;
        Note: Uses current wavelengths and intensities buffer values;

        """
        result: dict = {}
        duplicateSum = 0
        duplicateCount = 0
        for i in range(len(self.wavelengthsBuffer) - 1):
            duplicateCount += 1
            duplicateSum += self.intensitiesBuffer[i]
            if self.wavelengthsBuffer[i] != self.wavelengthsBuffer[i + 1]:
                result[self.wavelengthsBuffer[i]] += duplicateSum / duplicateCount

                duplicateCount = 0
                duplicateSum = 0

        self.wavelengthsBuffer, self.intensitiesBuffer = zip(*result.items())

    def fillBuffer(self) -> None:
        """
        Updates buffer with new sample

        """
        self.wavelengthsBuffer, self.intensitiesBuffer = self.device.spectrum()
        self.reduceNoise()

    def plotBuffer(self) -> None:
        """
        generates plotly plot using buffered values of wavelengths and intensities
        This graph is simply a sample from the sensor; if a more comprehensive visualization is needed
        use SpectrometerWrapper.plotAll()
        """

        fig = px.line(
            x=self.wavelengthsBuffer,
            y=self.intensitiesBuffer,
            labels={"x": "Wavelength (nm)", "y": "Intensity (a.u)"},
            title="Intensity vs Wavelength Sample",
        )
        fig.show()

        filename = os.getcwd() + "/Data/Spectrometer/plots/" + self.today + ".png"
        fig.write_image(filename)
        # plt.savefig(os.getcwd() + "/Data/Spectrometer/plots/" + today + ".png")

    @staticmethod
    def plot(csvpath: str):
        df = pd.read_csv(csvpath)
        fig = px.line(
            data_frame=df,
            labels={"x": "Wavelength (nm)", "y": "Intensity (a.u)"},
            title="Intensity vs Wavelength",
        )


def spectro():
    spec = SpectrometerWrapper()
    spec.fillBuffer()
    spec.plotBuffer()


if __name__ == "__main__":
    spectro()
