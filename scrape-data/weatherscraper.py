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
from datetime import datetime


def main():
    """ Main function """
    end_date = datetime.today().strftime('%Y-%m-%d')
    old_df = pd.read_csv("./weather.csv")
    start_date = old_df["date"].max()
    df = pd.read_csv("./cities_europe2.csv", sep=",", encoding='unicode_escape')
    api_string = "https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,sunrise,sunset,rain_sum,snowfall_sum&timezone=auto"
    first_row = True
    for index, row in df.iterrows():
        longitude = row["Longitude"]
        latitude = row["Latitude"]
        country = row["Country"]
        capital = row["capital"]
        final_string = api_string.format(latitude=latitude, longitude=longitude, start_date=start_date,end_date=end_date)
        r = requests.get(final_string)
        j = json.loads(r.text)
        try:
            dates = j["daily"]["time"]
            country = [country] * len(dates)
            capital = [capital] * len(dates)
            temp_mean = j["daily"]["temperature_2m_mean"]
            temp_max = j["daily"]["temperature_2m_max"]
            temp_min = j["daily"]["temperature_2m_min"]
            sunrise = j["daily"]["sunrise"]
            sunset = j["daily"]["sunset"]
            rain = j["daily"]["rain_sum"]
            snow = j["daily"]["snowfall_sum"]
        except KeyError:
            # try again in an hour
            time.sleep(3600)
        df2 = pd.read_csv("./weather.csv")
        df3 = pd.DataFrame(list(zip(dates,temp_mean, temp_max,temp_min,sunrise,sunset,rain,snow,country, capital)), columns =['date','temp_mean', 'temp_max','temp_min','sunrise','sunset','rain','snow',"country", "capital"])
        result = pd.concat([df2,df3])
        result.to_csv("./weather_data_api.csv")
        time.sleep(60)


if __name__ == '__main__':
    main()