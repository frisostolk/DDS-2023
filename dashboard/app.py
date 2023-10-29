import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime
import requests
import json
from sqlalchemy import create_engine, text, inspect, Table
import statistics

from src.data_import import _load_data_to_db

# from components.layout import create_layout
# import components.callbacks
from src.data_fetching import (
    _fetch_capitals,
    _fetch_prod_data_from_db,
    _fetch_weather_data_from_db,
    get_mean_temp,
    get_mean_rain,
    get_mean_snow,
    get_mean_sun,
)

# load data to db
#_load_data_to_db()

weather_data = _fetch_weather_data_from_db()

countries = weather_data["country"].unique()

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    style={},
    children=[
        html.H1("Agriculture Dashboard"),
        html.Div(
            style={},
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                children=[
                                    # Weather Analytics Block
                                    html.Div(
                                        style={},
                                        children=[
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.Label(
                                                                    "Select a country:"
                                                                ),
                                                                dcc.Dropdown(
                                                                    id="country-dropdown",
                                                                    options=[
                                                                        {
                                                                            "label": country,
                                                                            "value": country,
                                                                        }
                                                                        for country in countries
                                                                    ],
                                                                    value="Mariehamn",
                                                                ),
                                                            ]
                                                        ),
                                                        width=6,
                                                    ),
                                                    dbc.Col(
                                                        html.Div(
                                                            [
                                                                html.Label(
                                                                    "Select Analytics"
                                                                ),
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
                                                                        {
                                                                            "label": "Sunhours Time Series",
                                                                            "value": "sun-time",
                                                                        },
                                                                        {
                                                                            "label": "Summary",
                                                                            "value": "summary",
                                                                        },
                                                                    ],
                                                                    value="temp-time",
                                                                ),
                                                            ]
                                                        ),
                                                        width=6,
                                                    ),
                                                ]
                                            ),
                                            html.Label("Select a date range:"),
                                            dcc.DatePickerRange(
                                                id="date-range-picker",
                                                start_date="2016-01-01",
                                                end_date="2020-12-31",
                                            ),
                                            dbc.Row(
                                                dbc.Col(
                                                    html.Div(
                                                        [
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
                                                        ]
                                                    )
                                                )
                                            ),
                                            dbc.Row(
                                                dbc.Col(
                                                    html.Div(
                                                        id="statistics",
                                                        style={"display": "none"},
                                                    ),
                                                )
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            html.Div(
                                id="weather",
                                style={"display": "none"},
                            ),
                            width=6,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id="meantemperature-plot",
                                        style={
                                            "display": "block"
                                        },
                                    ),
                                    dcc.Graph(
                                         id="meanrain-plot",
                                         style={
                                            "display": "none"
                                         },
                                    ),
                                    dcc.Graph(
                                         id="meansnow-plot",
                                         style={
                                             "display": "none"
                                         },
                                    ),  
                                    dcc.Graph(
                                        id="meanSuntime-plot",
                                        style={
                                            "display": "none"
                                        },
                                    ),
                                ]
                            )
                        ),
                        dbc.Col(
                            html.Div(
                                children=[
                                    # Add other analytics here
                                ]
                            )
                        ),
                    ]
                ),
            ],
        ),
    ],
)


