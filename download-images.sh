#!/bin/bash

# Create images directory if it doesn't exist
mkdir -p images

echo "Downloading camera equipment images..."

# Define camera models and direct image URLs (all from Wikimedia Commons or other free sources)
declare -A camera_images
camera_images["sony-a7iii"]="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Sony_Alpha_7_II.jpg/1200px-Sony_Alpha_7_II.jpg"
camera_images["canon-eos-r5"]="https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Canon_EOS_R5_with_mount_cap.jpg/1200px-Canon_EOS_R5_with_mount_cap.jpg"
camera_images["nikon-z6ii"]="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Nikon_Z6_II_%28cropped%29.jpg/1200px-Nikon_Z6_II_%28cropped%29.jpg"
camera_images["blackmagic-pocket-6k"]="https://upload.wikimedia.org/wikipedia/commons/d/d7/Blackmagic_Pocket_Cinema_Camera_6K.jpg"
camera_images["fujifilm-xt4"]="https://upload.wikimedia.org/wikipedia/commons/b/be/Fujifilm_X-T4.jpg"

# Download each camera image
for camera in "sony-a7iii" "canon-eos-r5" "nikon-z6ii" "blackmagic-pocket-6k" "fujifilm-xt4"; do
  echo "Downloading: $camera.jpg"
  curl -s -o "images/$camera.jpg" "${camera_images[$camera]}"
  
  # Check if download was successful
  if [ -s "images/$camera.jpg" ]; then
    echo "✓ Successfully downloaded $camera.jpg"
  else
    echo "✗ Failed to download $camera.jpg"
    rm -f "images/$camera.jpg"  # Remove empty file
  fi
done

echo ""
echo "Image download complete."
echo ""
echo "IMPORTANT: These are sample images from Wikimedia Commons."
echo "For your production app, you should:"
echo "1. Visit yume.rent to manually download camera images"
echo "2. Replace these sample images with the ones from yume.rent"
echo "3. Make sure the filenames match those in app.js"
echo ""
echo "The following files should be in your images directory:"
ls -la images/ 