
import matplotlib.pyplot as plt
import numpy as np

from uncertainties import ufloat, unumpy
import pandas as pd
import os
import sys
# define class Messwerte


class Messwerte:
    x_werte = ""
    y_werte = ""
    x_name = ""
    y_name = ""

    def __init__(self, x_werte,x_err, y_werte, y_err, x_name,y_name) -> None:
    
        """constructor for an Werte Object
        :param x_werte: x values
        :param y_werte: y values
        :param x_err: error on x values
        :param y_err: error onmv values
        :param x_name: name of x values
        :param y_name: name of y values"""
       
        self.x_werte = unumpy.uarray(x_werte,x_err)
        self.y_werte = unumpy.uarray(y_werte,y_err)
        self.x_name = x_name
        self.y_name = y_name
    def to_csv(self,path_to_File):
        """
        to_csv converts the x and y values to a csv File
        :param self: Werte Object with the used x and y values
        :param path_to_File: String without the fileextention, where the file should be stored 
        :return: nothing
        """
        p = pd.DataFrame({self.x_name:self.x_werte,self.y_name:self.y_werte})
        p.to_csv(f"{path_to_File}.csv", index=False, float_format='%6.3E', sep=';', decimal=',')
        print(f"Saved in {path_to_File}")

    def __str__(self) -> str:
        str = f"{self.x_name}:\n {self.x_werte} \n {self.y_name}:\n {self.y_werte}"
        return str

    def errorbars(self,label, title, save=True):
        fig, ax = plt.subplots()
        ax.errorbar( unumpy.nominal_values(self.x_werte) , unumpy.nominal_values(self.y_werte), yerr=unumpy.std_devs(self.y_werte), xerr=unumpy.std_devs(self.x_werte), marker='', linestyle=' ', capsize=2, label=label)
        ax.set_title(title)
        ax.set_xlabel(self.x_name)
        ax.set_ylabel(self.y_name)
        ax.legend()
        if save == True:
            plt.savefig(f"{title}.pdf")
        


        

