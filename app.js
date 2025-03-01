// Initialize Telegram WebApp
let tg = window.Telegram?.WebApp;
const initData = tg?.initData || '';
const initDataUnsafe = tg?.initDataUnsafe || {};

// Enable closing confirmation for Telegram WebApp
if (tg) {
    tg.enableClosingConfirmation();
    tg.expand();
    
    // Apply theme colors if available
    document.documentElement.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
    document.documentElement.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
    document.documentElement.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color || '#999999');
    document.documentElement.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color || '#2481cc');
    document.documentElement.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#3390ec');
    document.documentElement.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
}

// DOM elements
const cameraListEl = document.getElementById('camera-list');
const bookingFormEl = document.getElementById('booking-form');
const selectedCameraEl = document.getElementById('selected-camera');
const cameraSelectEl = document.getElementById('camera-select');
const submitBtn = document.getElementById('submit-booking');
const backBtn = document.getElementById('back-to-list');
const successModal = document.getElementById('success-modal');
const closeModalBtn = document.getElementById('close-modal');
const accessoriesSelectEl = document.getElementById('accessories-select');

// State variables
let cameras = [];
let selectedCamera = null;

// Fixed accessories list
const accessories = [
    { id: 1, name: "Tripod", price: 500 },
    { id: 2, name: "Extra Battery", price: 300 },
    { id: 3, name: "Camera Bag", price: 700 },
    { id: 4, name: "SD Card (64GB)", price: 400 },
    { id: 5, name: "Flash", price: 600 },
    { id: 6, name: "Lens Filter Set", price: 800 }
];

// Fetch camera data from our JSON file
async function fetchCameraData() {
    try {
        const response = await fetch('camera-data.json');
        if (!response.ok) {
            throw new Error('Failed to fetch camera data');
        }
        
        const data = await response.json();
        
        // Process camera data to add more details
        cameras = data.map((camera, index) => {
            // Generate price and specs based on camera name to make up for missing metadata
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
        
        renderCameraList();
        populateCameraSelect();
    } catch (error) {
        console.error('Error loading camera data:', error);
        cameraListEl.innerHTML = `<p class="error">Failed to load cameras: ${error.message}</p>`;
    }
}

// Render the camera list
function renderCameraList() {
    cameraListEl.innerHTML = '';
    
    cameras.forEach(camera => {
        const cameraCard = document.createElement('div');
        cameraCard.className = 'camera-card';
        cameraCard.dataset.id = camera.id;
        
        cameraCard.innerHTML = `
            <img src="${camera.image}" alt="${camera.name}" class="camera-image">
            <div class="camera-info">
                <div class="camera-name">${camera.name}</div>
                <div class="camera-specs">${camera.specs}</div>
                <div class="camera-price">₽${camera.price}/day</div>
            </div>
        `;
        
        cameraCard.addEventListener('click', () => selectCamera(camera));
        cameraListEl.appendChild(cameraCard);
    });
}

// Populate the camera select dropdown
function populateCameraSelect() {
    cameraSelectEl.innerHTML = '<option value="">Select a camera</option>';
    
    cameras.forEach(camera => {
        const option = document.createElement('option');
        option.value = camera.id;
        option.textContent = `${camera.name} - ₽${camera.price}/day`;
        cameraSelectEl.appendChild(option);
    });
}

// Populate the accessories select dropdown
function populateAccessoriesSelect() {
    accessoriesSelectEl.innerHTML = '';
    
    accessories.forEach(accessory => {
        const option = document.createElement('option');
        option.value = accessory.id;
        option.textContent = `${accessory.name} - ₽${accessory.price}/day`;
        accessoriesSelectEl.appendChild(option);
    });
}

// Select a camera
function selectCamera(camera) {
    selectedCamera = camera;
    
    // Show the booking form and hide the camera list
    cameraListEl.parentElement.style.display = 'none';
    bookingFormEl.style.display = 'block';
    
    // Display selected camera info
    selectedCameraEl.innerHTML = `
        <img src="${camera.image}" alt="${camera.name}" class="camera-image" style="max-height: 150px; object-fit: contain;">
        <div>
            <h3>${camera.name}</h3>
            <p>${camera.specs}</p>
            <p>${camera.description}</p>
            <p class="camera-price">₽${camera.price}/day</p>
        </div>
    `;
    
    // Set the selected camera in the dropdown
    cameraSelectEl.value = camera.id;
    
    // Scroll to top of form
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Return to the camera list
function backToList() {
    bookingFormEl.style.display = 'none';
    cameraListEl.parentElement.style.display = 'block';
    selectedCamera = null;
}

// Submit booking
function submitBooking(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(bookingFormEl.querySelector('form'));
    const bookingData = {
        camera: cameras.find(c => c.id == formData.get('camera')),
        startDate: formData.get('start-date'),
        endDate: formData.get('end-date'),
        accessories: Array.from(accessoriesSelectEl.selectedOptions).map(option => 
            accessories.find(a => a.id == option.value)
        ),
        name: formData.get('name'),
        phone: formData.get('phone'),
        email: formData.get('email'),
        notes: formData.get('notes')
    };
    
    // Calculate total price
    const startDate = new Date(bookingData.startDate);
    const endDate = new Date(bookingData.endDate);
    const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) || 1;
    
    const cameraPrice = bookingData.camera ? bookingData.camera.price * days : 0;
    const accessoriesPrice = bookingData.accessories.reduce((sum, acc) => sum + acc.price * days, 0);
    const totalPrice = cameraPrice + accessoriesPrice;
    
    // Show success message
    document.getElementById('booking-details').innerHTML = `
        <p><strong>Equipment:</strong> ${bookingData.camera ? bookingData.camera.name : 'No camera selected'}</p>
        <p><strong>Rental Period:</strong> ${bookingData.startDate} to ${bookingData.endDate} (${days} day${days !== 1 ? 's' : ''})</p>
        <p><strong>Accessories:</strong> ${bookingData.accessories.length > 0 ? bookingData.accessories.map(a => a.name).join(', ') : 'None'}</p>
        <p><strong>Total Price:</strong> ₽${totalPrice}</p>
    `;
    
    // Show modal
    successModal.style.display = 'flex';
    
    // Send data to Telegram
    if (tg && tg.MainButton) {
        tg.MainButton.setText('Booking Completed!');
        tg.MainButton.show();
        
        // Send data to the bot
        tg.sendData(JSON.stringify(bookingData));
    }
}

// Close the modal
function closeModal() {
    successModal.style.display = 'none';
    backToList();
    
    // Reset form
    bookingFormEl.querySelector('form').reset();
}

// Event listeners
if (backBtn) backBtn.addEventListener('click', backToList);
if (submitBtn) submitBtn.addEventListener('click', submitBooking);
if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchCameraData();
    populateAccessoriesSelect();
    
    // Initially hide the booking form
    if (bookingFormEl) bookingFormEl.style.display = 'none';
}); 