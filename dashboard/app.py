import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd
from datetime import datetime
import requests
import json
from sqlalchemy import create_engine, text, inspect, Table
import statistics
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from src.data_import import _load_data_to_db

# from components.layout import create_layout
# import components.callbacks
from src.data_fetching import (
    _fetch_countries,
    _fetch_prod_data_from_db,
    _fetch_weather_data_from_db,
    _fetch_nutrient_data,
    _fetch_emission_data,
    get_monthlytemp_data,
)

# Load Data to database
_load_data_to_db()

agri_data = _fetch_prod_data_from_db()

# Fetch Nutrient Data from DB
nut_table = _fetch_nutrient_data()

# Fetch Emission Data from DB
em_table = _fetch_emission_data()

# Populate map using geo.json
euro_countries = gpd.read_file("./static/custom.geo.json")

weather_data = _fetch_weather_data_from_db()

countries = weather_data["country"].unique()

data = pd.read_csv("../data/weather/weather.csv")

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app_color = {"background-color": "#F1F1F1", "color": "black", "text-align": "center"}
nav_color = {"background-color": "#2A4D7C", "color": "white", "text-align": "center"}
block_color = {"background-color": "#FFFFFF", "color": "black", "text-align": "center"}
margin_style = {"margin": "10px"}  # Add padding
padding_style = {"padding": "10px"}

