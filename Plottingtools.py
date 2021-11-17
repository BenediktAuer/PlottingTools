
from typing import Iterable, NewType, TypeVar
import matplotlib.pyplot as plt
import numpy as np
from kafe2 import ContoursProfiler, Fit, Plot, XYContainer, fit
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
    label =""

    def __init__(self, x_werte,x_err, y_werte, y_err, x_name,y_name,label) -> None:
    
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
        self.label = label
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

    def errorbars(self, title, save=True):
        fig, ax = plt.subplots()
        ax.errorbar( unumpy.nominal_values(self.x_werte) , unumpy.nominal_values(self.y_werte), yerr=unumpy.std_devs(self.y_werte), xerr=unumpy.std_devs(self.x_werte), marker='', linestyle=' ', capsize=2, label=self.label)
        ax.set_title(title)
        ax.set_xlabel(self.x_name)
        ax.set_ylabel(self.y_name)
        ax.legend()
        if save == True:
            plt.savefig(f"{title}.pdf")
        

    def from_csv(datei,x_name,y_name,label):
        data = np.genfromtxt(f"{datei}", delimiter=";", skip_header=1)
        werte = Messwerte(data[:, 0], data[:, 1],data[:, 2],data[:, 3], x_name,y_name,label)
        return werte
        
    def plot(self,title, legend = False):
        fig, ax = plt.subplots()
        ax.errorbar( unumpy.nominal_values(self.x_werte) , unumpy.nominal_values(self.y_werte), yerr=unumpy.std_devs(self.y_werte), xerr=unumpy.std_devs(self.x_werte), marker='', linestyle=' ', capsize=2, label=f"{self.label}")
        ax.plot(unumpy.nominal_values(self.x_werte), unumpy.nominal_values(self.y_werte), label=f"{self.label}")
        ax.set_title(title)
        ax.set_xlabel(self.x_name)
        ax.set_ylabel(self.y_name)
        if legend ==True:
            ax.legend()
        
        plt.savefig(f"{title}.pdf")

    def plots(werte: Iterable, title: str ,x_name:str, y_name :str)-> None:
        fig, ax = plt.subplots()
        for werte in werte:
            ax.errorbar( unumpy.nominal_values(werte.x_werte) , unumpy.nominal_values(werte.y_werte), yerr=unumpy.std_devs(werte.y_werte), xerr=unumpy.std_devs(werte.x_werte), marker='', linestyle=' ', capsize=2, label=f"{werte.label}")
            ax.plot(unumpy.nominal_values(werte.x_werte), unumpy.nominal_values(werte.y_werte), label=f"{werte.label}")
        ax.set_title(title)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.legend()
        plt.savefig(f"{title}.pdf")
    
    def fit_plot(self,title:  str, model):
        fig, ax = plt.subplots()

        #fig.set_size_inches(18.5, 10.5)
        ax.errorbar(unumpy.nominal_values(self.x_werte), unumpy.nominal_values(self.y_werte), yerr=unumpy.std_devs(self.y_werte), xerr=unumpy.std_devs(self.x_werte), marker='', linestyle=' ', capsize=1)


        results, pars, perrs = Messwerte.__run_polynomial_fit(unumpy.nominal_values(self.x_werte), unumpy.nominal_values(self.y_werte), unumpy.std_devs(self.y_werte), model)
        fit_data = ""
        label1 = ""
        #making unumpy arrays of pars and perrs:
        fit_parameter=unumpy.uarray(pars,perrs)
        if (model.__name__) == "linear_model":
            fit_data = model(unumpy.nominal_values(self.x_werte), pars[0], pars[1])
            label1 = f"{fit_parameter[0]:p}x+{fit_parameter[1]:p}"
        elif model.__name__ == "qudratic_model":
            fit_data = model(unumpy.nominal_values(self.x_werte), pars[0], pars[1], pars[2])
            label1 = f"{fit_parameter[0]:p}x^2+{fit_parameter[1]:p}x+{fit_parameter[2]:p}"
        elif model.__name__ == "cubic_model":
            fit_data = model(unumpy.nominal_values(self.x_werte), pars[0], pars[1], pars[2], pars[2])
            label1 = (f"{fit_parameter[0]:p}x^3+{fit_parameter[1]:p}x^2+{fit_parameter[2]:p}x+{fit_parameter[3]}")
        ax.set_title(title)
        ax.set_xlabel(self.x_name)
        ax.set_ylabel(self.y_name)
        #print(results)
        ax.plot(unumpy.nominal_values(self.x_werte), fit_data, label=f"{label1}")
       
        
        ax.legend()
        plt.savefig(f"{title}_fit.pdf")
        return results, pars, perrs
        
    def __run_polynomial_fit(x_data1, y_data1, y_err, model_function, debug=False):

        xy_data = XYContainer(x_data=x_data1, y_data=y_data1)
        xy_data.add_error(axis="y", err_val=y_err)
        print(xy_data)
        my_fit = Fit(data=xy_data, model_function=model_function)
        results = my_fit.do_fit()
        if debug == True:
            plot = Plot([my_fit])  # erzeuge ein Plot-Objekt
            plot.plot()
        # put the fit parameters and their uncertainites into arrays (lists) for easier handling
        pars = list()
        perrs = list()
        for p in results['parameter_values']:
            pars.append(results['parameter_values'][p])
            perrs.append(results['parameter_errors'][p])

        return results, pars, perrs
    def linear_model(x, a, b):
        return a*x+b


    def qudratic_model(x, a, b, c):
        return a*x**2+b*x+c


    def cubic_model(x, a, b, c, d):
        return a*x**3+b*x**2+c*x+d
    def y_manipulate(self,function, y_name):
        self.y_werte = function(self.y_werte)
        self.y_name = y_name
        print("y Values manipulated")
    def x_manipulate(self, function, x_name):
        self.x_werte = function(self.x_werte)
        self.x_name = x_name
        print("x Values manipulated")
