import os
import requests

# Define the URL for the image
image_url = "https://services.swpc.noaa.gov/images/swx-overview-large.gif"

# Get the current working directory
current_directory = os.getcwd()

# Define the filename for the image
image_filename = os.path.join(current_directory, 'swpc_overview.png')

# Send a GET request to fetch the image
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode and save the image
    with open(image_filename, 'wb') as file:
        file.write(response.content)
    print(f"Image successfully saved as {image_filename}")
else:
    print(f"Failed to retrieve image. HTTP status code: {response.status_code}")
