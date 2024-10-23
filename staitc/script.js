function fetchWeatherData() {
    fetch('/')
        .then(response => response.text())
        .then(data => {
            // Replace the content of the body with the new data
            document.body.innerHTML = data;
        })
        .catch(error => console.error('Error fetching weather data:', error));
}

// Fetch weather data every 5 minutes (300000 milliseconds)
setInterval(fetchWeatherData, 300000);

// Optionally, you can call it once immediately when the page loads to fetch the initial data
fetchWeatherData();
