import serial
import adafruit_thermal_printer
from PIL import Image

# Set up the printer
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
printer = ThermalPrinter(uart)

# Load your PNG
img = Image.open("logo.png")

# Convert to black and white
img = img.convert("1")  # 1-bit B/W

# Resize to printer width (384 for 2.25" printer)
printer_width = 384
wpercent = (printer_width / float(img.width))
hsize = int((float(img.height) * float(wpercent)))
img = img.resize((printer_width, hsize))

# Center image (optional)
canvas = Image.new("1", (printer_width, img.height), 1)  # 1=white background
canvas.paste(img, (0, 0))
img = canvas

# Print image line by line
pixels = img.load()
for y in range(img.height):
    row = []
    for x in range(img.width):
        row.append(0 if pixels[x, y] == 0 else 1)  # 0=black, 1=white
    printer.bitImage(row, img.width)  # send each row
printer.feed(3)
