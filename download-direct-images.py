#!/usr/bin/env python3
import os
import requests
import time

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Camera image URLs from reliable sources that allow direct linking
camera_images = {
    'sony-a7iii.jpg': 'https://live.staticflickr.com/5564/30725680245_6e01dfa2de_b.jpg',
    'canon-eos-r5.jpg': 'https://live.staticflickr.com/65535/50138388087_db620284c5_b.jpg',
    'nikon-z6ii.jpg': 'https://live.staticflickr.com/65535/51051550162_6b147605e2_b.jpg',
    'blackmagic-pocket-6k.jpg': 'https://live.staticflickr.com/65535/48486111867_d496c1ecc5_b.jpg',
    'fujifilm-xt4.jpg': 'https://live.staticflickr.com/65535/49600169533_cafef60bd5_b.jpg'
}

# Function to download an image
def download_image(url, filename):
    """Download image from URL and save to filename"""
    print(f"Downloading {filename}...")
    try:
        # Add Mozilla user agent and referrer to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Save the image content to a file
            with open(os.path.join('images', filename), 'wb') as f:
                f.write(response.content)
            
            # Check file size
            file_size = os.path.getsize(os.path.join('images', filename))
            if file_size > 10000:  # Larger than 10KB is likely a real image
                print(f"✓ Successfully downloaded {filename} ({file_size/1024:.1f} KB)")
                return True
            else:
                print(f"✗ Downloaded file is too small: {filename} ({file_size/1024:.1f} KB)")
                return False
        else:
            print(f"✗ Failed to download {filename}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")
        return False

def main():
    print("Downloading camera equipment images...")
    
    # Delete any small files from previous attempts
    for filename in os.listdir('images'):
        file_path = os.path.join('images', filename)
        if os.path.isfile(file_path) and os.path.getsize(file_path) < 5000:  # Less than 5KB
            os.remove(file_path)
            print(f"Removed small file: {filename}")
    
    # Download each camera image
    success_count = 0
    
    for filename, url in camera_images.items():
        if download_image(url, filename):
            success_count += 1
        time.sleep(1)  # Delay to avoid rate limiting
    
    # If we failed to download any images, use a fallback method
    if success_count < len(camera_images):
        print("\nSome images couldn't be downloaded. Creating placeholder images...")
        
        # Create placeholder colored images for any missing files
        import numpy as np
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            colors = {
                'sony-a7iii.jpg': (30, 144, 255),       # DodgerBlue
                'canon-eos-r5.jpg': (220, 20, 60),      # Crimson
                'nikon-z6ii.jpg': (255, 215, 0),        # Gold
                'blackmagic-pocket-6k.jpg': (0, 0, 0),  # Black
                'fujifilm-xt4.jpg': (46, 139, 87)       # SeaGreen
            }
            
            for filename in camera_images.keys():
                if not os.path.exists(os.path.join('images', filename)) or os.path.getsize(os.path.join('images', filename)) < 5000:
                    color = colors.get(filename, (100, 100, 100))
                    
                    # Create a colored image with text
                    img = Image.new('RGB', (800, 600), color)
                    d = ImageDraw.Draw(img)
                    
                    # Add text (camera model)
                    model_name = filename.replace('.jpg', '').replace('-', ' ').upper()
                    d.text((400, 300), model_name, fill=(255, 255, 255), anchor="mm")
                    
                    # Save the image
                    img.save(os.path.join('images', filename))
                    print(f"Created placeholder image for {filename}")
                    success_count += 1
        except ImportError:
            print("PIL (Pillow) library not available. Can't create placeholder images.")
            print("Install with: pip install Pillow")
    
    print(f"\nSuccessfully prepared {success_count} of {len(camera_images)} camera images")
    
    # List all images in the directory
    print("\nFiles in images directory:")
    for filename in sorted(os.listdir('images')):
        file_path = os.path.join('images', filename)
        if os.path.isfile(file_path):
            size_kb = os.path.getsize(file_path) / 1024
            print(f" - {filename} ({size_kb:.1f} KB)")

    print("\nIMPORTANT: These are sample images.")
    print("For your production app, download actual product images from yume.rent")

if __name__ == "__main__":
    main() 