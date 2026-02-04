import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image
import time

# --------------------
# Serial + printer
# --------------------
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3)
printer = ThermalPrinter(uart)

def print_png(printer, filename, max_width=384):
    # Load and convert image to 1-bit
    img = Image.open(filename).convert("1")

    # Scale to printer width
    if img.width > max_width:
        scale = max_width / img.width
        img = img.resize((max_width, int(img.height * scale)))

    # Width must be multiple of 8
    if img.width % 8 != 0:
        new_width = img.width + (8 - img.width % 8)
        padded = Image.new("1", (new_width, img.height), 1)
        padded.paste(img, (0, 0))
        img = padded

    width, height = img.size

    # Build bitmap bytes (column-major, 8 pixels per byte)
    raw = bytearray()

    for x in range(width):
        for y in range(0, height, 8):
            byte = 0
            for bit in range(8):
                if y + bit < height:
                    if img.getpixel((x, y + bit)) == 0:  # black
                        byte |= 1 << bit
            raw.append(byte)

    # 🔑 CRITICAL FIX: convert to bytes
    bitmap_bytes = bytes(raw)

    time.sleep(0.1)
    printer._print_bitmap(width, height, bitmap_bytes)
    printer.feed(4)

# --------------------
# Print the image
# --------------------
print_png(printer, "kp_values.png")
