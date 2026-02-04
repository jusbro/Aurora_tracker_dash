import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image

# Serial setup
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

# Initialize printer
printer = ThermalPrinter(uart, cooling_factor=2.69)

# Load a PNG image
img = Image.open("logo.png")
img = img.convert("1")  # black & white
printer_width = 384
wpercent = (printer_width / float(img.width))
hsize = int((float(img.height) * float(wpercent)))
img = img.resize((printer_width, hsize))

# Print graphic
printer.print_graphic(img)
printer.feed(3)
