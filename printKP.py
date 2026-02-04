import serial
import adafruit_thermal_printer
from PIL import Image
from adafruit_thermal_printer import ThermalPrinter

# Set up serial connection
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

# Initialize printer
printer = ThermalPrinter(uart, cooling_factor=2.69)

# Load the image
img = Image.open("logo.png")

# Convert to 1-bit black and white
img = img.convert("1")

# Resize to printer width (384 dots for 2.25" printer)
printer_width = 384
wpercent = (printer_width / float(img.width))
hsize = int((float(img.height) * float(wpercent)))
img = img.resize((printer_width, hsize))

# Use the built-in graphics method
printer.print_graphic(img)

# Advance paper
printer.feed(3)
