import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime
import requests
import json

from src.data_import import _load_data_to_db

# from components.layout import create_layout
# import components.callbacks
from src.data_fetching import (
    _fetch_capitals,
    _fetch_prod_data_from_db,
    _fetch_weather_data_from_db,
)

# load data to db
#_load_data_to_db()

weather_data = _fetch_weather_data_from_db()

capitals = weather_data["country"].unique()

app = dash.Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style={"width": "100%", "margin": "0 auto", "background-color": "#f8f9fa"},
    children=[
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(html.Label("Select Country", style={"color": "white", "text-align": "center"}),
                            style={"margin-left": "20px", "margin-right": "20px"}),
                dcc.Dropdown(
                    style={"width": "200px"},
                    id="capital-dropdown",
                    options=[
                        {
                            "label": capital,
                            "value": capital,
                        }
                        for capital in capitals
                    ],
                    value="Mariehamn",
                ),
                dbc.NavItem(html.Label("Select Analytics", style={"color": "white", "text-align": "center"}),
                            style={"margin-left": "20px", "margin-right": "20px"}),  # Adjust margins for spacing
                dcc.Dropdown(
                    style={"width": "200px"},
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
                            "label": "Summary",
                            "value": "summary",
                        },
                    ],
                    value="temp-time",
                ),
                dbc.NavItem(html.Label("Select Time-frame", style={"color": "white", "text-align": "center"}),
                            style={"margin-left": "20px", "margin-right": "20px"}),
                dcc.DatePickerRange(
                    id="date-range-picker",
                    start_date="2016-01-01",
                    end_date="2020-12-31",
                ),
            ],
            color="primary",
            dark=True,
        ),

        html.Div(
            style={"margin": "0 auto"},
            children=[
                dbc.Row(
                    [

                            html.Div(
                                children=[
                                    # Weather Analytics Block
                                    html.Div(
                                        style={"width": "100%", "margin": "0 auto"},
                                        children=[
                                            dbc.Row(
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                id="temperature-plot",
                                                                style={"display": "block"},
                                                            ),
                                                            dcc.Graph(
                                                                id="rain-plot",
                                                                style={"display": "none"},
                                                            ),
                                                            dcc.Graph(
                                                                id="snow-plot",
                                                                style={"display": "none"},
                                                            ),
                                                        ]
                                                    )
                                                )
                                            ),
                                            dbc.Row(
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            id="statistics",
                                                            style={"display": "none"},
                                                        ),
                                                        html.Div(
                                                            id="weather",
                                                            style={"display": "block"},
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ],
                                    ),
                                ],
                            )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                children=[
                                    # Add other analytics here
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
    Input("weather-analytics-dropdown", "value")
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
@app.callback(
    Output("statistics", "style"), Input("weather-analytics-dropdown", "value")
)
def update_graph_visibility(selected_option):
    if selected_option == "summary":
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
    ],
    [
        Input("capital-dropdown", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
    ],
)
def update_plots(selected_capital, start_date, end_date):
    # filter the data for the selected capital and date range
    # weather_data = _fetch_weather_data_from_db()
    aggregated_data = weather_data.groupby(['date','country', "longitude", "latitude"], as_index=False).mean(numeric_only=True)
    filtered_data = aggregated_data[
        (aggregated_data["country"] == selected_capital)
        & (aggregated_data["date"] >= start_date)
        & (aggregated_data["date"] <= end_date)
    ]

    # create a temperature line plot
    temperature_fig = px.line(
        filtered_data,
        x="date",
        y="temp_mean",
        title=f"Temperature in {selected_capital}",
    )

    # create a rainfall line plot
    rain_fig = px.line(
        filtered_data, x="date", y="rain", title=f"Rainfall in {selected_capital}"
    )

    # create a snowfall line plot
    snow_fig = px.line(
        filtered_data, x="date", y="snow", title=f"Snowfall in {selected_capital}"
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


    current_weather = dbc.Row(
        children=[
            dbc.Col(
                className="dashboard",
                children=[
                    dbc.Col(html.Div("Current Weather", className="header"), width="auto"),
                    dbc.Col(html.Button("Retrieve Now", className="btn btn-primary", id="retrieve-button"), width="auto"),
                ],
                width=3,
            ),
            dbc.Col(
                [
                    dbc.Row([html.Span("Temperature:"), html.Span(id="valueTemperature", children="72°F")]),
                    dbc.Row([html.Span("Rain:"), html.Span(id="valueRain", children="10%")]),
                    dbc.Row([html.Span("Snow:"), html.Span(id="valueSnow", children="0%")]),
                ],
                width=6,
            ),
        ]
    )


    return temperature_fig, rain_fig, snow_fig, statistics_text, current_weather


@app.callback(
    (Output("valueTemperature", "children"),
    Output("valueRain", "children"),
    Output("valueSnow", "children"),),
    Input("retrieve-button", "n_clicks"),
    Input("capital-dropdown", "value")
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
