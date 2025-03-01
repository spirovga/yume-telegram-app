// Initialize Telegram WebApp
let tg = window.Telegram.WebApp;
tg.expand();

// Camera data
const cameras = [
    {
        id: 1,
        name: 'Sony Alpha A7 III',
        specs: 'Полнокадровая беззеркальная камера, 24.2 МП',
        description: 'Профессиональная полнокадровая камера с отличным качеством изображения и видео 4K.',
        price: 3500,
        priceUnit: '₽/день',
        image: 'images/sony-a7iii.jpg'
    },
    {
        id: 2,
        name: 'Canon EOS R5',
        specs: 'Полнокадровая беззеркальная камера, 45 МП',
        description: 'Высокопроизводительная камера для профессиональной фото и видеосъемки до 8K.',
        price: 4500,
        priceUnit: '₽/день',
        image: 'images/canon-eos-r5.jpg'
    },
    {
        id: 3,
        name: 'Nikon Z6 II',
        specs: 'Полнокадровая беззеркальная камера, 24.5 МП',
        description: 'Универсальная беззеркальная камера для фотографов и видеографов.',
        price: 3200,
        priceUnit: '₽/день',
        image: 'images/nikon-z6ii.jpg'
    },
    {
        id: 4,
        name: 'Blackmagic Pocket Cinema Camera 6K',
        specs: 'Кинокамера Super 35, 6K разрешение',
        description: 'Профессиональная видеокамера с потрясающим динамическим диапазоном и возможностью записи в RAW.',
        price: 5000,
        priceUnit: '₽/день',
        image: 'images/blackmagic-pocket-6k.jpg'
    },
    {
        id: 5,
        name: 'Fujifilm X-T4',
        specs: 'APS-C беззеркальная камера, 26.1 МП',
        description: 'Камера, сочетающая стильный дизайн и высокую производительность для фото и видео.',
        price: 2800,
        priceUnit: '₽/день',
        image: 'images/fujifilm-xt4.jpg'
    }
];

// DOM Elements
const cameraListEl = document.getElementById('camera-list');
const bookingFormEl = document.getElementById('booking-form');
const selectedCameraEl = document.getElementById('selected-camera');
const bookingForm = document.getElementById('booking');
const backToListBtn = document.getElementById('back-to-list');
const successModal = document.getElementById('success-modal');
const closeModalBtn = document.getElementById('close-modal');

// Selected camera
let selectedCamera = null;

// Render camera list
function renderCameraList() {
    cameraListEl.innerHTML = '';
    
    cameras.forEach(camera => {
        const cameraCard = document.createElement('div');
        cameraCard.className = 'camera-card';
        cameraCard.dataset.id = camera.id;
        
        cameraCard.innerHTML = `
            <img src="${camera.image}" alt="${camera.name}" class="camera-image">
            <div class="camera-name">${camera.name}</div>
            <div class="camera-specs">${camera.specs}</div>
            <div class="camera-description">${camera.description}</div>
            <div class="camera-price">${camera.price} ${camera.priceUnit}</div>
        `;
        
        cameraCard.addEventListener('click', () => selectCamera(camera));
        cameraListEl.appendChild(cameraCard);
    });
}

// Select a camera
function selectCamera(camera) {
    selectedCamera = camera;
    selectedCameraEl.innerHTML = `
        <div class="camera-name">${camera.name}</div>
        <div class="camera-specs">${camera.specs}</div>
        <div class="camera-price">${camera.price} ${camera.priceUnit}</div>
    `;
    
    cameraListEl.style.display = 'none';
    bookingFormEl.style.display = 'block';
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('start-date').min = today;
    document.getElementById('end-date').min = today;
    
    // Handle back button in Telegram
    tg.BackButton.show();
    tg.BackButton.onClick(() => backToList());
}

// Go back to list
function backToList() {
    cameraListEl.style.display = 'block';
    bookingFormEl.style.display = 'none';
    selectedCamera = null;
    tg.BackButton.hide();
}

// Submit booking
function submitBooking(e) {
    e.preventDefault();
    
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const comment = document.getElementById('comment').value;
    
    // Get selected accessories
    const accessoriesSelect = document.getElementById('accessories');
    const selectedAccessories = Array.from(accessoriesSelect.selectedOptions).map(option => option.text);
    
    // Create booking data
    const bookingData = {
        camera: selectedCamera.name,
        cameraId: selectedCamera.id,
        startDate,
        endDate,
        accessories: selectedAccessories,
        name,
        phone,
        comment,
        telegramUser: tg.initDataUnsafe.user ? {
            id: tg.initDataUnsafe.user.id,
            firstName: tg.initDataUnsafe.user.first_name,
            lastName: tg.initDataUnsafe.user.last_name,
            username: tg.initDataUnsafe.user.username
        } : null
    };
    
    // Send data to backend (here we'll just simulate it)
    console.log('Booking data:', bookingData);
    
    // Show success modal
    showSuccessModal();
    
    // Send data to Telegram
    if (tg.initDataUnsafe.user) {
        tg.sendData(JSON.stringify(bookingData));
    }
    
    // Clear form
    bookingForm.reset();
}

// Show success modal
function showSuccessModal() {
    successModal.style.display = 'flex';
}

// Close success modal
function closeModal() {
    successModal.style.display = 'none';
    backToList();
}

// Phone number formatting
function setupPhoneInput() {
    const phoneInput = document.getElementById('phone');
    
    phoneInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        
        if (value.length > 0 && value[0] !== '7') {
            value = '7' + value;
        }
        
        let formattedValue = '';
        
        if (value.length > 0) {
            formattedValue = '+' + value[0];
        }
        
        if (value.length > 1) {
            formattedValue += ' (' + value.substring(1, 4);
        }
        
        if (value.length > 4) {
            formattedValue += ') ' + value.substring(4, 7);
        }
        
        if (value.length > 7) {
            formattedValue += '-' + value.substring(7, 9);
        }
        
        if (value.length > 9) {
            formattedValue += '-' + value.substring(9, 11);
        }
        
        e.target.value = formattedValue;
    });
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    renderCameraList();
    setupPhoneInput();
    
    bookingForm.addEventListener('submit', submitBooking);
    backToListBtn.addEventListener('click', backToList);
    closeModalBtn.addEventListener('click', closeModal);
    
    // Set up date input logic
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    
    startDateInput.addEventListener('change', () => {
        endDateInput.min = startDateInput.value;
        if (endDateInput.value && new Date(endDateInput.value) < new Date(startDateInput.value)) {
            endDateInput.value = startDateInput.value;
        }
    });
    
    // Initialize Telegram WebApp UI
    tg.ready();
    
    // Setup main button
    tg.MainButton.setParams({
        text: 'Открыть приложение',
        color: tg.themeParams.button_color || '#3390ec'
    });
    
    tg.MainButton.onClick(() => {
        tg.MainButton.hide();
    });
    
    tg.MainButton.show();
}); 