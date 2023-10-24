import dash
from components.layout import create_layout
from src.data_fetching import (
    _fetch_capitals,
    _fetch_prod_data_from_db,
    _fetch_weather_data_from_db,
)

weather_data = _fetch_weather_data_from_db()

app = dash.Dash(__name__)

app.layout = create_layout(weather_data=weather_data)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
