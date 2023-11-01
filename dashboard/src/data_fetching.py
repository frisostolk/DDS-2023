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


# Fetch list of capitals
def _fetch_capitals():
    weather = _fetch_weather_data_from_db()
    capitals = weather["capital"].unique()
    print(capitals)
    return capitals

def get_monthly_data(selected_country, db_conn):
    data_frames = []
    for year in range(2013, 2024):
        query = f'''
            SELECT 
            TO_CHAR(w.date, 'YYYY-MM') as month_year,
            AVG(w.temp_mean) as mean_temp,
            EXTRACT(EPOCH FROM (MAX(w.sunset) - MIN(w.sunrise))) / 3600 as mean_sunhours
            FROM weather as w
            WHERE w.country = '{selected_country}'
            AND EXTRACT(YEAR FROM w.date) = {year}
            GROUP BY month_year
        '''

        table = pd.read_sql(query, db_conn)
        if not table.empty:
            data_frames.append(table)

    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return pd.DataFrame()