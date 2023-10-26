from dash import html
from dash import dcc
from my_dash_app.maindash import app
from dash.dependencies import Input, Output, State


# Define the layout of your app
def create_layout(weather_data):
    capitals = weather_data["capital"].unique()

    return html.Div(
        style={},
        children=[
            html.H1("Agriculture Dashboard"),
            html.Div(
                style={},
                children=[
                    html.Label("Select a capital:"),
                    dcc.Dropdown(
                        id="capital-dropdown",
                        options=[
                            {"label": capital, "value": capital} for capital in capitals
                        ],
                        value="Mariehamn",
                    ),
                    html.Label("Select a date range:"),
                    dcc.DatePickerRange(
                        id="date-range-picker",
                        start_date="2016-01-01",
                        end_date="2020-12-31",
                    ),
                    html.Label("Select Analytics"),
                    dcc.Dropdown(
                        id="weather-analytics-dropdown",
                        options=[
                            {"label": "Temperature Time Series", "value": "temp-time"},
                            {"label": "Rainfall Time Series", "value": "rain-time"},
                            {"label": "Snowfall Time Series", "value": "snow-time"},
                            {"label": "Summary", "value": "summary"},
                        ],
                        value="temp-time",
                    ),
                    dcc.Graph(id="temperature-plot", style={"display": "block"}),
                    dcc.Graph(id="rain-plot", style={"display": "none"}),
                    dcc.Graph(id="snow-plot", style={"display": "none"}),
                    html.Div(id="statistics", style={"display": "none"}),
                ],
            ),
            # Hidden Div used to store initial data load
            html.Div(id="initial-data", style={"display": "none"}),
            dcc.Interval(
                id="app-initialization", interval=1, n_intervals=0, disabled=False
            ),
        ],
    )


