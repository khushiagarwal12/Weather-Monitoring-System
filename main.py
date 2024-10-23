from flask import Flask, render_template
from weather import fetch_weather_data, CITIES  # Import CITIES from weather.py

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch weather data and alerts
    weather_data, alerts, summaries = fetch_weather_data()
    return render_template('weather.html', weather=weather_data, cities=CITIES, alerts=alerts, summaries=summaries)  # Pass summaries to the template

if __name__ == '__main__':
    app.run(debug=True)
