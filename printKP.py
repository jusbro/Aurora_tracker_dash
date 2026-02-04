import serial
from adafruit_thermal_printer.thermal_printer import ThermalPrinter
from PIL import Image
import time

# -----------------------
# Printer setup
# -----------------------
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3)
printer = ThermalPrinter(uart)

def print_png_file(printer, filename, printer_width=384, feed_lines=4):
    """
    Convert a PNG to 1-bit and print it to the thermal printer.
    """
    # Load the PNG and convert to 1-bit
    img = Image.open(filename).convert("1")
    
    # Scale to printer width while maintaining aspect ratio
    if img.width > printer_width:
        scale = printer_width / img.width
        new_height = int(img.height * scale)
        img = img.resize((printer_width, new_height))

    # Ensure width is a multiple of 8 (thermal printers work per 8 horizontal pixels)
    if img.width % 8 != 0:
        new_width = img.width + (8 - (img.width % 8))
        canvas = Image.new("1", (new_width, img.height), 1)  # white fill
        canvas.paste(img, ((new_width - img.width) // 2, 0))
        img = canvas

    width, height = img.size

    # Build raw bitmap data by column, 8 pixels per byte
    bitmap_data = bytearray()
    for x in range(0, width):
        for y in range(0, height, 8):
            byte = 0
            for bit in range(8):
                if y + bit < height:
                    pixel = img.getpixel((x, y + bit))
                    # In PIL mode "1", white = 255, black = 0
                    if pixel == 0:
                        byte |= 1 << bit
            bitmap_data.append(byte)

    # Give the printer a moment
    time.sleep(0.1)

    # Send bitmap to printer
    printer._print_bitmap(width, height, bitmap_data)

    # Feed paper so the image clears the head
    printer.feed(feed_lines)
    time.sleep(0.2)

# -----------------------
# Run print
# -----------------------
print_png_file(printer, "kp_values.png")
