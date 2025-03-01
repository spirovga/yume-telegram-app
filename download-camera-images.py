#!/usr/bin/env python3
import os
import requests
import time

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# User agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Camera image sources (using reliable, public domain or freely licensed sources)
camera_images = {
    'sony-a7iii.jpg': 'https://cdn.pixabay.com/photo/2019/10/14/13/38/sony-4549262_1280.jpg',
    'canon-eos-r5.jpg': 'https://cdn.pixabay.com/photo/2020/08/05/20/56/camera-5466033_1280.jpg',
    'nikon-z6ii.jpg': 'https://cdn.pixabay.com/photo/2021/01/01/21/09/nikon-5880661_1280.jpg',
    'blackmagic-pocket-6k.jpg': 'https://cdn.pixabay.com/photo/2021/01/05/07/02/video-camera-5890781_1280.jpg',
    'fujifilm-xt4.jpg': 'https://cdn.pixabay.com/photo/2019/12/31/09/13/camera-4730434_1280.jpg'
}

def download_image(url, filename):
    """Download image from URL and save to file"""
    print(f"Downloading {filename} from {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Check if it's an actual image by examining content type
            if 'image' in response.headers.get('Content-Type', ''):
                with open(f"images/{filename}", 'wb') as f:
                    f.write(response.content)
                
                # Check if file was created successfully
                if os.path.exists(f"images/{filename}") and os.path.getsize(f"images/{filename}") > 0:
                    print(f"✓ Successfully downloaded {filename}")
                    return True
                else:
                    print(f"✗ File was created but is empty: {filename}")
                    return False
            else:
                print(f"✗ URL did not return an image: {url}")
                return False
        else:
            print(f"✗ Failed to download from {url}: HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
        return False

def main():
    print("Downloading camera equipment images...")
    
    # Clean up any zero-byte files from previous attempts
    for filename in os.listdir('images'):
        file_path = os.path.join('images', filename)
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)
            print(f"Removed empty file: {filename}")
    
    # Download each camera image
    success_count = 0
    
    for filename, url in camera_images.items():
        if download_image(url, filename):
            success_count += 1
        
        # Short delay between downloads
        time.sleep(1)
    
    print(f"\nDownloaded {success_count} of {len(camera_images)} images")
    
    # List downloaded files
    print("\nFiles in images directory:")
    for filename in sorted(os.listdir('images')):
        file_size = os.path.getsize(os.path.join('images', filename)) / 1024  # Size in KB
        print(f" - {filename} ({file_size:.1f} KB)")
    
    print("\nIMPORTANT: These are sample public domain images.")
    print("For your production app, you should download actual product images from yume.rent")

if __name__ == "__main__":
    main() 