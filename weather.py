import requests
import sqlite3
import pandas as pd
from datetime import datetime

API_KEY = '96d0057da2cc9e10b7120f3d9c4ff215'  # Replace with your actual OpenWeather API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
TEMP_THRESHOLD = 35  # Define the temperature threshold for alerts

def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS weather_history ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            city TEXT, 
            temp REAL, 
            feels_like REAL, 
            condition TEXT, 
            humidity REAL, 
            wind_speed REAL, 
            visibility REAL, 
            last_updated TEXT 
        ) 
    ''')
    conn.commit()
    conn.close()

def save_weather_data(city, temp, feels_like, condition, humidity, wind_speed, visibility):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather_history (city, temp, feels_like, condition, humidity, wind_speed, visibility, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (city, temp, feels_like, condition, humidity, wind_speed, visibility, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def append_to_csv(city, temp, feels_like, condition, humidity, wind_speed, visibility):
    data = {
        'city': city,
        'temp': temp,
        'feels_like': feels_like,
        'condition': condition,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'visibility': visibility,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([data])
    df.to_csv('weather_data.csv', mode='a', header=not pd.io.common.file_exists('weather_data.csv'), index=False)

def fetch_weather_data():
    create_db()
    weather_data = {}
    alerts = []  # Store alerts here
    for city in CITIES:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            condition = data['weather'][0]['main']
            humidity = data['main']['humidity']  
            wind_speed = data['wind']['speed']  
            visibility = data.get('visibility', 'N/A')  
            last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Check if temperature exceeds threshold and create an alert
            if temp > TEMP_THRESHOLD:
                alerts.append(f"ALERT: {city} - Temperature {temp:.2f}°C exceeds the threshold of {TEMP_THRESHOLD}°C.")

            # Save to the database
            save_weather_data(city, temp, feels_like, condition, humidity, wind_speed, visibility)

            # Append to CSV
            append_to_csv(city, temp, feels_like, condition, humidity, wind_speed, visibility)

            # Store data for the city
            weather_data[city] = {
                'temp': temp,
                'feels_like': feels_like,
                'condition': condition,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'visibility': visibility,
                'last_updated': last_updated
            }
        else:
            print(f"Error fetching data for {city}: {response.status_code}")

    # Calculate average, max, min temperatures and dominant condition for each city
    summaries = {}
    for city, data in weather_data.items():
        summaries[city] = {
            'avg_temp': data['temp'],  # You might adjust this if you want to calculate across multiple fetches
            'max_temp': data['temp'],
            'min_temp': data['temp'],
            'dominant_condition': data['condition'],
        }
        
    return weather_data, alerts, summaries  # Return summaries along with weather data
