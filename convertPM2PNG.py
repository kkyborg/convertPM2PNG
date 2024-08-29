import argparse
from PIL import Image
import os

# Constants
IMAGE_WIDTH = 16
IMAGE_HEIGHT = 16

# Function to read binary file
def read_binary_file(filepath):
    with open(filepath, 'rb') as file:
        return list(file.read())

# Function to read palette file
def read_palette_file(filepath):
    palette = []
    with open(filepath, 'rb') as file:
        while True:
            color = file.read(3)  # Read 3 bytes at a time (RGB)
            if not color:
                break
            palette.extend(color)
    return palette

# Function to create the image
def create_image(pixel_data, palette_data, transparent_index=None):
    # Create a new image with mode 'P' (palette-based) and size 16x16
    img = Image.new('P', (IMAGE_WIDTH, IMAGE_HEIGHT))
    
    # Put the pixel data into the image
    img.putdata(pixel_data)
    
    # Apply the palette to the image
    img.putpalette(palette_data)
    
    # Set transparency if specified
    if transparent_index is not None:
        img.info['transparency'] = transparent_index
    
    return img

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create a PNG image from binary pixel data and indexed color palette.')
    parser.add_argument('pixel_file', type=str, help='Path to the binary pixel data file.')
    parser.add_argument('palette_file', type=str, help='Path to the indexed color palette file.')
    parser.add_argument('--output_image', type=str, help='Path to save the output PNG image. If not set, defaults to the input pixel file name with .png extension.')
    parser.add_argument('--transparent', type=int, help='Indexed color (byte value) to be set as transparent in the output image.')

    # Parse arguments
    args = parser.parse_args()

    # Set output file name to be the same as input pixel file if not provided
    if args.output_image:
        output_image_path = args.output_image
    else:
        base_name = os.path.splitext(args.pixel_file)[0]
        output_image_path = f"{base_name}.png"

    # Reading data from files
    pixel_data = read_binary_file(args.pixel_file)
    palette_data = read_palette_file(args.palette_file)

    # Create and save the image with optional transparency
    image = create_image(pixel_data, palette_data, transparent_index=args.transparent)
    image.save(output_image_path)

    print(f"Image saved as {output_image_path}")

if __name__ == '__main__':
    main()
