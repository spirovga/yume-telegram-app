#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Referer': 'https://www.google.com/'
}

# Target filenames
target_filenames = [
    'sony-a7iii.jpg',
    'canon-eos-r5.jpg',
    'nikon-z6ii.jpg',
    'blackmagic-pocket-6k.jpg',
    'fujifilm-xt4.jpg'
]

# Function to download image
def download_image(url, filename):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(f"images/{filename}", 'wb') as f:
                f.write(response.content)
            print(f"✓ Successfully downloaded {filename}")
            return True
        else:
            print(f"✗ Failed to download {url} - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
        return False

def scrape_yume_rent():
    print("Scraping yume.rent for camera images...")
    
    try:
        # Get the main page
        response = requests.get('https://yume.rent', headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to access yume.rent - Status code: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all image elements
        images = []
        
        # Look for img tags
        for img in soup.find_all('img'):
            if img.get('src'):
                images.append(urljoin('https://yume.rent', img.get('src')))
        
        # Look for images in CSS backgrounds
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                # Find urls in CSS
                urls = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', style_tag.string)
                for url in urls:
                    if url.endswith(('.jpg', '.jpeg', '.png')):
                        images.append(urljoin('https://yume.rent', url))
        
        # Look for background image in style attributes
        for tag in soup.find_all(lambda tag: tag.has_attr('style') and 'background' in tag['style']):
            urls = re.findall(r'url\([\'"]?(.*?)[\'"]?\)', tag['style'])
            for url in urls:
                if url.endswith(('.jpg', '.jpeg', '.png')):
                    images.append(urljoin('https://yume.rent', url))
        
        print(f"Found {len(images)} potential images on yume.rent")
        return images
    
    except Exception as e:
        print(f"Error scraping yume.rent: {e}")
        return []

# Main function
def main():
    # Scrape yume.rent
    yume_images = scrape_yume_rent()
    
    # Filter for likely camera images (larger images, not icons)
    camera_images = []
    
    if yume_images:
        print("Analyzing images to find camera equipment...")
        
        for img_url in yume_images:
            try:
                # Check image size without downloading fully
                response = requests.head(img_url, headers=headers, timeout=5)
                
                # If Content-Length exists and image is larger than 20KB, it's likely not an icon
                if 'Content-Length' in response.headers and int(response.headers['Content-Length']) > 20000:
                    camera_images.append(img_url)
            except:
                # If we can't check, still keep the image as a candidate
                camera_images.append(img_url)
        
        print(f"Found {len(camera_images)} potential camera images")
    
    # If we found any images, download them
    if camera_images:
        print("\nDownloading images from yume.rent...")
        
        # Get top 5 images or as many as available
        num_images = min(len(camera_images), 5)
        
        for i in range(num_images):
            download_image(camera_images[i], target_filenames[i])
            # Add a small delay to avoid overloading the server
            time.sleep(random.uniform(0.5, 1.5))
    else:
        print("No suitable images found on yume.rent")
        
        # Fallback to Wikimedia Commons images
        print("\nFalling back to Wikimedia Commons images...")
        
        fallback_images = {
            'sony-a7iii.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Sony_Alpha_7_II.jpg/1200px-Sony_Alpha_7_II.jpg',
            'canon-eos-r5.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Canon_EOS_R5_with_mount_cap.jpg/1200px-Canon_EOS_R5_with_mount_cap.jpg', 
            'nikon-z6ii.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Nikon_Z6_II_%28cropped%29.jpg/1200px-Nikon_Z6_II_%28cropped%29.jpg',
            'blackmagic-pocket-6k.jpg': 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Blackmagic_Pocket_Cinema_Camera_6K.jpg',
            'fujifilm-xt4.jpg': 'https://upload.wikimedia.org/wikipedia/commons/b/be/Fujifilm_X-T4.jpg'
        }
        
        for filename, url in fallback_images.items():
            download_image(url, filename)
    
    print("\nImage download complete.")
    print("\nIMPORTANT: Review the downloaded images to make sure they're suitable.")
    print("If needed, download more specific images manually from yume.rent")
    
    print("\nFiles in images directory:")
    for filename in os.listdir('images'):
        print(f" - {filename}")

if __name__ == "__main__":
    main() 