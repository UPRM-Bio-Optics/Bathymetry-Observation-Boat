import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from typing import Any
from datetime import datetime

import seabreeze

seabreeze.use("pyseabreeze")
from seabreeze.spectrometers import Spectrometer


def reduceNoise(
    wavelengths: list, intensities: list
) -> tuple[list[Any], list[float | Any]]:
    """Removes duplicates from wavelengths list and condenses them to a single entry with
    the average of the associated intensities

    Args:
        wavelengths (list): list of wavelengths spectrum
        intensities (list): list of intensities spectrum
    Returns:
        wavelengths (list): list of wavelengths spectrum with unique entries
        intensities (list): list of intensities spectrum with unique entries
    """
    data = {}
    sum = 0
    sumflag = False
    count = 1
    for i in range(len(wavelengths)):
        if wavelengths[i] in data:
            sum += intensities[i]
            sumflag = True
            count += 1
        elif sumflag:
            data[wavelengths[i - 1]] = sum / count
            sumflag = False
            count = 1
            data[wavelengths[i]] = intensities[i]
            sum = intensities[i]
        else:
            data[wavelengths[i]] = intensities[i]
            sum = intensities[i]

    return list(data.keys()), list(data.values())


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

    plt.figure()
    plt.xlabel("Wavelengths(nm)")
    plt.ylabel("Intensities(a.u)")
    plt.title("Spectrometer Data")
    plt.plot(wavelengths, intensities, "-m")
    plt.savefig(os.getcwd() + "/Data/Spectrometer/plots/" + today + ".png")


if __name__ == "__main__":
    spectro()
