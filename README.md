# 🎮 Retro Image Converter

A CLI tool that converts modern photos into retro/vintage styles reminiscent of Game Boy Camera, dot matrix printers, and classic computer graphics.

## Features

- **Game Boy Camera Style**: 4-shade green palette at 128x112 resolution
- **Dot Matrix Printer**: Classic black and white with dithering
- **Retro Computer Palettes**: CGA, Apple II, Commodore 64, and ZX Spectrum color schemes
- **Multiple Dithering Algorithms**: Floyd-Steinberg, Bayer matrix, and ordered dithering
- **Customizable Output**: Adjust resolution, contrast, and other parameters

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Make it executable (optional)

```bash
chmod +x retro_converter.py
```

## Usage

### Basic Examples

```bash
# Convert to Game Boy Camera style (default)
python retro_converter.py photo.jpg gameboy_output.png

# Convert to dot matrix printer style
python retro_converter.py photo.jpg --style dotmatrix output.png

# Convert to retro color with specific palette
python retro_converter.py photo.jpg --style retro --palette c64 output.png
```

### Advanced Options

```bash
# Custom resolution and dithering
python retro_converter.py photo.jpg --style dotmatrix --width 400 --dither bayer output.png

# Adjust contrast and show preview
python retro_converter.py photo.jpg --contrast 1.8 --preview --verbose output.png

# Multiple palette options for retro style
python retro_converter.py photo.jpg --style retro --palette apple2 --width 640 output.png
```

### CLI Options

- `--style`, `-s`: Output style (`gameboy`, `dotmatrix`, `retro`)
- `--dither`, `-d`: Dithering algorithm (`floyd_steinberg`, `bayer`, `ordered`)
- `--width`, `-w`: Output width in pixels
- `--height`, `-h`: Output height in pixels
- `--contrast`, `-c`: Contrast enhancement factor
- `--palette`, `-p`: Color palette for retro style (`cga`, `apple2`, `c64`, `spectrum`)
- `--preview`: Show image preview after processing
- `--verbose`, `-v`: Verbose output

### Styles

#### Game Boy Camera (`gameboy`)

- Resolution: 128x112 pixels
- Colors: 4-shade green palette
- Best for: Nostalgic, vintage look

#### Dot Matrix (`dotmatrix`)

- Colors: Black and white only
- Best for: High contrast images, text, simple graphics

#### Retro Computer (`retro`)

- Multiple vintage computer palettes
- **CGA**: IBM PC 16-color palette
- **Apple II**: Apple II 16-color palette
- **C64**: Commodore 64 16-color palette
- **Spectrum**: ZX Spectrum 16-color palette

### Dithering Algorithms

- **Floyd-Steinberg**: High quality, good for photographs
- **Bayer**: Fast processing, good for graphics and patterns
- **Ordered**: Alternative ordered dithering pattern

## Examples with Different Styles

```bash
# Game Boy Camera nostalgia
python retro_converter.py portrait.jpg --style gameboy gameboy_portrait.png

# Classic dot matrix printer
python retro_converter.py landscape.jpg --style dotmatrix --width 300 --contrast 2.5 matrix_landscape.png

# 1980s computer graphics
python retro_converter.py colorful_image.jpg --style retro --palette cga --dither bayer retro_image.png

# Commodore 64 style
python retro_converter.py photo.jpg --style retro --palette c64 --width 320 c64_photo.png
```

## Getting Help

```bash
# Show help
python retro_converter.py --help

# Show detailed information about styles and palettes
python retro_converter.py info
```

## Tips for Best Results

1. **High contrast images** work better with dithering
2. **Portraits** often look great in Game Boy Camera style
3. **Simple graphics** work well with dot matrix style
4. **Colorful images** benefit from retro computer palettes
5. Use **Floyd-Steinberg dithering** for photographs
6. Use **Bayer dithering** for faster processing of graphics
7. Adjust **contrast** if the output appears too light or dark

## Technical Details

The tool implements several classic image processing techniques:

- **Floyd-Steinberg error diffusion dithering**
- **Bayer matrix ordered dithering**
- **Color quantization** to limited palettes
- **Nearest color matching** in RGB space
- **Bicubic resampling** for resolution changes

## Supported File Formats

- **Input**: JPEG, PNG, BMP, TIFF, and other PIL-supported formats
- **Output**: PNG, JPEG, BMP, TIFF (PNG recommended for best quality)

## License

This project is open source and available under the MIT License.
