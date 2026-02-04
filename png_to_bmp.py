from PIL import Image

INPUT_FILE = "kp_values.png"
OUTPUT_FILE = "kp_values.bmp"
PRINTER_WIDTH = 384  # pixels

def convert_png_to_bmp():
    # Open image
    img = Image.open(INPUT_FILE)

    # Convert to grayscale first (better dithering)
    img = img.convert("L")

    # Resize to printer width, keep aspect ratio
    scale = PRINTER_WIDTH / img.width
    new_height = int(img.height * scale)
    img = img.resize((PRINTER_WIDTH, new_height), Image.LANCZOS)

    # Convert to 1-bit black & white with dithering
    img = img.convert("1")

    # Save as BMP (1-bit)
    img.save(OUTPUT_FILE, format="BMP")

    print(f"Converted {INPUT_FILE} → {OUTPUT_FILE}")
    print(f"Final size: {img.width} x {img.height} px (1-bit)")

if __name__ == "__main__":
    convert_png_to_bmp()
