#!/usr/bin/env python3
"""
Retro Image Converter CLI Tool

Convert photos to dot matrix, Game Boy camera, or retro computer styles
with various dithering algorithms and color palettes.
"""

import click
import sys
import os
from PIL import Image
from image_processor import RetroImageProcessor


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--style', '-s', 
              type=click.Choice(['gameboy', 'dotmatrix', 'retro']), 
              default='gameboy',
              help='Output style: gameboy (Game Boy Camera), dotmatrix (black/white), retro (color)')
@click.option('--dither', '-d',
              type=click.Choice(['floyd_steinberg', 'bayer', 'ordered']),
              default='floyd_steinberg',
              help='Dithering algorithm to use')
@click.option('--width', '-w',
              type=int,
              default=None,
              help='Output width in pixels (auto-calculated if not specified)')
@click.option('--height', '-h',
              type=int,
              default=None,
              help='Output height in pixels (auto-calculated if not specified)')
@click.option('--contrast', '-c',
              type=float,
              default=None,
              help='Contrast enhancement factor (default varies by style)')
@click.option('--palette', '-p',
              type=click.Choice(['cga', 'apple2', 'c64', 'spectrum']),
              default='cga',
              help='Color palette for retro style')
@click.option('--preview', 
              is_flag=True,
              help='Show image preview after processing (requires display)')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Verbose output')
def convert_image(input_file, output_file, style, dither, width, height, contrast, palette, preview, verbose):
    """
    Convert INPUT_FILE to retro style and save as OUTPUT_FILE.
    
    Examples:
    
    \b
    # Convert to Game Boy Camera style
    python retro_converter.py photo.jpg gameboy_photo.png
    
    \b
    # Convert to dot matrix printer style with custom width
    python retro_converter.py photo.jpg --style dotmatrix --width 300 matrix_photo.png
    
    \b
    # Convert to retro color with Bayer dithering
    python retro_converter.py photo.jpg --style retro --dither bayer --palette cga retro_photo.png
    """
    
    if verbose:
        click.echo(f"Loading image: {input_file}")
    
    try:
        # Load the image
        with Image.open(input_file) as img:
            processor = RetroImageProcessor()
            
            # Set default parameters based on style
            if style == 'gameboy':
                if width is None:
                    width = 128
                if height is None:
                    height = 112
                if contrast is None:
                    contrast = 1.5
                    
                if verbose:
                    click.echo(f"Converting to Game Boy Camera style...")
                    click.echo(f"Resolution: {width}x{height}, Contrast: {contrast}, Dither: {dither}")
                
                result = processor.convert_to_gameboy_camera(img, dither, contrast)
                
            elif style == 'dotmatrix':
                if width is None:
                    width = 200
                if contrast is None:
                    contrast = 2.0
                    
                if verbose:
                    click.echo(f"Converting to dot matrix printer style...")
                    click.echo(f"Width: {width}, Contrast: {contrast}, Dither: {dither}")
                
                result = processor.convert_to_dot_matrix(img, width, dither, contrast)
                
            elif style == 'retro':
                if width is None:
                    width = 320
                if contrast is None:
                    contrast = 1.2
                    
                if verbose:
                    click.echo(f"Converting to retro computer style...")
                    click.echo(f"Width: {width}, Palette: {palette}, Contrast: {contrast}, Dither: {dither}")
                
                result = processor.convert_to_retro_color(img, width, palette, dither, contrast)
            
            # Save the result
            if verbose:
                click.echo(f"Saving result to: {output_file}")
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            result.save(output_file)
            
            if verbose:
                click.echo(f"✓ Conversion complete! Saved as {output_file}")
                click.echo(f"Original size: {img.width}x{img.height}")
                click.echo(f"Output size: {result.width}x{result.height}")
            
            # Show preview if requested
            if preview:
                try:
                    result.show()
                except Exception as e:
                    click.echo(f"Warning: Could not show preview - {e}", err=True)
                    
    except FileNotFoundError:
        click.echo(f"Error: Input file '{input_file}' not found.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error processing image: {e}", err=True)
        sys.exit(1)


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Retro Image Converter - Transform photos into retro/vintage styles."""
    pass


@cli.command()
def info():
    """Show information about available styles and palettes."""
    click.echo("🎮 Retro Image Converter")
    click.echo("=" * 25)
    click.echo()
    click.echo("Available Styles:")
    click.echo("  gameboy    - Game Boy Camera style (4-shade green, 128x112)")
    click.echo("  dotmatrix  - Dot matrix printer style (black & white)")
    click.echo("  retro      - Retro computer style (limited color palette)")
    click.echo()
    click.echo("Dithering Algorithms:")
    click.echo("  floyd_steinberg - High quality, good for photos")
    click.echo("  bayer          - Fast, good for graphics")
    click.echo("  ordered        - Alternative ordered dithering")
    click.echo()
    click.echo("Color Palettes (for retro style):")
    click.echo("  cga            - IBM CGA 16-color palette")
    click.echo("  apple2         - Apple II 16-color palette")
    click.echo("  c64            - Commodore 64 16-color palette")
    click.echo("  spectrum       - ZX Spectrum 16-color palette")
    click.echo()
    click.echo("Examples:")
    click.echo("  retro_converter.py photo.jpg gameboy.png --style gameboy")
    click.echo("  retro_converter.py photo.jpg matrix.png --style dotmatrix --width 400")
    click.echo("  retro_converter.py photo.jpg retro.png --style retro --palette cga")


# Add the convert command to the CLI group
cli.add_command(convert_image, name='convert')


if __name__ == '__main__':
    # If run directly, use the convert command as default
    if len(sys.argv) == 1:
        cli(['--help'])
    else:
        # Check if first argument is a filename (not a subcommand)
        if sys.argv[1] not in ['convert', 'info', '--help', '--version']:
            # Insert 'convert' as the subcommand
            sys.argv.insert(1, 'convert')
        cli()
