#!/usr/bin/env python3
import os
import requests
import shutil

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Camera filenames
camera_files = [
    'sony-a7iii.jpg',
    'canon-eos-r5.jpg',
    'nikon-z6ii.jpg',
    'blackmagic-pocket-6k.jpg',
    'fujifilm-xt4.jpg'
]

# Direct image URLs for cameras from online sources that allow direct embedding
image_urls = [
    # Sony Alpha
    'https://images.unsplash.com/photo-1621520291095-aa6c7137f548?q=80&w=1200&auto=format',
    # Canon camera
    'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?q=80&w=1200&auto=format',
    # Nikon camera
    'https://images.unsplash.com/photo-1617866582289-bbc3e69a682b?q=80&w=1200&auto=format',
    # Professional video camera
    'https://images.unsplash.com/photo-1589872307379-0ffdf9829123?q=80&w=1200&auto=format',
    # Fujifilm style camera
    'https://images.unsplash.com/photo-1588458030516-dbf4dfd41a0d?q=80&w=1200&auto=format'
]

def download_image(url, filename):
    """Download an image from a URL to a file"""
    print(f"Downloading: {filename}")
    
    try:
        # Stream the image to avoid loading the whole file into memory
        with requests.get(url, stream=True) as response:
            if response.status_code == 200:
                # Open the file in write-binary mode
                with open(os.path.join('images', filename), 'wb') as f:
                    # Copy the image content to the file
                    shutil.copyfileobj(response.raw, f)
                print(f"✓ Successfully downloaded {filename}")
                return True
            else:
                print(f"✗ Failed to download {filename}: {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Error downloading {filename}: {e}")
        return False

def main():
    print("Downloading camera equipment images...")
    
    # Delete empty files from previous attempts
    for filename in os.listdir('images'):
        file_path = os.path.join('images', filename)
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)
            print(f"Removed empty file: {filename}")
    
    # Download images
    success_count = 0
    
    for i, filename in enumerate(camera_files):
        if i < len(image_urls):
            if download_image(image_urls[i], filename):
                success_count += 1
    
    print(f"\nDownloaded {success_count} of {len(camera_files)} camera images.")
    
    # List all files in images directory
    print("\nFiles in images directory:")
    for filename in sorted(os.listdir('images')):
        file_path = os.path.join('images', filename)
        if os.path.isfile(file_path):
            size_kb = os.path.getsize(file_path) / 1024
            print(f" - {filename} ({size_kb:.1f} KB)")
    
    print("\nIMPORTANT: These are sample images from Unsplash.")
    print("For your production app, download actual product images from yume.rent")
    print("Attribution: Images from Unsplash.com used under Unsplash License")

if __name__ == "__main__":
    main() 