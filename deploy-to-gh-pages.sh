#!/bin/bash

# GitHub Pages deployment script

# Check if git is installed
if ! [ -x "$(command -v git)" ]; then
  echo "Error: git is not installed. Please install git first."
  exit 1
fi

# Initialize git repository if not already done
if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
  
  # Check if initialization was successful
  if [ $? -ne 0 ]; then
    echo "Error: Failed to initialize git repository."
    exit 1
  fi
fi

# Check if there are any uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "Adding files to git..."
  git add .
  
  echo "Committing changes..."
  git commit -m "Initial commit for Yume.rent Telegram mini app"
  
  if [ $? -ne 0 ]; then
    echo "Error: Failed to commit changes. Please make sure your git config is set up correctly."
    echo "Run: git config --global user.email 'you@example.com'"
    echo "Run: git config --global user.name 'Your Name'"
    exit 1
  fi
fi

# Instructions for manual steps
echo ""
echo "===== GitHub Pages Deployment Steps ====="
echo ""
echo "Your Telegram mini app is ready for deployment!"
echo ""
echo "To deploy to GitHub Pages, complete these steps:"
echo ""
echo "1. Create a new repository on GitHub (if you haven't already)"
echo ""
echo "2. Connect your local repository to GitHub:"
echo "   git remote add origin git@github.com:yourusername/yume-telegram-app.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Pages in your repository settings:"
echo "   - Go to the repository on GitHub"
echo "   - Navigate to Settings > Pages"
echo "   - Under 'Source', select 'main' branch"
echo "   - Click 'Save'"
echo ""
echo "4. Your site will be published at:"
echo "   https://yourusername.github.io/yume-telegram-app/"
echo ""
echo "5. Configure your Telegram bot to use this URL:"
echo "   - Talk to @BotFather on Telegram"
echo "   - Use the /setmenubutton command"
echo "   - Provide your GitHub Pages URL when prompted"
echo ""
echo "===== End of Instructions ====="
echo ""
echo "Files ready for deployment:"
ls -la | grep -v "\.git" | grep -v "\.py" | grep -v "deploy-to-gh-pages.sh"
echo "" 