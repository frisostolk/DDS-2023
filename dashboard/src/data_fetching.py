import pandas as pd
import statistics
from sqlalchemy import create_engine, text, inspect, Table


# Fetch all production data from the DB
def _fetch_prod_data_from_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    agri_prod = pd.read_sql_table("production", engine, index_col="index")
    return agri_prod


# Fetch all weather data form the DB
def _fetch_weather_data_from_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    weather = pd.read_sql_table("weather", engine, index_col="index")
    return weather


def _fetch_nutrient_data():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    nutrients = pd.read_sql_table("nutrients", engine, index_col="index")
    return nutrients


def _fetch_emission_data():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    em_table = pd.read_sql_table("emissions", engine, index_col="index")
    return em_table


# Fetch list of countries
def _fetch_countries():
    weather = _fetch_weather_data_from_db()
    countries = weather["country"].unique()
    return countries

#Calculate the mean temperatures and sunhours for the months in the date picker, return an dataframe with the values
def get_monthlytemp_data(selected_country, db_conn, start_year, end_year, start_month, end_month): 
    data_frames = []
    if end_month == 12:
        end_year = end_year + 1
        end_month = 1
    for year in range(start_year, end_year + 1):
        if year == start_year:
            month_range_start = start_month
        else:
            month_range_start = 1

        if year == end_year:
            month_range_end = end_month + 1
        else:
            month_range_end = 12

        query = f'''
            SELECT 
            TO_CHAR(w.date, 'YYYY-MM') as month_year,
            AVG(w.temp_mean) as mean_temp,
            EXTRACT(EPOCH FROM AVG(w.sunset - w.sunrise)) / 3600 as mean_sunhours
            FROM weather as w
            WHERE w.country = '{selected_country}'
            AND EXTRACT(YEAR FROM w.date) = {year}
            AND EXTRACT(MONTH FROM w.date) BETWEEN {month_range_start} AND {month_range_end}
            GROUP BY month_year
        '''
        table = pd.read_sql(query, db_conn)
        if not table.empty:
            data_frames.append(table)

    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return pd.DataFrame()
