import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from sqlalchemy import create_engine, text, inspect, Table
from data_processing import _load_data_to_db


# Fetch the hardcoded population table from the database
def _fetch_prod_data_from_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    agri_prod = pd.read_sql_table("production", engine, index_col="index")
    return agri_prod


def _fetch_weather_data_from_db():
    engine = create_engine("postgresql://student:infomdss@db_dashboard:5432/dashboard")
    weather = pd.read_sql_table("weather", engine, index_col="index")
    return weather


# Load the data into the database
# You will do this asynchronously as a cronjob in the background of your application
# Or you fetch the data from different sources when the page is visited or how you like to fetch your data
# Notice that the method _load_data_to_db() now just reads a preloaded .csv file
# You will have to fetch external files, or call API's to fill your database

# _load_data_to_db()

app = dash.Dash(__name__)

# weather = _fetch_weather_data_from_db()

# capitals = weather["capital"].unique()

app.layout = html.Div(
    style={},
    children=[
        html.H1("Agriculture Dashboard"),
        # html.Div(
        #     style={},
        #     children=[
        #         html.Label("Select a capital:"),
        #         dcc.Dropdown(
        #             id="capital-dropdown",
        #             options=[
        #                 {"label": capital, "value": capital} for capital in capitals
        #             ],
        #             value="Mariehamn",
        #         ),
        #         html.Label("Select a date range:"),
        #         dcc.DatePickerRange(
        #             id="date-range-picker",
        #             start_date="2016-01-01",
        #             end_date="2020-12-31",
        #         ),
        #         html.Label("Select Analytics"),
        #         dcc.Dropdown(
        #             id="weather-analytics-dropdown",
        #             options=[
        #                 {"label": "Temperature Time Series", "value": "temp-time"},
        #                 {"label": "Rainfall Time Series", "value": "rain-time"},
        #                 {"label": "Snowfall Time Series", "value": "snow-time"},
        #                 {"label": "Summary", "value": "summary"},
        #             ],
        #         ),
        #         dcc.Graph(id="temperature-plot"),
        #         dcc.Graph(id="rain-plot"),
        #         dcc.Graph(id="snow-plot"),
        #         html.Div(id="statistics"),  # container for statistics
        #     ],
        # ),
        # html.Div(style={}, children=[]),
    ],
)

# app.layout = html.Div(
#     [
#         html.H1("Agriculture Dashboard"),
#         html.Label("Select a capital:"),
#         dcc.Dropdown(
#             id="capital-dropdown",
#             options=[{"label": capital, "value": capital} for capital in capitals],
#             value="Mariehamn",
#         ),
#         html.Label("Select a date range:"),
#         dcc.DatePickerRange(
#             id="date-range-picker", start_date="2016-01-01", end_date="2020-12-31"
#         ),
#         dcc.Graph(id="temperature-plot"),
#         dcc.Graph(id="rain-plot"),
#         dcc.Graph(id="snow-plot"),
#         html.Div(id="statistics"),  # container for statistics
#     ]
# )

# app.layout = html.Div(
#     [
#         html.H1("Weather Data"),
#         html.Label("Select a capital:"),
#         dcc.Dropdown(
#             id="capital-dropdown",
#             options=[{"label": capital, "value": capital} for capital in capitals],
#             value="Mariehamn",
#         ),
#         html.Label("Select a date range:"),
#         dcc.DatePickerRange(
#             id="date-range-picker", start_date="2016-01-01", end_date="2020-12-31"
#         ),
#         dcc.Graph(id="temperature-plot"),
#         dcc.Graph(id="rain-plot"),
#         dcc.Graph(id="snow-plot"),
#         html.Div(id="statistics"),  # container for statistics
#     ]
# )


# @app.callback(
#     [
#         Output("temperature-plot", "figure"),
#         Output("rain-plot", "figure"),
#         Output("snow-plot", "figure"),
#         Output("statistics", "children"),
#     ],  # output for statistics
#     [
#         Input("capital-dropdown", "value"),
#         Input("date-range-picker", "start_date"),
#         Input("date-range-picker", "end_date"),
#     ],
# )
# def update_plots(selected_capital, start_date, end_date):
#     # filter the data for the selected capital and date range
#     filtered_data = weather[
#         (weather["capital"] == selected_capital)
#         & (weather["date"] >= start_date)
#         & (weather["date"] <= end_date)
#     ]

#     # create a temperature line plot
#     temperature_fig = px.line(
#         filtered_data,
#         x="date",
#         y="temp_mean",
#         title=f"Temperature in {selected_capital}",
#     )

#     # create a rainfall line plot
#     rain_fig = px.line(
#         filtered_data, x="date", y="rain", title=f"Rainfall in {selected_capital}"
#     )

#     # create a snowfall line plot
#     snow_fig = px.line(
#         filtered_data, x="date", y="snow", title=f"Snowfall in {selected_capital}"
#     )

#     # calculate statistics not needed but I was just interesting in these statistics
#     mean_temp = filtered_data["temp_mean"].mean()
#     max_temp = filtered_data["temp_mean"].max()
#     min_temp = filtered_data["temp_mean"].min()

#     mean_rain = filtered_data["rain"].mean()
#     max_rain = filtered_data["rain"].max()
#     min_rain = filtered_data["rain"].min()

#     mean_snow = filtered_data["snow"].mean()
#     max_snow = filtered_data["snow"].max()
#     min_snow = filtered_data["snow"].min()

#     # create statistics text
#     statistics_text = html.Div(
#         [
#             html.H2("Statistics"),
#             html.P(f"Mean Temperature: {mean_temp:.2f}°C"),
#             html.P(f"Max Temperature: {max_temp:.2f}°C"),
#             html.P(f"Min Temperature: {min_temp:.2f}°C"),
#             html.P(f"Mean Rainfall: {mean_rain:.2f} mm"),
#             html.P(f"Max Rainfall: {max_rain:.2f} mm"),
#             html.P(f"Min Rainfall: {min_rain:.2f} mm"),
#             html.P(f"Mean Snowfall: {mean_snow:.2f} mm"),
#             html.P(f"Max Snowfall: {max_snow:.2f} mm"),
#             html.P(f"Min Snowfall: {min_snow:.2f} mm"),
#         ]
#     )

#     return temperature_fig, rain_fig, snow_fig, statistics_text


if __name__ == "__main__":
    app.run_server(
        debug=True, port=8053
    )  # port=8053 was needed to run the code on my laptop
