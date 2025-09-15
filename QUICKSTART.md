# 🚀 Quick Start Guide

## Installation

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Or manually:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Basic Usage

### Use the convenience script:
```bash
# Game Boy Camera style (default)
./run_converter.sh photo.jpg gameboy_output.png

# Dot matrix printer style
./run_converter.sh --style dotmatrix photo.jpg matrix_output.png

# Retro computer colors
./run_converter.sh --style retro --palette c64 photo.jpg retro_output.png
```

### Or activate the environment manually:
```bash
source venv/bin/activate
python retro_converter.py photo.jpg output.png
```

## Examples

```bash
# Game Boy Camera nostalgia
./run_converter.sh portrait.jpg gameboy_portrait.png

# High contrast dot matrix
./run_converter.sh --style dotmatrix --width 400 --contrast 2.5 landscape.jpg matrix.png

# Commodore 64 colors with fast dithering
./run_converter.sh --style retro --palette c64 --dither bayer colorful.jpg c64_style.png

# ZX Spectrum palette
./run_converter.sh --style retro --palette spectrum --width 256 photo.jpg spectrum_photo.png

# Apple II colors
./run_converter.sh --style retro --palette apple2 photo.jpg apple2_photo.png
```

## Features

✅ **Game Boy Camera**: 4-shade green, 128×112 resolution  
✅ **Dot Matrix**: Black & white with dithering  
✅ **Color Palettes**: CGA, Apple II, C64, ZX Spectrum  
✅ **Dithering**: Floyd-Steinberg, Bayer, Ordered  
✅ **Customizable**: Resolution, contrast, preview  

## Get Help

```bash
./run_converter.sh --help
./run_converter.sh info
```
