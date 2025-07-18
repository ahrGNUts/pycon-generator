#!/usr/bin/env python3
"""
Diagonal Pattern SVG Generator

This script generates SVG files with random diagonal patterns in a grid,
based on the p5.js sketch from script.js. Creates patterns using two types
of diagonal lines with configurable colors and transparency effects.
"""

import random
import colorsys
import argparse
import math
from pathlib import Path
import svgwrite


class DiagonalPatternGenerator:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        

        
    def hsb_to_rgb(self, h, s, b):
        """Convert HSB (p5.js style) to RGB hex string"""
        # p5.js HSB: H=0-360, S=0-100, B=0-100
        # Python HSV: H=0-1, S=0-1, V=0-1
        h_norm = (h % 360) / 360.0
        s_norm = s / 100.0
        v_norm = b / 100.0
        
        rgb = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)
        return '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
    
    def generate_random_color(self):
        """Generate a random color with good saturation and brightness"""
        hue = random.randint(0, 360)
        saturation = random.randint(60, 100)  # Good saturation
        brightness = random.randint(40, 90)   # Avoid too dark or too bright
        return self.hsb_to_rgb(hue, saturation, brightness)

    
    def create_diagonal_pattern(self, dwg, tile_count, stroke_weight, random_seed=None, 
                              color_left=None, color_right=None):
        """Create the diagonal pattern based on script.js logic"""
        
        if random_seed is not None:
            random.seed(random_seed)
        
        tile_size = self.width / tile_count
        
        for grid_y in range(tile_count):
            for grid_x in range(tile_count):
                pos_x = tile_size * grid_x
                pos_y = tile_size * grid_y
                
                # Random toggle between two diagonal patterns (like script.js)
                toggle = random.randint(0, 1)
                
                if toggle == 0:
                    # Pattern 0: Left-leaning diagonals (\)
                    # Two line segments forming the pattern
                    line1 = dwg.line(
                        start=(pos_x, pos_y),
                        end=(pos_x + tile_size / 2, pos_y + tile_size),
                        stroke=color_left,
                        stroke_width=stroke_weight
                    )
                    line2 = dwg.line(
                        start=(pos_x + tile_size / 2, pos_y),
                        end=(pos_x + tile_size, pos_y + tile_size),
                        stroke=color_left,
                        stroke_width=stroke_weight
                    )
                    dwg.add(line1)
                    dwg.add(line2)
                    
                else:
                    # Pattern 1: Right-leaning diagonals (/)
                    # Two line segments forming the pattern
                    line1 = dwg.line(
                        start=(pos_x, pos_y + tile_size),
                        end=(pos_x + tile_size / 2, pos_y),
                        stroke=color_right,
                        stroke_width=stroke_weight
                    )
                    line2 = dwg.line(
                        start=(pos_x + tile_size / 2, pos_y + tile_size),
                        end=(pos_x + tile_size, pos_y),
                        stroke=color_right,
                        stroke_width=stroke_weight
                    )
                    dwg.add(line1)
                    dwg.add(line2)
    
    def generate_pattern(self, filename, tile_count=20, stroke_weight=8, random_seed=None):
        """Generate a complete SVG pattern"""
        
        # Generate two random colors for this pattern
        color_left = self.generate_random_color()
        color_right = self.generate_random_color()
        
        # Create SVG drawing
        dwg = svgwrite.Drawing(filename, size=(self.width, self.height))
        
        # Add white background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(self.width, self.height),
            fill='white'
        ))
        
        # Generate the diagonal pattern
        self.create_diagonal_pattern(
            dwg, tile_count, stroke_weight, random_seed,
            color_left, color_right
        )
        
        # Save the SVG
        dwg.save()
        print(f"Generated pattern: {filename}")
        return filename


def main():
    parser = argparse.ArgumentParser(description='Generate diagonal pattern SVG files')
    parser.add_argument('-n', '--num-patterns', type=int, default=5,
                       help='Number of patterns to generate (default: 5)')
    parser.add_argument('-s', '--size', type=int, default=600,
                       help='Canvas size in pixels (default: 600)')
    parser.add_argument('-t', '--tiles', type=int, default=20,
                       help='Number of tiles per side (default: 20)')
    parser.add_argument('-w', '--stroke-weight', type=float, default=8.0,
                       help='Line stroke weight (default: 8.0)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducible patterns')
    parser.add_argument('--prefix', type=str, default='diagonal_pattern',
                       help='Filename prefix (default: diagonal_pattern)')
    
    args = parser.parse_args()
    
    # Create generator
    generator = DiagonalPatternGenerator(width=args.size, height=args.size)
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Generate patterns
    print(f"Generating {args.num_patterns} diagonal pattern SVGs...")
    print(f"Size: {args.size}x{args.size} pixels")
    print(f"Tiles: {args.tiles}x{args.tiles}")
    print(f"Stroke weight: {args.stroke_weight}")
    print(f"Saving to: {script_dir}")
    print("-" * 50)
    
    generated_files = []
    for i in range(args.num_patterns):
        # Use different seeds for each pattern if no specific seed provided
        if args.seed is not None:
            pattern_seed = args.seed + i
        else:
            pattern_seed = None
            
        filename = script_dir / f"{args.prefix}_{i+1:03d}.svg"
        generator.generate_pattern(
            str(filename),
            tile_count=args.tiles,
            stroke_weight=args.stroke_weight,
            random_seed=pattern_seed
        )
        generated_files.append(filename.name)
    
    print("-" * 50)
    print(f"Successfully generated {len(generated_files)} patterns:")
    for filename in generated_files:
        print(f"  {filename}")


if __name__ == "__main__":
    main() 