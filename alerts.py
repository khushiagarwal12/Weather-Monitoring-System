import pandas as pd
import random
import time

# Sample data simulation function
def simulate_weather_data():
    # This function simulates weather data for different cities
    cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    data = []
    for city in cities:
        # Randomly generating weather data
        temp = random.uniform(25, 40)  # Random temperature between 25 and 40 degrees Celsius
        feels_like = temp + random.uniform(-2, 2)  # Feels like temperature
        humidity = random.randint(30, 100)  # Humidity percentage
        wind_speed = random.uniform(0, 5)  # Wind speed in m/s
        visibility = random.randint(1000, 10000)  # Visibility in meters
        data.append([city, temp, feels_like, humidity, wind_speed, visibility])
    return pd.DataFrame(data, columns=['city', 'temp', 'feels_like', 'humidity', 'wind_speed', 'visibility'])

# Function to check alerts based on thresholds
def check_alerts(df, temp_threshold):
    alerts = []
    for index, row in df.iterrows():
        if row['temp'] > temp_threshold:
            alerts.append(f"ALERT: {row['city']} - Temperature {row['temp']:.2f}°C exceeds the threshold of {temp_threshold}°C.")
    return alerts

# User-defined thresholds
TEMP_THRESHOLD = 35  # Temperature threshold in degrees Celsius
consecutive_updates_required = 2
consecutive_alerts = 0

# Main monitoring loop
while True:
    # Simulate weather data
    weather_data = simulate_weather_data()
    print("Current Weather Data:\n", weather_data)

    # Check for alerts
    alerts = check_alerts(weather_data, TEMP_THRESHOLD)

    if alerts:
        consecutive_alerts += 1
        for alert in alerts:
            print(alert)
    else:
        consecutive_alerts = 0

    # Trigger an alert if the temperature exceeds the threshold for consecutive updates
    if consecutive_alerts >= consecutive_updates_required:
        print("ALERT: Temperature has exceeded the threshold for consecutive updates!")
        consecutive_alerts = 0  # Reset after triggering alert

    # Sleep for a specific interval before the next update
    time.sleep(10)  # Adjust the time interval as needed
