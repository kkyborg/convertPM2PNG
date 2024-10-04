import argparse
from PIL import Image
import os


# Function to read binary file
def read_binary_file(filepath, filesize):
    with open(filepath, 'rb') as file:
        return list(file.read(filesize))

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
def create_image(pixel_data, palette_data, transparent_index=None, width=16, height=16):
    # Create a new image with mode 'P' (palette-based) and size 16x16
    img = Image.new('P', (width, height))
    
    # Put the pixel data into the image
    img.putdata(pixel_data)
    
    # Apply the palette to the image
    img.putpalette(palette_data)
    
    # Set transparency if specified
    if transparent_index is not None:
        img.info['transparency'] = transparent_index
    
    return img

def parse_transparent_colors(file_content):
    """Parse the list of filenames and their transparent color indices."""
    color_map = {}
    lines = file_content.strip().split('\n')
    for line in lines:
        parts = line.split('//')
        if len(parts) > 1:
            index_part = parts[0].strip()
            filename_part = parts[1].strip()
            try:
                transparent_color_index = int(index_part.split(',')[0].strip())
                filename = filename_part.split('.')[0].strip()
                color_map[filename] = transparent_color_index
            except ValueError:
                continue
    return color_map
    
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create a PNG image from binary pixel data and indexed color palette.')
    parser.add_argument('pixel_file', type=str, help='Path to the binary pixel data file.')
    parser.add_argument('palette_file', type=str, help='Path to the indexed color palette file.')
    parser.add_argument('--output_image', type=str, help='Path to save the output PNG image. If not set, defaults to the input pixel file name with .png extension.')
    parser.add_argument('--transparent', type=int, help='Indexed color (byte value) to be set as transparent in the output image.')
    # Add an optional argument for transparent colors list
    parser.add_argument('--color-list', type=str, help='Path to the transparent colors list file', default=None)
    parser.add_argument('--width', type=int, help='Width of the image in pixels', default=16)
    parser.add_argument('--height', type=int, help='Height of the image in pixels', default=16)

    # Parse arguments
    args = parser.parse_args()

    # Read the transparent colors list if provided
    color_map = {}
    if args.color_list:
        try:
            with open(args.color_list, 'r') as file:
                file_content = file.read()
                color_map = parse_transparent_colors(file_content)
        except FileNotFoundError:
            print(f"Error: The file '{args.color_list}' was not found.")
            return

    # Extract the filename without extension
    input_file_base = args.pixel_file.split('.')[0]

    # Set output file name to be the same as input pixel file if not provided
    if args.output_image:
        output_image_path = args.output_image
    else:
        base_name = os.path.splitext(args.pixel_file)[0]
        output_image_path = f"{base_name}.png"
        
    # Check if the input filename is recognized and get transparent color index
    transparent_color_index = None
    if args.color_list and input_file_base in color_map:
        transparent_color_index = color_map[input_file_base]
        print(f"Recognized input file. Using transparent color index: {transparent_color_index}")
    

    # Reading data from files
    pixel_data = read_binary_file(args.pixel_file, args.width * args.height)
    palette_data = read_palette_file(args.palette_file)

    # Create and save the image with optional transparency
    # Continue processing based on the presence of transparent_color_index
    if transparent_color_index is not None and transparent_color_index != 255:
        # Handle transparent color index here
        image = create_image(pixel_data, palette_data, transparent_index=transparent_color_index, width=args.width, height=args.height)
    else:
        image = create_image(pixel_data, palette_data, transparent_index=args.transparent, width=args.width, height=args.height)
    image.save(output_image_path)

    print(f"Image saved as {output_image_path}")

if __name__ == '__main__':
    main()
