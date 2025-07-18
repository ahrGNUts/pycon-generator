#!/usr/bin/env python3
"""
Random Geometric SVG Icon Generator

This script generates random geometric SVG icons with up to 4 colors.
Icons are saved in the same directory as the script.
"""

import random
import colorsys
import os
import argparse
import math
from pathlib import Path
import svgwrite
from svgwrite import rgb


class RandomSVGIconGenerator:
    def __init__(self, width=200, height=200, max_colors=4):
        self.width = width
        self.height = height
        self.max_colors = max_colors
        self.colors = []
        self.shapes = ['circle', 'rectangle', 'triangle', 'polygon', 'ellipse']
        
    def generate_color_palette(self):
        """Generate a random color palette with 1-4 colors"""
        num_colors = random.randint(1, self.max_colors)
        self.colors = []
        
        # Generate colors with good contrast and variety
        base_hue = random.random()
        for i in range(num_colors):
            # Vary hue while maintaining good saturation and lightness
            hue = (base_hue + (i * 0.3)) % 1.0
            saturation = random.uniform(0.6, 1.0)
            lightness = random.uniform(0.3, 0.8)
            
            rgb_color = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb_color[0] * 255),
                int(rgb_color[1] * 255),
                int(rgb_color[2] * 255)
            )
            self.colors.append(hex_color)
    
    def get_random_color(self):
        """Get a random color from the current palette"""
        return random.choice(self.colors)
    
    def create_circle(self, dwg):
        """Create a random circle"""
        cx = random.randint(0, self.width)
        cy = random.randint(0, self.height)
        r = random.randint(10, min(self.width, self.height) // 4)
        
        fill_color = self.get_random_color()
        stroke_color = self.get_random_color() if random.choice([True, False]) else 'none'
        stroke_width = random.randint(1, 5) if stroke_color != 'none' else 0
        
        return dwg.circle(
            center=(cx, cy),
            r=r,
            fill=fill_color,
            stroke=stroke_color,
            stroke_width=stroke_width,
            opacity=random.uniform(0.7, 1.0)
        )
    
    def create_rectangle(self, dwg):
        """Create a random rectangle"""
        x = random.randint(0, self.width // 2)
        y = random.randint(0, self.height // 2)
        width = random.randint(20, self.width - x)
        height = random.randint(20, self.height - y)
        
        fill_color = self.get_random_color()
        stroke_color = self.get_random_color() if random.choice([True, False]) else 'none'
        stroke_width = random.randint(1, 5) if stroke_color != 'none' else 0
        
        # Optional rotation
        transform = ""
        if random.choice([True, False]):
            angle = random.randint(-45, 45)
            center_x = x + width // 2
            center_y = y + height // 2
            transform = f"rotate({angle} {center_x} {center_y})"
        
        rect = dwg.rect(
            insert=(x, y),
            size=(width, height),
            fill=fill_color,
            stroke=stroke_color,
            stroke_width=stroke_width,
            opacity=random.uniform(0.7, 1.0)
        )
        
        if transform:
            rect.attribs['transform'] = transform
            
        return rect
    
    def create_triangle(self, dwg):
        """Create a random triangle"""
        points = []
        for _ in range(3):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            points.append((x, y))
        
        fill_color = self.get_random_color()
        stroke_color = self.get_random_color() if random.choice([True, False]) else 'none'
        stroke_width = random.randint(1, 5) if stroke_color != 'none' else 0
        
        return dwg.polygon(
            points=points,
            fill=fill_color,
            stroke=stroke_color,
            stroke_width=stroke_width,
            opacity=random.uniform(0.7, 1.0)
        )
    
    def create_polygon(self, dwg):
        """Create a random polygon (4-8 sides)"""
        num_sides = random.randint(4, 8)
        center_x = random.randint(50, self.width - 50)
        center_y = random.randint(50, self.height - 50)
        radius = random.randint(20, 80)
        
        points = []
        for i in range(num_sides):
            angle = (2 * math.pi * i) / num_sides
            radius_variation = random.uniform(0.7, 1.3)
            x = center_x + radius * radius_variation * math.cos(angle)
            y = center_y + radius * radius_variation * math.sin(angle)
            points.append((x, y))
        
        fill_color = self.get_random_color()
        stroke_color = self.get_random_color() if random.choice([True, False]) else 'none'
        stroke_width = random.randint(1, 5) if stroke_color != 'none' else 0
        
        return dwg.polygon(
            points=points,
            fill=fill_color,
            stroke=stroke_color,
            stroke_width=stroke_width,
            opacity=random.uniform(0.7, 1.0)
        )
    
    def create_ellipse(self, dwg):
        """Create a random ellipse"""
        cx = random.randint(0, self.width)
        cy = random.randint(0, self.height)
        rx = random.randint(15, self.width // 4)
        ry = random.randint(15, self.height // 4)
        
        fill_color = self.get_random_color()
        stroke_color = self.get_random_color() if random.choice([True, False]) else 'none'
        stroke_width = random.randint(1, 5) if stroke_color != 'none' else 0
        
        # Optional rotation
        transform = ""
        if random.choice([True, False]):
            angle = random.randint(0, 180)
            transform = f"rotate({angle} {cx} {cy})"
        
        ellipse = dwg.ellipse(
            center=(cx, cy),
            r=(rx, ry),
            fill=fill_color,
            stroke=stroke_color,
            stroke_width=stroke_width,
            opacity=random.uniform(0.7, 1.0)
        )
        
        if transform:
            ellipse.attribs['transform'] = transform
            
        return ellipse
    
    def create_shape(self, dwg, shape_type):
        """Create a shape based on the specified type"""
        shape_methods = {
            'circle': self.create_circle,
            'rectangle': self.create_rectangle,
            'triangle': self.create_triangle,
            'polygon': self.create_polygon,
            'ellipse': self.create_ellipse
        }
        
        return shape_methods[shape_type](dwg)
    
    def generate_icon(self, filename, num_shapes=None):
        """Generate a complete SVG icon"""
        # Create SVG drawing
        dwg = svgwrite.Drawing(filename, size=(self.width, self.height))
        
        # Generate color palette
        self.generate_color_palette()
        
        # Random background (sometimes)
        if random.choice([True, False]):
            bg_color = self.get_random_color()
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill=bg_color,
                opacity=random.uniform(0.1, 0.3)
            ))
        
        # Determine number of shapes
        if num_shapes is None:
            num_shapes = random.randint(2, 8)
        
        # Generate shapes
        for _ in range(num_shapes):
            shape_type = random.choice(self.shapes)
            shape = self.create_shape(dwg, shape_type)
            dwg.add(shape)
        
        # Save the SVG
        dwg.save()
        print(f"Generated icon: {filename}")
        return filename


def main():
    parser = argparse.ArgumentParser(description='Generate random geometric SVG icons')
    parser.add_argument('-n', '--num-icons', type=int, default=5, 
                       help='Number of icons to generate (default: 5)')
    parser.add_argument('-s', '--size', type=int, default=200, 
                       help='Icon size in pixels (default: 200)')
    parser.add_argument('-c', '--max-colors', type=int, default=4, 
                       help='Maximum colors per icon (default: 4)')
    parser.add_argument('--shapes', type=int, default=None, 
                       help='Number of shapes per icon (default: random 2-8)')
    parser.add_argument('--prefix', type=str, default='icon', 
                       help='Filename prefix (default: icon)')
    
    args = parser.parse_args()
    
    # Create generator
    generator = SVGIconGenerator(
        width=args.size, 
        height=args.size, 
        max_colors=args.max_colors
    )
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Generate icons
    print(f"Generating {args.num_icons} SVG icons...")
    print(f"Size: {args.size}x{args.size} pixels")
    print(f"Max colors per icon: {args.max_colors}")
    print(f"Saving to: {script_dir}")
    print("-" * 40)
    
    generated_files = []
    for i in range(args.num_icons):
        filename = script_dir / f"{args.prefix}_{i+1:03d}.svg"
        generator.generate_icon(str(filename), args.shapes)
        generated_files.append(filename.name)
    
    print("-" * 40)
    print(f"Successfully generated {len(generated_files)} icons:")
    for filename in generated_files:
        print(f"  {filename}")


if __name__ == "__main__":
    main() 