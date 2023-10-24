import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
from src.data_fetching import _fetch_weather_data_from_db, _fetch_capitals

from app import app

weather_data = app.weather_data


# App load callback
@app.callback(
    Output("app-initialization", "disabled"),
    Input("app-initialization", "n_intervals"),
)
def disable_initialization(n_intervals):
    return True  # This will disable the interval after the first run


# Initial data load
@app.callback(
    Output("initial-data", "children"),
    Input("app-initialization", "n_clicks"),
    State("initial-data", "children"),
)
def load_initial_data_callback(n_clicks, existing_data):
    if n_clicks is None:  # This callback only runs once at app initialization
        weather_data = _fetch_weather_data_from_db()
        return weather_data
    return existing_data


# Callback to populate capitals dropdown list
@app.callback(
    Output("capital-dropdown", "options"),
    Input("app-initialization", "n_clicks"),
)
def update_capitals_dropdown(app_initialization):
    capitals = _fetch_capitals
    options = [{"label": capital, "value": capital} for capital in capitals]
    return options


# Weather - Temperature timeseries callback
@app.callback(Output("temperature-plot", "style"), Input("dropdown", "value"))
def update_graph_visibility(selected_option):
    if selected_option == "temp-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Weather - Rainfall timeseries callback
@app.callback(Output("rain-plot", "style"), Input("dropdown", "value"))
def update_graph_visibility(selected_option):
    if selected_option == "rain-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Weather - Snowfall timeseries callback
@app.callback(Output("snow-plot", "style"), Input("dropdown", "value"))
def update_graph_visibility(selected_option):
    if selected_option == "snow-time":
        return {"display": "block"}
    else:
        return {"display": "none"}


# Weather - Summary statistics callback
@app.callback(Output("statistics", "style"), Input("dropdown", "value"))
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
    ],  # output for statistics
    [
        Input("capital-dropdown", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
    ],
)
def update_plots(selected_capital, start_date, end_date):
    # filter the data for the selected capital and date range
    weather_data = _fetch_weather_data_from_db()

    filtered_data = weather_data[
        (weather_data["capital"] == selected_capital)
        & (weather_data["date"] >= start_date)
        & (weather_data["date"] <= end_date)
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
            html.P(f"Mean Temperature: {mean_temp:.2f}°C"),
            html.P(f"Max Temperature: {max_temp:.2f}°C"),
            html.P(f"Min Temperature: {min_temp:.2f}°C"),
            html.P(f"Mean Rainfall: {mean_rain:.2f} mm"),
            html.P(f"Max Rainfall: {max_rain:.2f} mm"),
            html.P(f"Min Rainfall: {min_rain:.2f} mm"),
            html.P(f"Mean Snowfall: {mean_snow:.2f} mm"),
            html.P(f"Max Snowfall: {max_snow:.2f} mm"),
            html.P(f"Min Snowfall: {min_snow:.2f} mm"),
        ]
    )

    return temperature_fig, rain_fig, snow_fig, statistics_text
