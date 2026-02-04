import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image

# Serial setup
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

# Initialize printer
printer = ThermalPrinter(uart)

# ------------------------
# Convert a PNG to 1-bit BMP
# ------------------------
def png_to_bmp_1bit(png_path, bmp_path, printer_width=384):
    img = Image.open(png_path)
    # Convert to 1-bit B/W
    img = img.convert("1")
    # Resize to printer width
    wpercent = printer_width / float(img.width)
    hsize = int(float(img.height) * wpercent)
    img = img.resize((printer_width, hsize))
    # Save as BMP
    img.save(bmp_path, format="BMP")

# Convert your PNG
png_to_bmp_1bit("logo.png", "logo.bmp")

# Print BMP
printer.print_bmp("logo.bmp")
printer.feed(3)
