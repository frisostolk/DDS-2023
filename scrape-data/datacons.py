# Filename: Weatherscraper.py
# Description: processes all the weather data and combined it in to one readable format.
# Date: 2-10-2023
# Author: F.R.P. Stolk


import pandas as pd
import sys
import json
import os
import requests
import time
import matplotlib.pyplot as plt


def main():
    """ Main function """
    # start_date = "2015-01-01"
    # end_date = "2023-10-01"
    # df = pd.read_csv("./weather_data_api.csv", sep=",")
    # wrong_col = ['Unnamed: 0.57', 'Unnamed: 0.56', 'Unnamed: 0.55', 'Unnamed: 0.54','Unnamed: 0.53', 'Unnamed: 0.52', 'Unnamed: 0.51', 'Unnamed: 0.50','Unnamed: 0.49', 'Unnamed: 0.48', 'Unnamed: 0.47', 'Unnamed: 0.46','Unnamed: 0.45', 'Unnamed: 0.44', 'Unnamed: 0.43', 'Unnamed: 0.42','Unnamed: 0.41', 'Unnamed: 0.40', 'Unnamed: 0.39', 'Unnamed: 0.38','Unnamed: 0.37', 'Unnamed: 0.36', 'Unnamed: 0.35', 'Unnamed: 0.34','Unnamed: 0.33', 'Unnamed: 0.32', 'Unnamed: 0.31', 'Unnamed: 0.30','Unnamed: 0.29', 'Unnamed: 0.28', 'Unnamed: 0.27', 'Unnamed: 0.26','Unnamed: 0.25', 'Unnamed: 0.24', 'Unnamed: 0.23', 'Unnamed: 0.22','Unnamed: 0.21', 'Unnamed: 0.20', 'Unnamed: 0.19', 'Unnamed: 0.18','Unnamed: 0.17', 'Unnamed: 0.16', 'Unnamed: 0.15', 'Unnamed: 0.14','Unnamed: 0.13', 'Unnamed: 0.12', 'Unnamed: 0.11', 'Unnamed: 0.10','Unnamed: 0.9', 'Unnamed: 0.8', 'Unnamed: 0.7', 'Unnamed: 0.6','Unnamed: 0.5', 'Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2','Unnamed: 0.1', 'Unnamed: 0']
    # df = df.drop(columns=wrong_col)
    # print(df.head())
    df = pd.read_csv("./cleaned_data.csv", sep=",")
    df_ams = df.loc[df['capital'] == "Amsterdam"]
    print(df_ams)
    plt.plot(df_ams["date"], df_ams["temp_max"])
    plt.show(block=True)

if __name__ == '__main__':
    main()