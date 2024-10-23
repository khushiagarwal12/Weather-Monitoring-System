import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the data from CSV
df = pd.read_csv('weather_data.csv')

# Step 2: Ensure 'last_updated' is in datetime format
df['last_updated'] = pd.to_datetime(df['last_updated'])

# Step 3: Filter data for the desired date
date_filter = '2024-10-23'  # Set the desired date
df_filtered = df[df['last_updated'].dt.date == pd.to_datetime(date_filter).date()]

# Step 4: Verify filtered data
if df_filtered.empty:
    print(f"No data available for the date: {date_filter}")
else:
    print(f"Data available for the date: {date_filter}")

# Step 5: Plotting the weather metrics for each city

plt.figure(figsize=(14, 10))

# Loop through the numeric columns for visualization
numeric_columns = ['temp', 'feels_like', 'humidity', 'wind_speed', 'visibility']
titles = [
    'Temperature (°C)',
    'Feels Like Temperature (°C)',
    'Humidity (%)',
    'Wind Speed (m/s)',
    'Visibility (km)'
]

# Create subplots for each numeric column
for i, column in enumerate(numeric_columns):
    plt.subplot(3, 2, i + 1)
    if column == 'visibility':
        plt.bar(df_filtered['city'], df_filtered[column] / 1000, color='red')  # Convert visibility to km
        plt.ylabel('Visibility (km)')
    else:
        plt.bar(df_filtered['city'], df_filtered[column], color='orange' if column == 'temp' else 'blue' if column == 'feels_like' else 'green')
        plt.ylabel(column.capitalize())
    
    plt.title(f"{titles[i]} on {date_filter}")
    plt.xlabel('City')
    plt.xticks(rotation=45)

# Adjust layout and show plots
plt.tight_layout()
plt.show()
