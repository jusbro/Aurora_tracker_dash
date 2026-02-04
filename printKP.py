import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image
import time

# --------------------------
# Setup printer
# --------------------------
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
printer = ThermalPrinter(uart)

# --------------------------
# Helper function to print PNG
# --------------------------
def print_png(printer, filename, printer_width=384, feed_lines=3):
    """
    Prints a PNG file on the thermal printer.
    Converts to 1-bit B/W, resizes to printer width,
    and sends raw bitmap data to _print_bitmap().
    """
    # Load image and convert to 1-bit black & white
    img = Image.open(filename).convert("1")

    # Resize to printer width
    wpercent = printer_width / float(img.width)
    hsize = int(float(img.height) * wpercent)
    img = img.resize((printer_width, hsize))

    # Center on a white canvas
    canvas = Image.new("1", (printer_width, img.height), 1)
    canvas.paste(img, ((printer_width - img.width) // 2, 0))
    img = canvas

    # Convert to raw bitmap bytes
    data = bytearray()
    for x in range(img.width):
        for y in range(0, img.height, 8):
            byte = 0
            for bit in range(8):
                if y + bit < img.height:
                    pixel = img.getpixel((x, y + bit))
                    if pixel == 0:  # black pixel
                        byte |= 1 << bit
            data.append(byte)

    # Send raw bitmap to printer
    printer._print_bitmap(img.width, img.height, data)
    printer.feed(feed_lines)
    time.sleep(0.2)  # small delay to ensure printing completes

# --------------------------
# Example usage
# --------------------------
printer.println("Printing Logo Example")
printer.feed(1)
print_png(printer, "logo.png")
printer.println("Done!")
printer.feed(3)
