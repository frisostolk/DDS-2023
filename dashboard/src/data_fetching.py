import pandas as pd
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


# Fetch list of capitals
def _fetch_capitals():
    weather = _fetch_weather_data_from_db()
    capitals = weather["capital"].unique()
    print(capitals)
    return capitals
