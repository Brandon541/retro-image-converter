"""
Core image processing functions for retro-style image conversion.
Includes dithering algorithms, color quantization, and palette matching.
"""

import numpy as np
from PIL import Image, ImageEnhance
from typing import List, Tuple, Optional
import math


class RetroImageProcessor:
    """Main class for processing images into retro/Game Boy camera style."""
    
    # Game Boy Camera 4-shade grayscale palette
    GAMEBOY_PALETTE = [
        (15, 56, 15),    # Dark green (black)
        (48, 98, 48),    # Medium-dark green
        (139, 172, 15),  # Medium-light green
        (155, 188, 15)   # Light green (white)
    ]
    
    # Classic dot matrix printer palette (black and white)
    DOT_MATRIX_PALETTE = [
        (0, 0, 0),       # Black
        (255, 255, 255)  # White
    ]
    
    # Retro computer palettes
    CGA_PALETTE = [
        (0, 0, 0),       # Black
        (0, 0, 170),     # Blue
        (0, 170, 0),     # Green
        (0, 170, 170),   # Cyan
        (170, 0, 0),     # Red
        (170, 0, 170),   # Magenta
        (170, 85, 0),    # Brown
        (170, 170, 170), # Light gray
        (85, 85, 85),    # Dark gray
        (85, 85, 255),   # Light blue
        (85, 255, 85),   # Light green
        (85, 255, 255),  # Light cyan
        (255, 85, 85),   # Light red
        (255, 85, 255),  # Light magenta
        (255, 255, 85),  # Yellow
        (255, 255, 255)  # White
    ]
    
    # Apple II palette
    APPLE_II_PALETTE = [
        (0, 0, 0),       # Black
        (114, 38, 64),   # Dark red
        (64, 51, 127),   # Dark blue
        (228, 52, 254),  # Purple
        (14, 89, 64),    # Dark green
        (128, 128, 128), # Gray
        (27, 154, 254),  # Medium blue
        (191, 179, 255), # Light blue
        (64, 76, 0),     # Brown
        (228, 101, 1),   # Orange
        (128, 128, 128), # Gray 2
        (241, 166, 191), # Pink
        (27, 203, 1),    # Green
        (191, 204, 128), # Yellow
        (141, 217, 191), # Aqua
        (255, 255, 255)  # White
    ]
    
    # Commodore 64 palette
    C64_PALETTE = [
        (0, 0, 0),       # Black
        (255, 255, 255), # White
        (136, 0, 0),     # Red
        (170, 255, 238), # Cyan
        (204, 68, 204),  # Purple
        (0, 204, 85),    # Green
        (0, 0, 170),     # Blue
        (238, 238, 119), # Yellow
        (221, 136, 85),  # Orange
        (102, 68, 0),    # Brown
        (255, 119, 119), # Light red
        (51, 51, 51),    # Dark gray
        (119, 119, 119), # Medium gray
        (170, 255, 102), # Light green
        (0, 136, 255),   # Light blue
        (187, 187, 187)  # Light gray
    ]
    
    # ZX Spectrum palette
    ZX_SPECTRUM_PALETTE = [
        (0, 0, 0),       # Black
        (0, 0, 192),     # Blue
        (192, 0, 0),     # Red
        (192, 0, 192),   # Magenta
        (0, 192, 0),     # Green
        (0, 192, 192),   # Cyan
        (192, 192, 0),   # Yellow
        (192, 192, 192), # White
        (0, 0, 0),       # Bright black
        (0, 0, 255),     # Bright blue
        (255, 0, 0),     # Bright red
        (255, 0, 255),   # Bright magenta
        (0, 255, 0),     # Bright green
        (0, 255, 255),   # Bright cyan
        (255, 255, 0),   # Bright yellow
        (255, 255, 255)  # Bright white
    ]
    
    def __init__(self):
        self.bayer_matrix_4x4 = np.array([
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]) / 16.0
    
    def resize_image(self, image: Image.Image, target_width: int, target_height: Optional[int] = None, maintain_aspect: bool = True) -> Image.Image:
        """Resize image to target dimensions."""
        if target_height is None:
            if maintain_aspect:
                aspect_ratio = image.height / image.width
                target_height = int(target_width * aspect_ratio)
            else:
                target_height = target_width
        
        return image.resize((target_width, target_height), Image.LANCZOS)
    
    def enhance_contrast(self, image: Image.Image, factor: float = 1.5) -> Image.Image:
        """Enhance image contrast for better dithering results."""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def floyd_steinberg_dither(self, image: Image.Image, palette: List[Tuple[int, int, int]]) -> Image.Image:
        """Apply Floyd-Steinberg dithering algorithm."""
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image, dtype=np.float64)
        height, width, channels = img_array.shape
        
        # Process each pixel
        for y in range(height):
            for x in range(width):
                old_pixel = img_array[y, x]
                new_pixel = self._find_closest_color(old_pixel, palette)
                img_array[y, x] = new_pixel
                
                error = old_pixel - new_pixel
                
                # Distribute error to neighboring pixels
                if x + 1 < width:
                    img_array[y, x + 1] += error * 7/16
                if y + 1 < height:
                    if x - 1 >= 0:
                        img_array[y + 1, x - 1] += error * 3/16
                    img_array[y + 1, x] += error * 5/16
                    if x + 1 < width:
                        img_array[y + 1, x + 1] += error * 1/16
        
        # Clip values and convert back to image
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array, 'RGB')
    
    def bayer_dither(self, image: Image.Image, palette: List[Tuple[int, int, int]]) -> Image.Image:
        """Apply Bayer matrix dithering."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_array = np.array(image, dtype=np.float64)
        height, width, channels = img_array.shape
        
        # Apply Bayer matrix threshold
        for y in range(height):
            for x in range(width):
                threshold = self.bayer_matrix_4x4[y % 4, x % 4] * 255
                pixel = img_array[y, x]
                
                # Add threshold noise
                pixel_with_noise = pixel + (threshold - 127.5)
                pixel_with_noise = np.clip(pixel_with_noise, 0, 255)
                
                # Find closest color
                new_pixel = self._find_closest_color(pixel_with_noise, palette)
                img_array[y, x] = new_pixel
        
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array, 'RGB')
    
    def ordered_dither(self, image: Image.Image, palette: List[Tuple[int, int, int]], matrix_size: int = 4) -> Image.Image:
        """Apply ordered dithering with custom matrix size."""
        # For simplicity, use Bayer dithering as base
        return self.bayer_dither(image, palette)
    
    def _find_closest_color(self, pixel: np.ndarray, palette: List[Tuple[int, int, int]]) -> np.ndarray:
        """Find the closest color in the palette to the given pixel."""
        min_distance = float('inf')
        closest_color = palette[0]
        
        for color in palette:
            distance = np.sum((pixel - np.array(color)) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_color = color
        
        return np.array(closest_color, dtype=np.float64)
    
    def convert_to_gameboy_camera(self, image: Image.Image, dither_method: str = 'floyd_steinberg', contrast_factor: float = 1.5) -> Image.Image:
        """Convert image to Game Boy Camera style (128x112, 4-shade grayscale)."""
        # Resize to Game Boy Camera resolution
        resized = self.resize_image(image, 128, 112, maintain_aspect=False)
        
        # Enhance contrast
        enhanced = self.enhance_contrast(resized, contrast_factor)
        
        # Apply dithering
        if dither_method == 'floyd_steinberg':
            return self.floyd_steinberg_dither(enhanced, self.GAMEBOY_PALETTE)
        elif dither_method == 'bayer':
            return self.bayer_dither(enhanced, self.GAMEBOY_PALETTE)
        else:
            return self.ordered_dither(enhanced, self.GAMEBOY_PALETTE)
    
    def convert_to_dot_matrix(self, image: Image.Image, width: int = 200, dither_method: str = 'floyd_steinberg', contrast_factor: float = 2.0) -> Image.Image:
        """Convert image to dot matrix printer style (black and white)."""
        # Resize image
        resized = self.resize_image(image, width)
        
        # Enhance contrast
        enhanced = self.enhance_contrast(resized, contrast_factor)
        
        # Apply dithering
        if dither_method == 'floyd_steinberg':
            return self.floyd_steinberg_dither(enhanced, self.DOT_MATRIX_PALETTE)
        elif dither_method == 'bayer':
            return self.bayer_dither(enhanced, self.DOT_MATRIX_PALETTE)
        else:
            return self.ordered_dither(enhanced, self.DOT_MATRIX_PALETTE)
    
    def convert_to_retro_color(self, image: Image.Image, width: int = 320, palette: str = 'cga', dither_method: str = 'floyd_steinberg', contrast_factor: float = 1.2) -> Image.Image:
        """Convert image to retro color palette style."""
        # Get the appropriate palette
        palette_map = {
            'cga': self.CGA_PALETTE,
            'apple2': self.APPLE_II_PALETTE,
            'c64': self.C64_PALETTE,
            'spectrum': self.ZX_SPECTRUM_PALETTE
        }
        
        color_palette = palette_map.get(palette.lower(), self.CGA_PALETTE)
        
        # Resize image
        resized = self.resize_image(image, width)
        
        # Enhance contrast slightly
        enhanced = self.enhance_contrast(resized, contrast_factor)
        
        # Apply dithering
        if dither_method == 'floyd_steinberg':
            return self.floyd_steinberg_dither(enhanced, color_palette)
        elif dither_method == 'bayer':
            return self.bayer_dither(enhanced, color_palette)
        else:
            return self.ordered_dither(enhanced, color_palette)
    
    def get_available_palettes(self) -> dict:
        """Return dictionary of available palettes with descriptions."""
        return {
            'cga': 'IBM CGA 16-color palette',
            'apple2': 'Apple II 16-color palette', 
            'c64': 'Commodore 64 16-color palette',
            'spectrum': 'ZX Spectrum 16-color palette'
        }
