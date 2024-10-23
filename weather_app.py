from flask import Flask, render_template
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# List of cities to fetch weather data for
CITIES = ["London", "New York", "Tokyo"]  # Add your cities here
API_KEY = "96d0057da2cc9e10b7120f3d9c4ff215"  # Replace with your OpenWeatherMap API key

# Function to fetch weather data
def fetch_weather_data():
    weather_data = {}
    for city in CITIES:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        if response.status_code == 200:
            data = response.json()
            weather_data[city] = {
                "temp": data['main']['temp'],
                "feels_like": data['main']['feels_like'],
                "condition": data['weather'][0]['description'],
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # Append data to CSV
            append_to_csv(city, weather_data[city])
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
    return weather_data

# Function to append data to a CSV file
def append_to_csv(city, data):
    df = pd.DataFrame([{
        "City": city,
        "Temperature (°C)": data['temp'],
        "Feels Like (°C)": data['feels_like'],
        "Condition": data['condition'],
        "Last Updated": data['last_updated']
    }])
    
    # Append data to CSV, creating the file if it doesn't exist
    df.to_csv('weather_data.csv', mode='a', header=not pd.io.common.file_exists('weather_data.csv'), index=False)

@app.route('/')
def index():
    weather = fetch_weather_data()
    return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