app.layout = html.Div(
    style={**app_color},
    children=[
        # STARTING NAV BAR
        dbc.Row(
            [
                dbc.Col(
                    html.Div([html.H1("Agriculture Dashboard")]),
                    width=6,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[
                            {"label": country, "value": country}
                            for country in countries
                        ],
                        value="Netherlands",
                    ),
                    width=6,
                    style={**nav_color, "padding": "10px", "color": "black"},
                ),
            ],
            className="mb-4",
            style={**nav_color},
        ),
        # ENDING NAV BAR
        # STARTING FIRST ROW WITH WEATHER AND PRODUCTION
        html.Div(
            style={**app_color},
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                style={**app_color},
                                children=[
                                    html.Div(
                                        style={
                                            "background-color": "#2A4D7C",
                                            "color": "white",
                                            "text-align": "center",
                                            "display": "flex",
                                            "align-items": "center",
                                            "justify-content": "center",
                                        },
                                        children=[html.H2("Weather Data")],
                                    ),
                                    # Weather Analytics Block
                                    html.Div(
                                        style=app_color,
                                        children=[
                                            html.Div(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                html.Label(
                                                                    "Select Analytics"
                                                                ),
                                                                width=6,
                                                            ),
                                                            dbc.Col(
                                                                dcc.Dropdown(
                                                                    id="weather-analytics-dropdown",
                                                                    options=[
                                                                        {
                                                                            "label": "Temperature Time Series",
                                                                            "value": "temp-time",
                                                                        },
                                                                        {
                                                                            "label": "Rainfall Time Series",
                                                                            "value": "rain-time",
                                                                        },
                                                                        {
                                                                            "label": "Snowfall Time Series",
                                                                            "value": "snow-time",
                                                                        },
                                                                    ],
                                                                    value="temp-time",
                                                                ),
                                                                width=4,
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                html.Label(
                                                                    "Select a Date Range"
                                                                ),
                                                                width=6,
                                                            ),
                                                            dbc.Col(
                                                                dcc.DatePickerRange(
                                                                    id="date-range-picker",
                                                                    start_date="2023-01-01",
                                                                    end_date="2023-12-31",
                                                                ),
                                                                width=4,
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                style=block_color,
                                            ),
                                            dbc.Row(
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                id="weather-plot",
                                                                style={
                                                                    "display": "block"
                                                                },
                                                            ),
                                                            dcc.Graph(
                                                                id="temperature-plot",
                                                                style={
                                                                    "display": "block"
                                                                },
                                                            ),
                                                            dcc.Graph(
                                                                id="rain-plot",
                                                                style={
                                                                    "display": "none"
                                                                },
                                                            ),
                                                            dcc.Graph(
                                                                id="snow-plot",
                                                                style={
                                                                    "display": "none"
                                                                },
                                                            ),
                                                        ],
                                                        style=block_color,
                                                    )
                                                )
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Div(
                                                        style={
                                                            "background-color": "#2A4D7C",
                                                            "color": "white",
                                                            "text-align": "center",
                                                            "display": "flex",
                                                            "align-items": "center",
                                                            "justify-content": "center",
                                                        },
                                                        children=[
                                                            html.H3("Statistics")
                                                        ],
                                                    ),
                                                    html.Div(
                                                        id="statistics",
                                                        style={**block_color},
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Button(
                                                                "Retrieve current weather",
                                                                className="btn",
                                                                id="retrieve-button",
                                                                style={
                                                                    "display": "flex",
                                                                    "align-items": "center",
                                                                    "background-color": "#1285D1",
                                                                    "color": "white",
                                                                    "text-align": "center",
                                                                    "margin": "auto",
                                                                },
                                                            ),
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        html.Div(
                                                                            dbc.Row(
                                                                                [
                                                                                    html.Span(
                                                                                        "Temperature:"
                                                                                    ),
                                                                                    html.Span(
                                                                                        id="valueTemperature",
                                                                                        children="72°F",
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                        ),
                                                                    ),
                                                                    dbc.Col(
                                                                        html.Div(
                                                                            dbc.Row(
                                                                                [
                                                                                    html.Span(
                                                                                        "Rain:"
                                                                                    ),
                                                                                    html.Span(
                                                                                        id="valueRain",
                                                                                        children="10%",
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                        )
                                                                    ),
                                                                    dbc.Col(
                                                                        html.Div(
                                                                            dbc.Row(
                                                                                [
                                                                                    html.Span(
                                                                                        "Snow:"
                                                                                    ),
                                                                                    html.Span(
                                                                                        id="valueSnow",
                                                                                        children="0%",
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                        )
                                                                    ),
                                                                ]
                                                            ),
                                                        ],
                                                        style=block_color,
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                style={**block_color},
                                                children=[
                                                    # EU map analytics
                                                    html.Div(
                                                        style={
                                                            "margin-top": "20px",
                                                            "background-color": "#2A4D7C",
                                                            "color": "white",
                                                            "text-align": "center",
                                                            "display": "flex",
                                                            "align-items": "center",
                                                            "justify-content": "center",
                                                        },
                                                        children=[
                                                            html.H3(
                                                                "Agricultural Indicators"
                                                            )
                                                        ],
                                                    ),
                                                    html.P("Select an Indicator:"),
                                                    dcc.Dropdown(
                                                        id="indicator-dropdown",
                                                        options=[
                                                            {
                                                                "label": "Nitrogen",
                                                                "value": "Nitrogen",
                                                            },
                                                            {
                                                                "label": "Phosphorus",
                                                                "value": "Phosphorus",
                                                            },
                                                            {
                                                                "label": "Emissions",
                                                                "value": "Emissions",
                                                            },
                                                        ],
                                                        value="Emissions",
                                                    ),
                                                    dcc.Dropdown(
                                                        id="year-dropdown",
                                                        options=[
                                                            {
                                                                "label": "2010",
                                                                "value": "2010",
                                                            },
                                                            {
                                                                "label": "2011",
                                                                "value": "2011",
                                                            },
                                                            {
                                                                "label": "2012",
                                                                "value": "2012",
                                                            },
                                                            {
                                                                "label": "2013",
                                                                "value": "2013",
                                                            },
                                                            {
                                                                "label": "2014",
                                                                "value": "2014",
                                                            },
                                                            {
                                                                "label": "2015",
                                                                "value": "2015",
                                                            },
                                                            {
                                                                "label": "2016",
                                                                "value": "2016",
                                                            },
                                                            {
                                                                "label": "2017",
                                                                "value": "2017",
                                                            },
                                                            {
                                                                "label": "2018",
                                                                "value": "2018",
                                                            },
                                                            {
                                                                "label": "2019",
                                                                "value": "2019",
                                                            },
                                                            {
                                                                "label": "2020",
                                                                "value": "2020",
                                                            },
                                                            {
                                                                "label": "2021",
                                                                "value": "2021",
                                                            },
                                                        ],
                                                        value="2021",
                                                    ),
                                                    dcc.Graph(
                                                        id="choropleth-maps-x-graph"
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            width=6,
                            style=app_color,
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    style={
                                        "background-color": "#2A4D7C",
                                        "color": "white",
                                        "text-align": "center",
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "center",
                                    },
                                    children=[html.H2("Production Data")],
                                ),
                                html.Div(
                                    style=block_color,
                                    children=[
                                        dcc.Dropdown(
                                            id="dashboard-dropdown",
                                            options=[
                                                {
                                                    "label": "Value by Type Over Years",
                                                    "value": "value",
                                                },
                                                {
                                                    "label": "Growth Percentage Over Years",
                                                    "value": "percentage",
                                                },
                                            ],
                                            value="percentage",  # Default selected value
                                            multi=False,
                                        ),
                                        dcc.Graph(id="line-chart"),
                                    ],
                                ),
                                html.Div(
                                    style={
                                        "margin-top": "20px",
                                        "background-color": "#2A4D7C",
                                        "color": "white",
                                        "text-align": "center",
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "center",
                                    },
                                    children=[html.H2("Production prediction")],
                                ),
                                dbc.Col(
                                    html.Div(
                                        style={**block_color},
                                        children=[
                                            html.Label("Select Type:"),
                                            dcc.Dropdown(
                                                id="type-dropdown-regression",
                                                options=[
                                                    {
                                                        "label": data_type,
                                                        "value": data_type.strip(),
                                                    }
                                                    for data_type in agri_data[
                                                        "Type"
                                                    ].unique()
                                                    if pd.notna(data_type)
                                                ],
                                                value="Cereals",
                                                multi=False,  # Allow multiple selections
                                            ),
                                            dcc.Graph(id="line-chart-regression"),
                                        ],
                                    )
                                ),
                            ],
                            width=6,
                        ),
                    ]
                )
            ],
        ),
    ],
)


# Weather - Temperature timeseries callback
@app.callback(
    Output("temperature-plot", "style"),
    Input("weather-analytics-dropdown", "value"),
)
def update_graph_visibility(selected_option):
    if selected_option == "temp-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Weather - Rainfall timeseries callback
@app.callback(
    Output("rain-plot", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "rain-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Weather - Snowfall timeseries callback
@app.callback(
    Output("snow-plot", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "snow-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Weather - Summary statistics callback
# @app.callback(
#     Output("statistics", "style"), Input("weather-analytics-dropdown", "value")
# )
# def update_graph_visibility(selected_option):
#     if selected_option == "summary":
#         return {"display": "block"}
#     else:
#         return {"display": "none"}


# Weather analytics callback
@app.callback(
    [
        Output("weather-plot", "figure"),
        Output("temperature-plot", "figure"),
        Output("rain-plot", "figure"),
        Output("snow-plot", "figure"),
        Output("statistics", "children"),
    ],
    [
        Input("country-dropdown", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
        Input("weather-analytics-dropdown", "value"),
    ],
)
def update_plots(selected_country, start_date, end_date, selected_data):
    # filter the data for the selected country and date range
    # weather_data = _fetch_weather_data_from_db()
    aggregated_data = weather_data.groupby(
        ["date", "country", "longitude", "latitude"], as_index=False
    ).mean(numeric_only=True)
    filtered_data = aggregated_data[
        (aggregated_data["country"] == selected_country)
        & (aggregated_data["date"] >= start_date)
        & (aggregated_data["date"] <= end_date)
    ]

    # create a temperature line plot
    temperature_fig = px.line(
        filtered_data,
        x="date",
        y="temp_mean",
        title=f"Temperature in {selected_country}",
        labels={"date": "Date", "temp_mean": "Mean Temperature in °C"},
    )

    # create a rainfall line plot
    rain_fig = px.line(
        filtered_data,
        x="date",
        y="rain",
        title=f"Rainfall in {selected_country}",
        labels={"date": "Date", "rain": "Rainfall in mm"},
    )

    # create a snowfall line plot
    snow_fig = px.line(
        filtered_data,
        x="date",
        y="snow",
        title=f"Snowfall in {selected_country}",
        labels={"date": "Date", "rain": "Snowfall in mm"},
    )

    # calculate statistics not needed but I was just interesting in these statistics
    mean_temp = filtered_data["temp_mean"].mean()
    max_temp = filtered_data["temp_mean"].max()
    min_temp = filtered_data["temp_mean"].min()

    mean_rain = filtered_data["rain"].mean()
    max_rain = filtered_data["rain"].max()
    min_rain = filtered_data["rain"].min()

    mean_snow = filtered_data["snow"].mean()
    max_snow = filtered_data["snow"].max()
    min_snow = filtered_data["snow"].min()

    # create statistics text
    statistics_text = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.P(f"Mean Temperature: {mean_temp:.2f}°C"),
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(f"Max Temperature: {max_temp:.2f}°C"),
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(f"Min Temperature: {min_temp:.2f}°C"),
                        )
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.P(f"Mean Rainfall: {mean_rain:.2f} mm"),
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(f"Max Rainfall: {max_rain:.2f} mm"),
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(f"Min Rainfall: {min_rain:.2f} mm"),
                        )
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.P(f"Mean Snowfall: {mean_snow:.2f} mm"),
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(f"Max Snowfall: {max_snow:.2f} mm"),
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            html.P(f"Min Snowfall: {min_snow:.2f} mm"),
                        )
                    ),
                ]
            ),
        ]
    )

    # get the mean temperature and suntimes for the overview graph and draw these with the rain and sun in the overview graph
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    db_conn = engine.connect()
    start_year = int(start_date.split("-")[0])
    end_year = int(end_date.split("-")[0])
    start_month = int(start_date.split("-")[1])
    end_month = int(end_date.split("-")[1])
    data = get_monthlytemp_data(
        selected_country, db_conn, start_year, end_year, start_month, end_month
    )
    if not data.empty:
        fig = make_subplots(
            specs=[[{"secondary_y": True}]]
        )  # Create subplots with a secondary y-axis
        fig.add_trace(
            go.Scatter(
                x=data["month_year"],
                y=data["mean_temp"],
                mode="lines",
                name="Temperature",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data["month_year"],
                y=data["mean_sunhours"],
                mode="lines",
                name="Sunhours",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=filtered_data["date"],
                y=filtered_data["rain"],
                mode="lines",
                name="Rainfall",
            ),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(
                x=filtered_data["date"],
                y=filtered_data["snow"],
                mode="lines",
                name="Snowfall",
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title=f"Weather Data in {selected_country}",
            xaxis_title="Date",
            xaxis_rangeslider_visible=True,
        )
    else:
        fig = px.line(title=f"No data available for {selected_country}")
    db_conn.close()

    return (
        fig,
        temperature_fig,
        rain_fig,
        snow_fig,
        statistics_text,
    )  # current_weather


# Current weather callback
@app.callback(
    (
        Output("valueTemperature", "children"),
        Output("valueRain", "children"),
        Output("valueSnow", "children"),
    ),
    Input("retrieve-button", "n_clicks"),
    Input("country-dropdown", "value"),
)
def update_output(n_clicks, country):
    if n_clicks is not None and n_clicks > 0:
        # The button has been pressed
        latitude = weather_data.loc[weather_data["country"] == country][
            "latitude"
        ].tolist()[0]
        longitude = weather_data.loc[weather_data["country"] == country][
            "longitude"
        ].tolist()[0]
        api_string = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,rain,snowfall&forecast_days=1"
        final_string = api_string.format(latitude=latitude, longitude=longitude)
        r = requests.get(final_string)
        j = json.loads(r.text)
        temp_mean = j["current"]["temperature_2m"]
        rain = j["current"]["rain"]
        snow = j["current"]["snowfall"]
        return temp_mean, rain, snow
    else:
        return "", "", ""


# Agri production Callback
@app.callback(
    Output("line-chart", "figure"),
    [Input("dashboard-dropdown", "value"), Input("country-dropdown", "value")],
)
def update_dashboard(selected_dashboard, selected_country):
    if selected_dashboard == "value":
        # Filter data based on selected country
        filtered_df = agri_data[agri_data["Country"] == selected_country]

        # Create traces for each type
        traces = []
        for data_type in filtered_df["Type"].unique():
            type_data = filtered_df[filtered_df["Type"] == data_type]
            trace = dict(
                x=type_data["Year"], y=type_data["Value"], mode="lines", name=data_type
            )
            traces.append(trace)

        # Create the layout for the line chart
        layout = dict(
            title=f"{selected_country} - Value by Type Over Years",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Value"),
        )

        # Return a single Figure object
        line_chart_figure = dict(data=traces, layout=layout)

        return line_chart_figure

    elif selected_dashboard == "percentage":
        # Filter data based on selected country
        filtered_df = agri_data[agri_data["Country"] == selected_country]

        # Sort the DataFrame by Country, Type, and Year
        filtered_df.sort_values(by=["Country", "Type", "Year"], inplace=True)

        # Calculate the growth percentage for each group (Country and Type)
        filtered_df["Growth"] = (
            filtered_df.groupby(["Country", "Type"])["Value"].pct_change() * 100
        )
        filtered_df["Growth"] = filtered_df["Growth"].fillna(0)

        # Reset index to have a clean DataFrame
        filtered_df.reset_index(drop=True, inplace=True)

        # Create line chart figure with separate traces for each 'Type'
        line_chart_figure = {
            "data": [
                {
                    "x": filtered_df[filtered_df["Type"] == type_name]["Year"],
                    "y": filtered_df[filtered_df["Type"] == type_name]["Growth"],
                    "type": "line",
                    "name": type_name,
                }
                for type_name in filtered_df["Type"].unique()
            ],
            "layout": {
                "title": f"Growth Percentage Over Years - {selected_country}",
                "xaxis": {"title": "Year"},
                "yaxis": {"title": "Growth Percentage"},
            },
        }

        return line_chart_figure


# Map analytics callback
@app.callback(
    Output("choropleth-maps-x-graph", "figure"),
    Input("indicator-dropdown", "value"),
    Input("year-dropdown", "value"),
)
def update_choropleth(indicator, year):
    if indicator == "Emissions":
        map_data = em_table[em_table["Year"] == year]
    else:
        nut = nut_table[nut_table["Nutrient"] == indicator]
        map_data = nut[nut["Year"] == year]

    fig = px.choropleth(
        map_data,
        geojson=euro_countries,
        locations="Country",
        color="Value",
        scope="europe",
        featureidkey="properties.name",
    )

    return fig


# regression callback
@app.callback(
    Output("line-chart-regression", "figure"),
    [
        Input("country-dropdown", "value"),
        Input("type-dropdown-regression", "value"),
    ],
)
def update_regression_chart(
    selected_country,
    selected_type,
):
    prod_by_country_no_type = agri_data[agri_data["Country"] == selected_country]

    # Filter production data to only contain relevant production type
    prod_by_country = prod_by_country_no_type[
        prod_by_country_no_type["Type"] == selected_type
    ]

    # Filter weather data to only consider weather data from selected country.
    sorted_weather = weather_data[
        weather_data["country"] == selected_country
    ].sort_values("date", ascending=False)

    # Select first and last available year in dataset
    start_year = sorted_weather.iloc[-1]["date"].year
    end_year = sorted_weather.iloc[0]["date"].year

    month = sorted_weather.iloc[0]["date"].month

    reg_data = pd.DataFrame()

    # Aggregate weather data by month for each year and create row of dependant variables
    for i in range(start_year, end_year + 1):
        yearly_weather = sorted_weather[sorted_weather["date"].dt.year == i]
        data_for_year = pd.DataFrame()

        for k in range(1, month):
            # print(f"{i}-{k}")
            monthly_weather = yearly_weather[yearly_weather["date"].dt.month == k]
            avg_rain = monthly_weather["rain"].mean()
            avg_temp = monthly_weather["temp_mean"].mean()
            data_for_year[f"{k}-rain"] = [avg_rain]  # This shows NaN

            data_for_year[f"{k}-temp"] = [avg_temp]
        prod = prod_by_country[prod_by_country["Year"] == str(i)]
        try:
            data_for_year["production"] = prod["Value"].values
        except:
            data_for_year["production"] = float("NaN")
        data_for_year["year"] = i
        reg_data = pd.concat(
            [reg_data, pd.DataFrame([data_for_year][0])], ignore_index=True
        )

    training = reg_data.iloc[:10]
    # Drop rows with empty values (in this case production)
    training = training.dropna()
    prediction = reg_data.iloc[10:11]

    X = training.drop(["year", "production"], axis=1)

    y = training["production"]

    x_pred = prediction.drop(["year", "production"], axis=1)

    model = LinearRegression().fit(X, y)

    y_pred = model.predict(x_pred)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=prod_by_country["Year"],
            y=prod_by_country["Value"],
            mode="markers",
            name="Prodcution",
        )
    )
    fig.add_trace(go.Scatter(x=["2023"], y=y_pred, mode="markers", name="Prediction"))
    fig.update_layout(
        title=(
            f"Prediction of {selected_type} production in {selected_country} for 2023"
        ),
        xaxis_title="Prediction",
        yaxis_title="Production",
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
