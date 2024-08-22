import os
import cairosvg
from PIL import Image, UnidentifiedImageError, PngImagePlugin
from tqdm import tqdm
import json

# Constants
GENERATED_DIR = 'generated'
GENERATED_PNG_DIR = 'pngs'
SPRITE_SHEET_EXT = '.png'
METADATA_EXT = '.json'


def optimize_png(img, png_path: str, do_resize: bool = False):
    """
    Optimize PNG file by removing unnecessary metadata and ensuring it's saved in the correct format.
    :param img: PIL Image object
    :param png_path: str
    :param do_resize: bool
    """
    try:
        # Ensure image is in RGBA format
        img = img.convert('RGBA')
        # Resize images to smaller icon size
        # TODO: implement resize feature
        if do_resize:
            img.thumbnail((32, 32), Image.Resampling.LANCZOS)
        # Optimize PNG by removing unnecessary metadata
        img.save(png_path, format="PNG", optimize=True, pnginfo=PngImagePlugin.PngInfo())
    except Exception as e:
        print(f"Error optimizing PNG {png_path}: {e}")


def create_sprite_sheet(
        svg_directory: str,
        output_directory_name: str,
        output_sprite_sheet: str,
        metadata_file: str,
        do_resize: bool = False):
    if not os.path.exists(svg_directory):
        print(f"Directory {svg_directory} does not exist.")
        return

    # Get list of SVG files
    svg_files = [f for f in os.listdir(svg_directory) if f.endswith('.svg')]
    num_files = len(svg_files)
    if num_files == 0:
        print("No SVG files found.")
        return

    generated_path = create_directories(output_directory_name)

    # Load SVG files and convert to PNG
    sprites = []
    metadata = {}
    for svg_file in tqdm(svg_files, desc='Converting SVG to PNG', unit='files'):
        filename = os.path.splitext(svg_file)[0]
        svg_path = os.path.join(svg_directory, svg_file)
        png_path = os.path.join(f"{generated_path}/{GENERATED_PNG_DIR}", f"{os.path.splitext(svg_file)[0]}.png")
        try:
            # Convert SVG to PNG
            cairosvg.svg2png(url=svg_path, write_to=png_path)

            # Verify PNG file integrity
            try:
                with Image.open(png_path) as img:
                    optimize_png(img, png_path, do_resize=do_resize)
                    sprites.append(png_path)
                    metadata.update({
                        filename: {
                            'width': img.width,
                            'height': img.height,
                            'mask': 'true'
                        }
                    })
            except (UnidentifiedImageError, IOError) as e:
                print(f"Error verifying PNG {png_path}: {e}")
                continue
        except Exception as e:
            print(f"Error converting {svg_file} to PNG: {e}")
            continue

    if not sprites:
        print("No valid PNG files generated.")
        return

    # Calculate optimized sprite sheet size
    sprite_width = max(metadata[sprite]['width'] for sprite in metadata)
    sprite_height = max(metadata[sprite]['height'] for sprite in metadata)
    num_sprites = len(sprites)
    sprites_per_row = int(num_sprites ** 0.5)
    sprites_per_col = (num_sprites + sprites_per_row - 1) // sprites_per_row
    sprite_sheet_width = sprites_per_row * sprite_width
    sprite_sheet_height = sprites_per_col * sprite_height
    sprite_sheet = Image.new('RGBA', (sprite_sheet_width, sprite_sheet_height), (0, 0, 0, 0))

    # Add sprites to the sprite sheet
    for i, sprite_path in enumerate(tqdm(sprites, desc='Creating sprite sheet', unit='sprites')):
        sprite_name = os.path.splitext(os.path.basename(sprite_path))[0]
        sprite = Image.open(sprite_path)
        x = (i % sprites_per_row) * sprite_width
        y = (i // sprites_per_row) * sprite_height
        sprite_sheet.paste(sprite, (x, y))

        # Update metadata with sprite position
        metadata[sprite_name]['x'] = x
        metadata[sprite_name]['y'] = y

    if sprite_sheet is None:
        print("No sprite sheet generated.")
        return

    try:
        # Save the resulting sprite sheet
        print("Saving sprite sheet...")
        sprite_sheet_path = os.path.join(generated_path, output_sprite_sheet)
        sprite_sheet.save(
            f"{sprite_sheet_path}{SPRITE_SHEET_EXT}",
            format="PNG",
            optimize=True,
            pnginfo=PngImagePlugin.PngInfo())
        print(f"Sprite sheet saved to {sprite_sheet_path}")

        # Save the metadata JSON
        print("Saving metadata...")
        metadata_path = f"{os.path.join(generated_path, metadata_file)}{METADATA_EXT}"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        print(f"Metadata saved to {metadata_path}")
    except Exception as e:
        print(f"Error saving sprite sheet and metadata: {e}")
        return


def create_directories(output_directory_name: str):
    if not os.path.exists(GENERATED_DIR):
        os.makedirs(GENERATED_DIR)

    generated_path = os.path.join(GENERATED_DIR, output_directory_name)
    if not os.path.exists(generated_path):
        os.makedirs(generated_path)
    else:
        counter = 1
        while os.path.exists(f"{generated_path}_{counter}"):
            counter += 1
        generated_path = f"{generated_path}_{counter}"
        os.makedirs(generated_path)

    if not os.path.exists(f"{generated_path}/{GENERATED_PNG_DIR}"):
        os.makedirs(f"{generated_path}/{GENERATED_PNG_DIR}")

    return generated_path


def main():
    # get input from user
    svg_directory = input("Enter the directory containing SVG files (ABS PATH): ")
    output_directory_name = input("Enter the directory name for the generated files: ")
    output_sprite_sheet = input("Enter the filename for the generated sprite sheet (Only name): ")
    metadata_file = input("Enter the filename for the metadata JSON file (Only name): ")

    create_sprite_sheet(svg_directory, output_directory_name, output_sprite_sheet, metadata_file)


if __name__ == "__main__":
    main()
