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


def get_mean_temp(selected_country,year, formatted_month, db_conn, monthly_temp_data, temp_date, formatted_date):
    query_1 = '''SELECT w.temp_mean
                 FROM weather as w
                 WHERE w.country = '%s'
                 AND TO_CHAR(w.date, 'YYYY-MM-DD') LIKE '%s-%s-__'
              ''' % (selected_country, year, formatted_month)
    table_1 = pd.read_sql(query_1, db_conn) if not query_1.isspace() else pd.DataFrame()
    if not table_1.empty:
        meantemp_int = table_1['temp_mean'].astype(int)
        meantemp_value = statistics.mean(meantemp_int)
        monthly_temp_data.append(meantemp_value)
        temp_date.append(formatted_date) 

def get_mean_rain(selected_country,year, formatted_month, db_conn, monthly_rain_data, rain_date, formatted_date):
    query_1 = '''SELECT w.rain
                 FROM weather as w
                 WHERE w.country = '%s'
                 AND TO_CHAR(w.date, 'YYYY-MM-DD') LIKE '%s-%s___'
              ''' % (selected_country, year, formatted_month)
    table_1 = pd.read_sql(query_1, db_conn) if not query_1.isspace() else pd.DataFrame()
    if not table_1.empty:
        meanrain_float = table_1['rain'].astype(float)
        meanrain_value = statistics.mean(meanrain_float)
        monthly_rain_data.append(meanrain_value)
        rain_date.append(formatted_date) 

def get_mean_snow(selected_country,year, formatted_month, db_conn, monthly_snow_data, snow_date, formatted_date):
    query_1 = '''SELECT w.snow
                 FROM weather as w
                 WHERE w.country = '%s'
                 AND TO_CHAR(w.date, 'YYYY-MM-DD') LIKE '%s-%s___'
              ''' % (selected_country, year, formatted_month)
    table_1 = pd.read_sql(query_1, db_conn) if not query_1.isspace() else pd.DataFrame()
    if not table_1.empty:
        meansnow_float = table_1['snow'].astype(float)
        meansnow_value = statistics.mean(meansnow_float)
        monthly_snow_data.append(meansnow_value)
        snow_date.append(formatted_date)
        
def get_mean_sun(selected_country,year, formatted_month, db_conn, monthly_sunhours_data, sunhours_date, formatted_date):
    query = '''
        SELECT 
        w.sunrise as sunrise_time,
        w.sunset as sunset_time
        FROM weather as w
        WHERE w.country = '%s'
        AND TO_CHAR(w.date, 'YYYY-MM-DD') LIKE '%s-%s___'
        ''' % (selected_country, year, formatted_month)

    table_suntime = pd.read_sql(query, db_conn) if not query.isspace() else pd.DataFrame()
    table_suntime['sunrise_time'] = pd.to_datetime(table_suntime['sunrise_time'], format='%Y-%m-%dT%H:%M')
    table_suntime['sunset_time'] = pd.to_datetime(table_suntime['sunset_time'], format='%Y-%m-%dT%H:%M')

    table_suntime['time_difference'] = (table_suntime['sunset_time'] - table_suntime['sunrise_time']).dt.total_seconds() / 3600.0
    if not table_suntime.empty:
        meansuntime_value = statistics.mean(table_suntime['time_difference'])
        monthly_sunhours_data.append(meansuntime_value)
        sunhours_date.append(formatted_date)  