import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image
import time

# --------------------------
# Setup printer
# --------------------------
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3)
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
    img = Image.open(filename).convert("1")

    # Resize to printer width
    scale = printer_width / img.width
    new_height = int(img.height * scale)
    img = img.resize((printer_width, new_height))

    # Convert to raw bitmap bytes
    data = bytearray()
    for x in range(img.width):
        for y in range(0, img.height, 8):
            byte = 0
            for bit in range(8):
                if y + bit < img.height:
                    if img.getpixel((x, y + bit)) == 0:  # black
                        byte |= 1 << bit
            data.append(byte)

    # Print bitmap
    printer._print_bitmap(img.width, img.height, data)
    printer.feed(feed_lines)
    time.sleep(0.25)

# --------------------------
# Example usage
# --------------------------
printer.println(b"Printing Logo Example")  # already bytes
printer.feed(1)

print_png(printer, "logo.png")

printer.println("Done!".encode("utf-8"))
printer.feed(3)
