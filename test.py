
import matplotlib.pyplot as plt
import numpy as np

from uncertainties import ufloat,unumpy
import pandas as pd
import os
import sys
import Plottingtools

# einlesen Fadenstrahlrohr versuch
data = np.genfromtxt("232.3.1.csv", delimiter=";", skip_header=1)
# data slicing
widerstand = data[:, 0]
spannung = data[:, 1]
strom = data[:, 2]
strom_err = np.full(10, 0.5)
strom_with_err = unumpy.uarray(strom,strom_err)
spannung_with_err = unumpy.uarray(spannung,strom_err)
test = Plottingtools.Messwerte(strom,strom_err,spannung,strom_err,"Strom", "Spannung")
print(test)
test.errorbars("Spannung","UI-Diagramm")