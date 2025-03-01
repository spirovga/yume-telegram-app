# Deployment Instructions

## Step 1: Download Images from yume.rent

1. Visit yume.rent and find suitable camera equipment images
2. Save images to your local project folder in a new directory named `images`
3. Aim for at least 5 high-quality images matching the equipment in your app.js

## Step 2: Update app.js to use local images

```javascript
// Update the camera data to use local images
const cameras = [
    {
        id: 1,
        name: 'Sony Alpha A7 III',
        specs: 'Полнокадровая беззеркальная камера, 24.2 МП',
        description: 'Профессиональная полнокадровая камера с отличным качеством изображения и видео 4K.',
        price: 3500,
        priceUnit: '₽/день',
        image: 'images/sony-a7iii.jpg' // Change to your local image path
    },
    // Update other camera entries similarly
];
```

## Step 3: Deploy to GitHub Pages

1. Create a new GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Yume.rent Telegram mini app"
   ```

2. Create a new repository on GitHub through the web interface

3. Connect your local repository to GitHub:
   ```bash
   git remote add origin git@github.com:yourusername/yume-telegram-app.git
   git branch -M main
   git push -u origin main
   ```

4. Enable GitHub Pages:
   - Go to your repository on GitHub
   - Navigate to Settings > Pages
   - Under "Source", select "main" branch
   - Click "Save"

5. Your site will be published at `https://yourusername.github.io/yume-telegram-app/`

## Step 4: Configure Telegram Bot to Use Your GitHub Pages URL

1. Talk to @BotFather on Telegram
2. Set up your bot's menu button with the `/setmenubutton` command
3. Provide your GitHub Pages URL when prompted
4. Test the functionality by opening your bot in Telegram

Remember to update your README.md with the new deployment details. 