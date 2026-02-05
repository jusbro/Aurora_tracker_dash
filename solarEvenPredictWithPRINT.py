import os
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image
import time

uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3)
printer = ThermalPrinter(uart)

# Get the current working directory
current_directory = os.getcwd()

# Define the filename for the image
image_filename = os.path.join(current_directory, 'kp_values.png')

# Define the URL for the JSON data
url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"

#setup the highest Kp value for the next three days
highest_kp_today = 0
highest_kp_tomorrow = 0
highest_kp_day_after_tomorrow = 0


# Define a function to map Kp values to colors
def map_kp_to_color(kp):
    if kp < 5:
        return 'green'
    elif 5 <= kp < 6:
        return 'yellow'
    elif 6 <= kp < 7:
        return 'gold'
    elif 7 <= kp < 8:
        return 'orange'
    elif 8 <= kp < 9:
        return 'red'
    else:
        return 'darkred'

try:
    #Get today's date yyyy-mm-dd
    today = datetime.today().date()
    print(today)

    #Get tomorrow's date
    tomorrow = today + timedelta(days=1)
    print(tomorrow)
    #Get the day after tomorrow's date
    day_after_tomorrow = today + timedelta(days=2)

    print
    # Send a GET request to fetch the JSON data
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract data for plotting
        timestamps = []
        kp_values = []
        colors = []

        # Initialize variables to track the highest probability of Aurora
        highest_kp = 0
        highest_kp_time = None

        # Initialize the previous date
        prev_date = None

        # Define time zones for UTC and EST
        utc_timezone = pytz.timezone('UTC')
        est_timezone = pytz.timezone('US/Eastern')

        # Skip the header row (data[0]) and process the rest of the data
        for entry in data[1:]:
                    # Check if the current Kp value is higher than the previous highest for each day

            time_str = entry[0]
            kp = float(entry[1])
            current_date_utc = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            current_date_est = current_date_utc.astimezone(est_timezone)

            if current_date_est.date() != prev_date:
                timestamps.append(current_date_est)
                kp_values.append(kp)
                colors.append(map_kp_to_color(kp))
                prev_date = current_date_est.date()
            else:
                timestamps.append(current_date_est)
                kp_values.append(kp)
                colors.append(map_kp_to_color(kp))

            # Check if the current Kp value is higher than the previous highest
            if kp > highest_kp:
                highest_kp = kp
                highest_kp_time = current_date_est
                    # Check if the current Kp value is higher than the previous highest for each day
            if current_date_est.date() == today:
                if kp > highest_kp_today:
                    highest_kp_today = kp
            elif current_date_est.date() == tomorrow:
                if kp > highest_kp_tomorrow:
                    highest_kp_tomorrow = kp
            elif current_date_est.date() == day_after_tomorrow:
                if kp > highest_kp_day_after_tomorrow:
                    highest_kp_day_after_tomorrow = kp

        # Get colors for the highest Kp values for each day
        color_today = map_kp_to_color(highest_kp_today)
        color_tomorrow = map_kp_to_color(highest_kp_tomorrow)
        color_day_after_tomorrow = map_kp_to_color(highest_kp_day_after_tomorrow)

        # Print the colors for today, tomorrow, and the day after tomorrow to the terminal
        print(f"Today: {color_today.capitalize()} Highest Kp: {highest_kp_today}")
        print(f"Tomorrow: {color_tomorrow.capitalize()} Highest Kp: {highest_kp_tomorrow}")
        print(f"Day After Tomorrow: {color_day_after_tomorrow.capitalize()} Highest Kp: {highest_kp_day_after_tomorrow}")
        # Create the bar graph with removed lines and double-width columns
        plt.figure(figsize=(12, 6), dpi=100)
        plt.bar(timestamps, kp_values, color=colors, width=0.1, )  # Adjust width as needed (doubled)
        plt.title('Planetary K-index (Kp) Forecast', fontsize=26)
        plt.xlabel('Date and Time (EST)', fontsize=12)
        plt.ylabel('Kp Value', fontsize=18)
        plt.grid(axis='y', linestyle='--', alpha=0.7)  # Remove vertical grid lines
        plt.ylim(0, 9)
        plt.xticks(rotation=45)

        # Set x-axis labels to display the date only on the first data point of a day
        date_labels = [timestamp.strftime('%m-%d') if timestamp.hour == 0 else "" for timestamp in timestamps]
        plt.xticks(timestamps, date_labels)

        plt.tight_layout()

        # Display the highest probability of Aurora below the graph
        if highest_kp_time:
            highest_kp_text = f"The highest probability of Aurora will occur on {highest_kp_time.strftime('%Y-%m-%d')} at {highest_kp_time.strftime('%H:%M')} EST"
            plt.text(0.5, -0.15, highest_kp_text, fontsize=18, ha="center", transform=plt.gca().transAxes)
        plt.axhline(y=7.2, color='r', linestyle='--',label="Minimum Kp for Aurora to be possible in Hamburg, PA.", linewidth=2)  # Add a horizontal line at Kp = 5
        plt.legend(loc='upper left', fontsize=16)

        # Save the figure as a .png file with the name kp_values.png in the same directory as the script
        plt.savefig(image_filename)

    else:
        print(f"HTTP error: {response.status_code}")

except requests.exceptions.RequestException as req_err:
    print(f"Request error: {req_err}")

try:
    printer.print("Hello World")
except requests.exceptions.RequestException as req_err:
    print(f"Request Error: {req_err}")
