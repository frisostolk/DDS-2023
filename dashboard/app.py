import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# from components.layout import create_layout
# import components.callbacks
from src.data_fetching import (
    _fetch_capitals,
    _fetch_prod_data_from_db,
    _fetch_weather_data_from_db,
)

weather_data = _fetch_weather_data_from_db()

capitals = weather_data["capital"].unique()

app = dash.Dash(__name__)

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
                                                                    "Select a capital:"
                                                                ),
                                                                dcc.Dropdown(
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
                                children=[
                                    # Add agricultural prod data here
                                ]
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
    Output("temperature-plot", "style"), Input("weather-analytics-dropdown", "value")
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

    return temperature_fig, rain_fig, snow_fig, statistics_text


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
