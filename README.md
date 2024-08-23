# SVG Sprite Sheet Generator
This project automates the process of creating a sprite sheet from a directory of SVG files. It offers features like:

- **Converting SVG to PNG:** Efficiently converts SVG files to optimized PNG format.
- **Image Optimization:** Optimizes PNG files by removing unnecessary metadata and ensuring correct formatting. (Optional Resize Functionality)
- **Sprite Sheet Creation:** Generates a single image file containing all the individual PNGs (sprites) arranged efficiently.
- **Metadata Generation:** Creates a JSON file containing information about each sprite within the sheet, including its filename, dimensions, and position within the sprite sheet.


## Installation
This project requires Python 3 and the following libraries:

- `cairosvg`
- `Pillow (PIL Fork)`
- `tqdm`

You can install them using `pip`:

```bash
pip install -r requirements.txt
```


## Usage
1. **Clone the repository:**
```bash
git clone https://github.com/your-username/svg-sprite-generator.git
```

2. **Navigate to the project directory:**
```bash
cd svg-sprite-generator
```

3. **Run the script:**

The script prompts you for user input. Provide the following details:

- Enter the directory containing SVG files (ABS PATH): Specify the absolute path to the directory containing your SVG files.
- Enter the directory name for the generated files: Define the name for the directory that will hold the generated sprite sheet and metadata file.
- Enter the filename for the generated sprite sheet (Only name): Enter the desired filename for the sprite sheet (without extension, .png will be added automatically).
- Enter the filename for the metadata JSON file (Only name): Choose a filename for the JSON file containing sprite metadata (without extension, .json will be added).

**Example:**
```
Enter the directory containing SVG files (ABS PATH): /path/to/your/svg/directory
Enter the directory name for the generated files: my_sprite_sheet
Enter the filename for the generated sprite sheet (Only name): sprite_sheet
Enter the filename for the metadata JSON file (Only name): metadata
```

The script will then convert your SVG files to PNGs, optimize them (optional resize), create the sprite sheet, and generate the corresponding metadata file.

**Output:**

The script will create a new directory within the `generated` folder with the specified name. This directory will contain:

- A subfolder named `pngs` holding all the optimized PNG files converted from the SVGs.
- The generated sprite sheet file (`sprite_sheet.png` in the example).
- The JSON metadata file (`metadata.json` in the example) containing information about each sprite within the sheet.


### Additional Notes
- This script uses absolute paths for input and output. Ensure you provide the correct absolute path to your SVG directory.
- The script provides basic error handling and informative messages.
- Feel free to modify the script to customize aspects like the sprite sheet naming convention or metadata structure.