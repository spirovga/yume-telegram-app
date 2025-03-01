#!/usr/bin/env python3
import requests
import json
import os
import re
import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

def save_image(img, filename):
    """Save image in its original format with transparency if available."""
    img.save(filename, 'PNG')
    return True

def extract_colors_and_images():
    # Set up headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        url = "https://yume.rent/"
        print(f"Opening {url}...")
        driver.get(url)
        
        # Wait for page to load content
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Extract colors from computed styles
        colors = {}
        # Try to extract CSS custom properties
        print("Extracting colors...")
        css_vars = driver.execute_script("""
            var styles = getComputedStyle(document.documentElement);
            var cssVars = {};
            for (var i = 0; i < styles.length; i++) {
                var prop = styles[i];
                if (prop.startsWith('--')) {
                    cssVars[prop] = styles.getPropertyValue(prop).trim();
                }
            }
            return cssVars;
        """)
        
        for var_name, color_value in css_vars.items():
            if color_value.startswith('#'):
                colors[var_name.replace('--', '')] = color_value
        
        # If no colors found, try another approach
        if not colors:
            print("No CSS variables found, trying alternative approach...")
            # Look for background-color, color properties in main elements
            main_elements = driver.find_elements(By.CSS_SELECTOR, 'header, footer, main, body, h1, h2, h3, button')
            for elem in main_elements:
                bg_color = driver.execute_script('return window.getComputedStyle(arguments[0]).backgroundColor', elem)
                if bg_color and bg_color != 'rgba(0, 0, 0, 0)':
                    key = f"bg-{elem.tag_name}"
                    colors[key] = bg_color
                
                text_color = driver.execute_script('return window.getComputedStyle(arguments[0]).color', elem)
                if text_color:
                    key = f"text-{elem.tag_name}"
                    colors[key] = text_color
        
        # Save colors to JSON
        with open('yume-colors.json', 'w') as f:
            json.dump(colors, f, indent=2)
        print(f"Extracted {len(colors)} colors and saved to yume-colors.json")
        
        # Extract camera equipment images
        print("Looking for camera products...")
        cameras = []
        
        # Take a screenshot for debugging
        driver.save_screenshot("page_screenshot.png")
        print("Saved page screenshot to page_screenshot.png")
        
        # Print page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Saved page source to page_source.html")
        
        # Try different selectors to find product elements
        product_elements = driver.find_elements(By.CSS_SELECTOR, '.product-card, .camera-card, .equipment-card, [class*="product"], [class*="camera"], [class*="equipment"]')
        print(f"Found {len(product_elements)} product elements with primary selectors")
        
        # If nothing found, try finding any element with image and heading
        if not product_elements:
            product_elements = driver.find_elements(By.CSS_SELECTOR, 'div:has(img):has(h2), div:has(img):has(h3), div:has(img):has(h4), div:has(img):has(p)')
            print(f"Found {len(product_elements)} product elements with secondary selectors")
        
        # As a fallback, just get all images
        if not product_elements:
            print("No product elements found, falling back to all images...")
            img_elements = driver.find_elements(By.TAG_NAME, 'img')
            print(f"Found {len(img_elements)} image elements")
            
            for i, img in enumerate(img_elements):
                if i > 15:  # Limit to 15 images to avoid getting icons, etc.
                    break
                    
                src = img.get_attribute('src')
                if src and (src.endswith('.jpg') or src.endswith('.png') or src.endswith('.jpeg')):
                    # Try to get alt text as name, or use index
                    name = img.get_attribute('alt') or f"camera-{i+1}"
                    filename = name.lower().replace(' ', '-')
                    filename = re.sub(r'[^\w\-]', '', filename) + '.png'
                    
                    try:
                        print(f"Downloading image from {src}...")
                        img_response = requests.get(src)
                        img_response.raise_for_status()
                        img_obj = Image.open(BytesIO(img_response.content))
                        
                        # Skip small images (likely icons)
                        if img_obj.width < 100 or img_obj.height < 100:
                            print(f"Skipping small image: {img_obj.width}x{img_obj.height}")
                            continue
                        
                        if save_image(img_obj, f"images/{filename}"):
                            print(f"Downloaded image: images/{filename}")
                            cameras.append({"name": name, "image": filename})
                    except Exception as e:
                        print(f"Error downloading {src}: {e}")
        else:
            # Process found product elements
            for i, elem in enumerate(product_elements):
                try:
                    # Try to get title element
                    title_elem = elem.find_element(By.CSS_SELECTOR, 'h2, h3, h4, [class*="title"], [class*="name"]')
                    name = title_elem.text.strip()
                except:
                    name = f"camera-{i+1}"
                
                print(f"Processing product: {name}")
                
                # Normalize name for filename
                filename = name.lower().replace(' ', '-')
                filename = re.sub(r'[^\w\-]', '', filename) + '.png'
                
                # Try to get image
                try:
                    img_elem = elem.find_element(By.TAG_NAME, 'img')
                    src = img_elem.get_attribute('src')
                    
                    if src:
                        print(f"Downloading image from {src}...")
                        img_response = requests.get(src)
                        img_response.raise_for_status()
                        img_obj = Image.open(BytesIO(img_response.content))
                        
                        if save_image(img_obj, f"images/{filename}"):
                            print(f"Downloaded image for {name}: images/{filename}")
                            cameras.append({"name": name, "image": filename})
                except Exception as e:
                    print(f"Error processing element {i}: {e}")
        
        # Save camera data to JSON
        with open('camera-data.json', 'w') as f:
            json.dump(cameras, f, indent=2)
        print(f"Extracted data for {len(cameras)} cameras and saved to camera-data.json")
        
        # Close the browser
        driver.quit()
        
    except Exception as e:
        print(f"Error scraping data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    extract_colors_and_images() 