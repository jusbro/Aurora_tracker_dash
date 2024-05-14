# List of image filenames
image_files = ["kp_values.png", "swpc_notifications.png", "swpfc_overview.png", "drap_f10_global.png", "drap_f15_global.png", "drap_f20_global.png", "drap_f25_global.png", "drap_f30_global.png"]

# Define the text for each image
text = "Test Image, Test Information"

# Generate HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aurora Predictor Dashboard</title>
<style>
  /* CSS for responsive images */
  img {
    max-width: 100%;
    height: auto;
  }
  /* CSS for centering text */
  .image-container {
    text-align: center;
  }
  /* CSS for background color */
  body {
    background-color: #383737;
  }
</style>
</head>
<body>
"""

# Add image and text containers to HTML content
for filename in image_files:
    html_content += f"""
    <div class="image-container">
      <p>{text}</p>
      <img src="{filename}" alt="{filename}">
    </div>
    <br>
    """

# Close HTML content
html_content += """
</body>
</html>
"""

# Write HTML content to a file
with open("image_gallery.html", "w") as f:
    f.write(html_content)

print("HTML page generated successfully!")
