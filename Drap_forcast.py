import os
import requests

# Define the base URL parts for the image
base_image_url = "https://services.swpc.noaa.gov/images/drap_f"
base_image_url_ending = "_global.png"

# Get the current working directory
current_directory = os.getcwd()

# Define the starting value for the counter
counter = 5

# Loop through the desired frequencies (5 MHz to 35 MHz, increasing by 5 MHz)
while counter <= 30:
    # Construct the full URL for the image
    image_url = f"{base_image_url}{counter}{base_image_url_ending}"

    # Define the filename for the image
    image_filename = os.path.join(current_directory, f"drap_f{counter}_global.png")

    # Send a GET request to fetch the image
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary write mode and save the image
        with open(image_filename, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully saved as {image_filename}")
    else:
        print(f"Failed to retrieve image for {counter} MHz. HTTP status code: {response.status_code}")

    # Increment the counter by 5 for the next frequency
    counter += 5
