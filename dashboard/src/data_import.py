import pandas as pd
from sqlalchemy import create_engine, text, inspect, Table

def _load_data_to_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")

    with engine.connect() as conn:
        result = conn.execute(text("DROP TABLE IF EXISTS population, area, nutrients, emissions, weather CASCADE; "))

    # population_df = pd.read_csv("../data/world_population.csv", delimiter=";")
    # population_df.to_sql("population", engine, if_exists="replace", index=True)
    agri_prod_cereals = pd.read_excel("../data/agri_production/cereals.xlsx", "Sheet 1", header=8, usecols="A,B,D,F,H,J,L,N,P,R,T,V", skiprows=[9, 10, 11, 12], skipfooter=7, na_values=":")
    agri_prod_cereals = agri_prod_cereals.rename(columns={'TIME': 'Country'})
    agri_prod_cereals = agri_prod_cereals.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_cereals["Type"] = "Cereals"

    agri_prod_vegetables = pd.read_excel("../data/agri_production/vegetables.xlsx", "Sheet 1", header=8,  usecols="A,B,D,F,H,J,L,N,P,R,T,V", skiprows=[9, 10, 11, 12], skipfooter=7, na_values=":")
    agri_prod_vegetables = agri_prod_vegetables.rename(columns={'TIME': 'Country'})
    agri_prod_vegetables = agri_prod_vegetables.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_vegetables["Type"] = "Vegetables"

    #Data set for dairy
    agri_prod_dairy = pd.read_excel("../data/agri_production/dairy.xlsx", "Sheet 1", header=8, usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[9, 10, 11, 12], skipfooter=9, na_values=":")
    agri_prod_dairy = agri_prod_dairy.rename(columns={'TIME': 'Country'})
    agri_prod_dairy = agri_prod_dairy.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_dairy["Type"] = "Dairy"

    #Data sets for meat production
    agri_prod_beef = pd.read_excel("../data/agri_production/beef.xlsx", "Sheet 1", header=9, usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[10, 11, 12, 13, 14, 15], skipfooter=7, na_values=":")
    agri_prod_beef = agri_prod_beef.rename(columns={'TIME': 'Country'})
    agri_prod_beef = agri_prod_beef.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_beef["Type"] = "Beef"

    agri_prod_mutton = pd.read_excel("../data/agri_production/mutton.xlsx", "Sheet 1", header=9,  usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[10, 11, 12, 13, 14, 15], skipfooter=7, na_values=":")
    agri_prod_mutton = agri_prod_mutton.rename(columns={'TIME': 'Country'})
    agri_prod_mutton = agri_prod_mutton.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_mutton["Type"] = "Mutton"


    agri_prod_pork = pd.read_excel("../data/agri_production/pork.xlsx", "Sheet 1", header=9,  usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[10, 11, 12, 13, 14, 15], skipfooter=7, na_values=":")
    agri_prod_pork = agri_prod_pork.rename(columns={'TIME': 'Country'})
    agri_prod_pork = agri_prod_pork.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_pork["Type"] = "Pork"

    #Data set for poultry production
    agri_prod_poultry = pd.read_excel("../data/agri_production/poultry.xlsx", "Sheet 1", header=9, usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[10, 11, 12, 13, 14, 15], skipfooter=9, na_values=":")
    agri_prod_poultry = agri_prod_poultry.rename(columns={"TIME": "Country"})
    agri_prod_poultry = agri_prod_poultry.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_prod_poultry["Type"] = "Poultry"

    #Combine all production df's into one frame
    frames = [agri_prod_cereals, agri_prod_vegetables, agri_prod_dairy, agri_prod_beef, agri_prod_mutton, agri_prod_pork, agri_prod_poultry ]
    agri_prod = pd.concat(frames)
    
    #Agri area data import
    agri_area = pd.read_excel("../data/agri_area/general_area_2020.xlsx", "Sheet 1", header=11, usecols="A,B,D,F,H,J,L,N,P,R,T,V", skiprows=[12], skipfooter=5, na_values=":")
    agri_area = agri_area.rename(columns={"CROPS (Labels)": "Country"})

    #Agricultural nutrient data
    agri_nut_nitrogen = pd.read_excel("../data/agri_nutrients/nitrogen_per_hectare.xlsx", "Sheet 1", header=8,  usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[9, 10], skipfooter=5, na_values=":")
    agri_nut_nitrogen = agri_nut_nitrogen.rename(columns={"TIME": "Country"})
    agri_nut_nitrogen = agri_nut_nitrogen.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_nut_nitrogen["Nutrient"] = "Nitorgen"

    agri_nut_phosphorus = pd.read_excel("../data/agri_nutrients/phosphorus_per_hectare.xlsx", "Sheet 1", header=8, usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[9, 10], skipfooter=5, na_values=":")
    agri_nut_phosphorus = agri_nut_phosphorus.rename(columns={"TIME": "Country"})
    agri_nut_phosphorus = agri_nut_phosphorus.melt(id_vars='Country', var_name='Year', value_name='Value')
    agri_nut_phosphorus["Nutrient"] = "Phosphorus"

    frames = [agri_nut_nitrogen, agri_nut_phosphorus]
    
    #Combine all nutrient df's into one frame
    agri_nut = pd.concat(frames)
    
    #Greenhouse eimission data import
    agri_greenhouse_emissions = pd.read_excel("../data/agri_emissions/greenhouse.xlsx", "Sheet 1", header=9,  usecols="A,B,D,F,H,J,L,N,P,R,T", skiprows=[10, 11], skipfooter=3, na_values=":")
    agri_greenhouse_emissions = agri_greenhouse_emissions.rename(columns={"TIME": "Country"})
    agri_greenhouse_emissions = agri_greenhouse_emissions.melt(id_vars='Country', var_name='Year', value_name='Value')

    #Weather data import
    weather_data = pd.read_csv("../data/weather/weather.csv", index_col=0)
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    weather_data['sunrise'] = pd.to_datetime(weather_data['sunrise'])
    weather_data['sunset'] = pd.to_datetime(weather_data['sunset'])
    
    #Read data into DB files
    agri_prod.to_sql("production", engine, if_exists="replace", index=True)
    agri_area.to_sql("area", engine, if_exists="replace", index=True)
    agri_nut.to_sql("nutrients", engine, if_exists="replace", index=True)
    agri_greenhouse_emissions.to_sql("emissions", engine, if_exists="replace", index=True)
    weather_data.to_sql("weather", engine, if_exists="replace", index=True)