# Weather - Temperature timeseries callback
@app.callback(
    Output("temperature-plot", "style"),
    Output("weather", "style"),
    Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "temp-time":
        return {"display": "block"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}


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
@app.callback(
    Output("statistics", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "summary":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Mean Weather statistics callbacks
# Mean monthly temperature
@app.callback(
    Output("meantemperature-plot", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "temp-time":
        return {"display": "block"}
    else:
        return {"display": "none"}

#mean rainfall callback
@app.callback(
    Output("meanrain-plot", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "rain-time":
        return {"display": "block"}
    else:
        return {"display": "none"}

#mean snowfall callback
@app.callback(
    Output("meansnow-plot", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "snow-time":
        return {"display": "block"}
    else:
        return {"display": "none"}

#mean Suntime callback
@app.callback(
    Output("meanSuntime-plot", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "sun-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    [
        Output("temperature-plot", "figure"),
        Output("rain-plot", "figure"),
        Output("snow-plot", "figure"),
        Output("statistics", "children"),
        Output("weather","children"),
        Output("meantemperature-plot", "figure"),
        Output("meanrain-plot", "figure"),
        Output("meansnow-plot", "figure"),
        Output("meanSuntime-plot", "figure"),
    ],
    [
        Input("country-dropdown", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
    ],
)
def update_plots(selected_country, start_date, end_date):
    # filter the data for the selected country and date range
    #weather_data = _fetch_weather_data_from_db()
    aggregated_data = weather_data.groupby(['date','country', "longitude", "latitude"], as_index=False).mean(numeric_only=True)
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
    )

    # create a rainfall line plot
    rain_fig = px.line(
        filtered_data, x="date", y="rain", title=f"Rainfall in {selected_country}"
    )

    # create a snowfall line plot
    snow_fig = px.line(
        filtered_data, x="date", y="snow", title=f"Snowfall in {selected_country}"
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
            html.H2("Statistics"),
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


    current_weather = html.Div([
        html.Div(className="dashboard", children=[
            html.Div(className="header", children="Current Weather"),
            html.Button("Retrieve Now", className="button", id="retrieve-button"),
            html.Div(className="row", children=[
                html.Span(className="label", children="Temperature:"),
                html.Span(id="valueTemperature", children="72°F")
                ]),
            html.Div(className="row", children=[
                html.Span(className="label", children="Rain:"),
                html.Span(id="valueRain", children="10%")
                ]),
            html.Div(className="row", children=[
                html.Span(className="label", children="Snow:"),
                html.Span(id="valueSnow", children="0%")
                ])
            ])
        ])

    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    db_conn = engine.connect()
    monthly_temp_data = []
    temp_date = []
    monthly_rain_data = []
    rain_date = []
    monthly_snow_data = []
    snow_date = []
    monthly_sunhours_data = []
    sunhours_date = []

    for year in range(2013, 2024):
        for month in range(1, 13):
            formatted_month = str(month).zfill(2)
            formatted_date = f"{year}.{formatted_month}"
            get_mean_temp(selected_country, year, formatted_month, db_conn, monthly_temp_data, temp_date, formatted_date)
            get_mean_rain(selected_country, year, formatted_month, db_conn, monthly_rain_data, rain_date, formatted_date)
            get_mean_snow(selected_country, year, formatted_month, db_conn, monthly_snow_data, snow_date, formatted_date)
            get_mean_sun(selected_country, year, formatted_month, db_conn, monthly_sunhours_data, sunhours_date, formatted_date)

            mean_temperature_df = pd.DataFrame({'date':temp_date, 'mean_temp_value':monthly_temp_data})
            mean_rainfall_df = pd.DataFrame({'date':rain_date, 'mean_rain_value':monthly_rain_data})
            mean_snowfall_df = pd.DataFrame({'date':snow_date, 'mean_snow_value':monthly_snow_data})
            mean_sunhours_df = pd.DataFrame({'date':sunhours_date, 'mean_sunhours_value':monthly_sunhours_data})

            mean_temperature_fig = px.line(mean_temperature_df,
                x='date' ,
                y='mean_temp_value',
                title=f"Mean temperature in {selected_country}",
            )

            mean_rainfall_fig = px.line(mean_rainfall_df,
                x='date' ,
                y='mean_rain_value',
                title=f"Mean rainfall in {selected_country}",
            )

            mean_snowfall_fig = px.line(mean_snowfall_df,
                x='date' ,
                y='mean_snow_value',
                title=f"Mean snowfall in {selected_country}",
            )

            mean_sunhours_fig = px.line(mean_sunhours_df,
                x='date' ,
                y='mean_sunhours_value',
                title=f"Mean sunhours in {selected_country}",
            )

    return temperature_fig, rain_fig, snow_fig, statistics_text, current_weather, mean_temperature_fig, mean_rainfall_fig, mean_snowfall_fig, mean_sunhours_fig


@app.callback(
    (Output("valueTemperature", "children"),
    Output("valueRain", "children"),
    Output("valueSnow", "children"),),
    Input("retrieve-button", "n_clicks"),
    Input("country-dropdown", "value")
)
def update_output(n_clicks, country):
    if n_clicks is not None and n_clicks > 0:
        # The button has been pressed
        latitude = weather_data.loc[weather_data['country'] == country]["latitude"].tolist()[0]
        longitude = weather_data.loc[weather_data['country'] == country]["longitude"].tolist()[0]
        api_string = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,rain,snowfall&forecast_days=1"
        final_string = api_string.format(latitude=latitude, longitude=longitude)
        r = requests.get(final_string)
        j = json.loads(r.text)
        temp_mean = j["current"]["temperature_2m"]
        rain = j["current"]["rain"]
        snow = j["current"]["snowfall"]
        return temp_mean, rain, snow
    else:
        return "", "",""



if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
