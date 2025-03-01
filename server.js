const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3001;

// Enable CORS for all routes
app.use(cors());

// Parse JSON request body
app.use(express.json());

// Serve static files
app.use(express.static(path.join(__dirname)));

// API route to get all cameras
app.get('/api/cameras', (req, res) => {
    try {
        const cameraData = fs.readFileSync(path.join(__dirname, 'camera-data.json'), 'utf8');
        const cameras = JSON.parse(cameraData);
        
        // Add more details to each camera
        const enhancedCameras = cameras.map((camera, index) => {
            const priceBase = 1000 + (index % 7) * 500;
            const typeKeywords = ['DSLR', 'Mirrorless', 'Medium Format', 'Compact', 'Film', 'Action'];
            const typeIndex = index % typeKeywords.length;
            
            return {
                id: index + 1,
                name: camera.name,
                specs: `${typeKeywords[typeIndex]} Camera`,
                description: `Professional ${typeKeywords[typeIndex]} camera for photography enthusiasts.`,
                price: priceBase,
                image: `images/${camera.image}`
            };
        });
        
        res.json(enhancedCameras);
    } catch (error) {
        console.error('Error reading camera data:', error);
        res.status(500).json({ error: 'Failed to load camera data' });
    }
});

// API route to get colors
app.get('/api/colors', (req, res) => {
    try {
        const colorData = fs.readFileSync(path.join(__dirname, 'yume-colors.json'), 'utf8');
        const colors = JSON.parse(colorData);
        res.json(colors);
    } catch (error) {
        console.error('Error reading color data:', error);
        res.status(500).json({ error: 'Failed to load color data' });
    }
});

// API route to get a single camera by ID
app.get('/api/cameras/:id', (req, res) => {
    try {
        const cameraId = parseInt(req.params.id);
        const cameraData = fs.readFileSync(path.join(__dirname, 'camera-data.json'), 'utf8');
        const cameras = JSON.parse(cameraData);
        
        // Find the camera with the specified ID
        const camera = cameras.find((c, index) => index + 1 === cameraId);
        
        if (!camera) {
            return res.status(404).json({ error: 'Camera not found' });
        }
        
        // Add more details to the camera
        const typeKeywords = ['DSLR', 'Mirrorless', 'Medium Format', 'Compact', 'Film', 'Action'];
        const typeIndex = (cameraId - 1) % typeKeywords.length;
        const priceBase = 1000 + ((cameraId - 1) % 7) * 500;
        
        const enhancedCamera = {
            id: cameraId,
            name: camera.name,
            specs: `${typeKeywords[typeIndex]} Camera`,
            description: `Professional ${typeKeywords[typeIndex]} camera for photography enthusiasts.`,
            price: priceBase,
            image: `images/${camera.image}`
        };
        
        res.json(enhancedCamera);
    } catch (error) {
        console.error('Error reading camera data:', error);
        res.status(500).json({ error: 'Failed to load camera data' });
    }
});

// Handle booking submissions
app.post('/api/bookings', (req, res) => {
    try {
        // In a real app, you would save this to a database
        console.log('Received booking:', req.body);
        
        // Send confirmation
        res.json({ 
            success: true, 
            message: 'Booking received successfully', 
            bookingId: `YR-${Date.now()}`
        });
    } catch (error) {
        console.error('Error processing booking:', error);
        res.status(500).json({ error: 'Failed to process booking' });
    }
});

// Catch-all route to return the main index.html for any unmatched routes
// This is important for single-page applications
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT} to access the app`);
}); 