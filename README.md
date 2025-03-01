# Yume Camera Rental - Telegram Mini App

A Telegram Mini App for renting camera equipment, featuring a catalog of cameras scraped from yume.rent.

## Features

- Camera catalog with images and details
- Rental booking system
- Integration with Telegram Mini App platform
- Mobile-friendly responsive design

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

## Running the app

Start the development server:

```bash
npm run dev
```

Or run in production mode:

```bash
npm start
```

The app will be available at http://localhost:3001

## Setting up with Telegram Bot

To use this as a Telegram Mini App:

1. Create a bot using [@BotFather](https://t.me/BotFather)
2. Use the /newapp command to set up a mini app for your bot
3. Enter the URL where you've deployed this application
4. Configure the bot to handle the data received from the mini app

## Project Structure

- `server.js`: Express server for serving the app
- `index.html`: Main HTML structure
- `app.js`: Client-side JavaScript for the app
- `style.css`: Styling for the application
- `camera-data.json`: Camera data scraped from yume.rent
- `images/`: Directory containing camera images

## Customizing

You can modify the following files to customize the app:

- `style.css`: Change colors, layout, and visual appearance
- `app.js`: Modify functionality and behavior
- `index.html`: Update content and structure
- `server.js`: Add or modify API endpoints

## Camera Data

The camera data was scraped from yume.rent using a Python script. The images are stored in the `images/` directory, and the metadata is stored in `camera-data.json`.

## License

MIT 