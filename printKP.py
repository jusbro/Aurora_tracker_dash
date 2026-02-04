import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image

# --------------------------
# Setup your printer
# --------------------------
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
printer = ThermalPrinter(uart)  # latest CircuitPython library, no extra args

# --------------------------
# Helper function to print PNG
# --------------------------
def print_png(printer, filename, printer_width=384, feed_lines=3, center=True):
    """
    Prints a PNG image to the thermal printer.
    
    Args:
        printer: ThermalPrinter object
        filename: path to PNG file
        printer_width: printer width in pixels (384 for 2.25" printer)
        feed_lines: lines to feed after printing
        center: whether to center the image
    """
    # Load image
    img = Image.open(filename)
    
    # Convert to 1-bit B/W using dithering
    img = img.convert("1")  # Floyd–Steinberg dithering
    
    # Resize image to printer width, maintain aspect ratio
    wpercent = printer_width / float(img.width)
    hsize = int(float(img.height) * wpercent)
    img = img.resize((printer_width, hsize))
    
    # Center image on white canvas if requested
    if center:
        canvas = Image.new("1", (printer_width, img.height), 1)  # white background
        canvas.paste(img, ((printer_width - img.width)//2, 0))
        img = canvas
    
    # Print image
    printer.print_graphic(img)
    
    # Feed a few lines
    printer.feed(feed_lines)

# --------------------------
# Example usage
# --------------------------
print_png(printer, "logo.png")
