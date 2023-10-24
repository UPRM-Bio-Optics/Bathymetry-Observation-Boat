import os
import csv
import numpy as np
import plotly.express as px
from typing import Any
from datetime import datetime

import seabreeze

seabreeze.use("pyseabreeze")
from seabreeze.spectrometers import Spectrometer


class SpectrometerWrapper:
    wavelengthsBuffer = []
    intensitiesBuffer = []
    device = None

    def __init__(self, serialNumber: int = None):
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

    def reduceNoise(self):
        """Removes duplicates from wavelengths list and condenses them to a single entry with
        the average of the associated intensities;
        Note: Uses current wavelengths and intensities buffer values;

        """
        result: dict = {}
        duplicateCount: float = 1
        sumDuplicates: float = 0
        for i in range(len(self.wavelengthsBuffer)):
            if result.has_key(self.wavelengthsBuffer[i]):
                duplicateCount += 1
                sumDuplicates += self.intensitiesBuffer[i]
                result[self.wavelengthsBuffer[i]] = sumDuplicates / duplicateCount
            else:
                result[self.wavelengthsBuffer[i]] = result[self.intensitiesBuffer[i]]

        self.wavelengthsBuffer, self.intensitiesBuffer = zip(*result.items())

    def fillBuffer(self) -> None:
        """
        Updates buffer with new sample

        """
        self.reduceNoise(self.device.spectrum())

    def plotBuffer(self):
        """
        generates plotly plot using buffered values of wavelengths and intensities
        This graph is simply a sample from the sensor; if a more comprehensive visualization is needed
        use SpectrometerWrapper.plotAll()
        """
        today = datetime.now().strftime("%m/%d/%Y, %H/%M/%S")

        fig = px.line(
            x=self.wavelengthsBuffer,
            y=self.intensitiesBuffer,
            labels={"x": "Wavelength (nm)", "y": "Intensity (a.u)"},
            title="Intensity vs Wavelength Sample",
        )
        fig.show()

        filename = os.getcwd() + "/Data/Spectrometer/plots/" + today + ".png"
        fig.write_image(filename)
        # plt.savefig(os.getcwd() + "/Data/Spectrometer/plots/" + today + ".png")


def spectro():
    spec = Spectrometer.from_first_available()
    spec.integration_time_micros(100000)

    wavelengths, intensities = spec.spectrum()
    wavelengths = np.round(wavelengths)
    intensities = np.round(intensities)

    wavelengths, intensities = reduceNoise(
        wavelengths=wavelengths, intensities=intensities
    )

    today = datetime.now().strftime("%b-%d-%Y")
    csvfile = open(os.getcwd() + "/Data/Spectrometer/csv/" + today + ".csv", "w")
    writer = csv.writer(csvfile)
    _header = ["Wavelengths (nm)", "Intensities (a.u)"]
    writer.writerow(_header)

    for i in range(len(wavelengths)):
        wavelength = wavelengths[i]
        intensity = intensities[i]
        row = [wavelength, intensity]
        writer.writerow(row)


if __name__ == "__main__":
    spectro()
