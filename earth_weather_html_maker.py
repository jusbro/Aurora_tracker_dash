import requests
from datetime import datetime, timedelta, timezone

def get_weather_by_zip(zip_code):
    # Step 1: Get the latitude and longitude for the given ZIP code using the ZIP Code API
    zip_api_url = f"http://api.zippopotam.us/us/{zip_code}"
    zip_response = requests.get(zip_api_url)
    
    if zip_response.status_code != 200:
        print("Error fetching data for the given ZIP code.")
        return
    
    zip_data = zip_response.json()
    latitude = zip_data['places'][0]['latitude']
    longitude = zip_data['places'][0]['longitude']
    
    # Step 2: Get the weather forecast for the location using the NWS API
    nws_api_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    nws_response = requests.get(nws_api_url)
    
    if nws_response.status_code != 200:
        print("Error fetching data from NWS API.")
        return
    
    nws_data = nws_response.json()
    forecast_url = nws_data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    
    if forecast_response.status_code != 200:
        print("Error fetching forecast data.")
        return
    
    forecast_data = forecast_response.json()
    periods = forecast_data['properties']['periods']
    
    # Get the next three days of weather conditions
    today = datetime.now(timezone.utc)  # Make 'today' an offset-aware datetime
    weather_forecast = []
    
    for period in periods:
        period_start = datetime.strptime(period['startTime'], '%Y-%m-%dT%H:%M:%S%z')
        if period_start >= today and period_start <= (today + timedelta(days=3)):
            weather_forecast.append({
                'name': period['name'],
                'startTime': period['startTime'],
                'endTime': period['endTime'],
                'temperature': period['temperature'],
                'temperatureUnit': period['temperatureUnit'],
                'detailedForecast': period['detailedForecast']
            })
    
    return weather_forecast

#Get the current radar image
def get_radar_image_url():
    
    # Construct the URL for the latest radar image
    radar_image_url = "https://radar.weather.gov/ridge/standard/KDIX_0.gif"

    return radar_image_url

# Create the Earth Weather Page HTML content
def generate_earth_weather_html(zip_code):
    # Get the weather forecast
    forecast = get_weather_by_zip(zip_code)

    # Create the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Earth Weather Forecast</title>
        <!-- Internal CSS to style the page -->
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <!-- Banner at the top with company logo and title -->
        <div class="banner">
            <img src="company_logo.jpg" alt="company_logo">
            <div class="page-title">Aurora Prediction Dashboard</div>
        </div>

        <!-- Button container with a button to navigate to another page -->
        <div class="button-container">
            <button onclick="location.href='Aurora_Dashboard.html'">Home</button>
            <button onclick="location.href='alerts.html'">Alerts & Warnings</button>
            <button onclick="location.href='extended_forcast.html'">Extended Forecast Details</button>
            <button onclick="location.href='earth_weather.html'">Earth Weather</button>
            <button onclick="location.href='drap.html'">Drap Forecast</button>
            <button onclick="location.href='about.html'">About</button>
        </div>
        <div class = "weather_image-container">
        <span class = "image-title"> Local Radar Local Clouds</span>
        <img src = "latest_radar_image.png" alt = "latest_radar_image.png">
        <img src = "latest_cloud_cover_image.jpg" alt = "latest_cloud_cover_image.jpg">
        <img src = "dark_cloud_cover_image.jpg" alt = "dark_cloud_cover_image.jpg">
        </div>
        <div class="page-header">
           Earth Weather Forecast 
        </div>
    """

    # Add weather forecast information to the HTML content
    html_content += "<div class='weather-forecast'>\n"
    html_content += "<table>\n"
    html_content += "<tr><th><span class = weather-title>Date</span></th><th><span class = weather-title>Temperature</span></th><th><span class = weather-title>Detailed Forecast</span></th></tr>\n"

    for day in forecast:
        html_content += f"<tr><td><span class = date-text>{day['name']}</span></td><td><span class = temperature-text>{day['temperature']}&deg;{day['temperatureUnit']}</span></td><td><span class = weather-text>{day['detailedForecast']}</span></td></tr>\n"
        html_content += "<tr><td colspan='3'><hr></td></tr>\n"
    html_content += "</table>\n"

    html_content += "</div>\n"

    # Add closing tags for HTML content
    html_content += """
</body>
    </html>
    """

    return html_content

# Example usage
zip_code = "19605"  # Replace with your desired ZIP code
earth_weather_html = generate_earth_weather_html(zip_code)

# Write HTML content to a file
with open("earth_weather.html", "w") as f:
    f.write(earth_weather_html)

print("Earth Weather HTML page generated successfully!")
