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
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

from src.data_import import _load_data_to_db

# from components.layout import create_layout
# import components.callbacks
from src.data_fetching import (
    _fetch_countries,
    _fetch_prod_data_from_db,
    _fetch_weather_data_from_db,
    _fetch_nutrient_data,
    _fetch_emission_data,
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

data = pd.read_csv('../data/weather/weather.csv')

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
                                                                    value="Netherlands",
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
                                                                        # {
                                                                        #     "label": "Summary",
                                                                        #     "value": "summary",
                                                                        # },
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
                                                        style={"display": "block"},
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
                                    # Production Analytics
                                    html.Label("Select Country:"),
                                    dcc.Dropdown(
                                        id="country-dropdown-prod",
                                        options=[
                                            {"label": country, "value": country}
                                            for country in agri_data["Country"].unique()
                                            if pd.notna(country)
                                        ],
                                        value=agri_data["Country"].iloc[
                                            0
                                        ],  # Default selected value
                                        multi=False,
                                    ),
                                    html.Label("Select Types:"),
                                    dcc.Dropdown(
                                        id="type-dropdown",
                                        options=[
                                            {"label": data_type, "value": data_type}
                                            for data_type in agri_data["Type"].unique()
                                            if pd.notna(data_type)
                                        ],
                                        value=agri_data[
                                            "Type"
                                        ].unique(),  # Default selected value (all types)
                                        multi=True,  # Allow multiple selections
                                    ),
                                    dcc.Graph(id="line-chart"),
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
                                    # EU map analytics
                                    html.H4("Agricultural Indicators"),
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
                                            {"label": "2010", "value": "2010"},
                                            {"label": "2011", "value": "2011"},
                                            {"label": "2012", "value": "2012"},
                                            {"label": "2013", "value": "2013"},
                                            {"label": "2014", "value": "2014"},
                                            {"label": "2015", "value": "2015"},
                                            {"label": "2016", "value": "2016"},
                                            {"label": "2017", "value": "2017"},
                                            {"label": "2018", "value": "2018"},
                                            {"label": "2019", "value": "2019"},
                                            {"label": "2020", "value": "2020"},
                                            {"label": "2021", "value": "2021"},
                                        ],
                                        value="2021",
                                    ),
                                    dcc.Graph(id="choropleth-maps-x-graph"),
                                ]
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            html.Div(
                                children=[
                                    # regression Analytics
                                    html.Label("Select Country:"),
                                    dcc.Dropdown(
                                        id="country-dropdown-regression",
                                        options=[
                                            {"label": country, "value": country}
                                            for country in agri_data["Country"].unique()
                                            if pd.notna(country)
                                        ],
                                        value=agri_data["Country"].iloc[
                                            0
                                        ],  # Default selected value
                                        multi=False,
                                    ),
                                    html.Label("Select Type:"),
                                    dcc.Dropdown(
                                        id="type-dropdown-regression",
                                        options=[
                                            {"label": data_type, "value": data_type}
                                            for data_type in agri_data["Type"].unique()
                                            if pd.notna(data_type)
                                        ],
                                        value='Cereals',
                                        multi=False,  # Allow multiple selections
                                    ),
                                    html.Label("Select average rain, maximum temperature, minimum temperature and snow of 2023 to predict the production on:"),
                                    dcc.Input(
                                        id="selected_rain",
                                        type = 'number',
                                        placeholder='rain',
                                        value = 0,
                                    ),
                                    dcc.Input(
                                        id="selected_max",
                                        type = 'number',
                                        placeholder='max temperature',
                                        value = 0,
                                    ),
                                    dcc.Input(
                                        id="selected_min",
                                        type = 'number',
                                        placeholder='min temperature',
                                        value= 0,
                                    ),
                                    dcc.Input(
                                        id="selected_snow",
                                        type = 'number',
                                        placeholder='snow',
                                        value=0,
                                    ),
                                    dcc.Graph(id="line-chart-regression"),
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
                                ]
                            ),
                            width=6,
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
        Output("temperature-plot", "figure"),
        Output("rain-plot", "figure"),
        Output("snow-plot", "figure"),
        Output("statistics", "children"),
    ],
    [
        Input("country-dropdown", "value"),
        Input("date-range-picker", "start_date"),
        Input("date-range-picker", "end_date"),
    ],
)
def update_plots(selected_country, start_date, end_date):
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

    # I had to comment the current weather out, it needs to be incorporated into the layout, and use callbacks when the button is pressed
    # havent gotten around to implementing it myself

    # current_weather = html.Div(
    #     [
    #         html.Div(
    #             className="dashboard",
    #             children=[
    #                 html.Div(className="header", children="Current Weather"),
    #                 html.Button(
    #                     "Retrieve Now", className="button", id="retrieve-button"
    #                 ),
    #                 html.Div(
    #                     className="row",
    #                     children=[
    #                         html.Span(className="label", children="Temperature:"),
    #                         html.Span(id="valueTemperature", children="72°F"),
    #                     ],
    #                 ),
    #                 html.Div(
    #                     className="row",
    #                     children=[
    #                         html.Span(className="label", children="Rain:"),
    #                         html.Span(id="valueRain", children="10%"),
    #                     ],
    #                 ),
    #                 html.Div(
    #                     className="row",
    #                     children=[
    #                         html.Span(className="label", children="Snow:"),
    #                         html.Span(id="valueSnow", children="0%"),
    #                     ],
    #                 ),
    #             ],
    #         )
    #     ]
    # )

    return (
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
    [Input("country-dropdown-prod", "value"), Input("type-dropdown", "value")]
)
def update_line_chart(selected_country, selected_types):
    # Filter data based on selected country and types
    filtered_df = agri_data[
        (agri_data["Country"] == selected_country)
        & (agri_data["Type"].isin(selected_types))
    ]

    # Create traces for each selected type
    traces = []
    for data_type in selected_types:
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

    # Return the Figure object
    return dict(data=traces, layout=layout)


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
    [Input("country-dropdown-regression", "value"), Input("type-dropdown-regression", "value"),Input('selected_rain','value'), Input('selected_min','value'), Input('selected_max','value'), Input('selected_snow','value')]
)
def update_regression_chart(selected_country, selected_type,selected_rain,selected_min,selected_max,selected_snow):

    y_train=[]
    filtered_df = agri_data[(agri_data['Country'] == selected_country) & (agri_data['Type'].isin([selected_type]))]
    y_train = np.array(filtered_df['Value'])
    y_train= y_train[0:10]

    filtered_data_weather = data[(data['country'] == selected_country)]
    pd.options.mode.chained_assignment = None  # default='warn'
    filtered_data_weather[['Year','Month','Day']] = filtered_data_weather['date'].str.split('-',expand=True)

    #Fill train data with mean maxtemp, mintemp, snow and rain per year. But not 2023
    X_train = []
    for i in filtered_data_weather['Year'].unique():
        if i == '2023':
            break
        X_train.append([np.mean(filtered_data_weather[filtered_data_weather['Year'] == i]['rain']),
        np.mean(filtered_data_weather[filtered_data_weather['Year'] == i]['temp_max']),
        np.mean(filtered_data_weather[filtered_data_weather['Year'] == i]['temp_min']),
        np.mean(filtered_data_weather[filtered_data_weather['Year'] == i]['snow'])])
    X_train = np.array(X_train)

    model = LinearRegression()
    model.fit(X_train, y_train)
    new_data = np.array([selected_rain, selected_min,selected_max,selected_snow]).reshape(1,-1)
    # Make predictions on the new data
    new_prediction = model.predict(new_data)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['Year'],y=filtered_df['Value'] ,mode='markers', name='Prodcution'))
    fig.add_trace(go.Scatter(x=['2023'], y=new_prediction, mode='markers', name='Prediction'))
    fig.update_layout(
    title=(f"Prediction of {selected_type} production in {selected_country} for 2023"),
    xaxis_title="Year",
    yaxis_title="Production",

)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
