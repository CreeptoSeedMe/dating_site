// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Лайки
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const profileId = this.dataset.profileId;
            const result = await handleLike(profileId);
            
            if (result.success) {
                this.classList.add('liked');
                this.disabled = true;
            }
        });
    });

    // Основные функции и утилиты
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    // Обработка лайков
    const handleLike = async (profileId) => {
        try {
            const response = await fetch(`/matching/like/${profileId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            
            if (data.match) {
                showMatchNotification(data.matchedProfile);
            }
            
            return data;
        } catch (error) {
            console.error('Error handling like:', error);
        }
    };

    // Уведомления
    const showNotification = (message, type = 'success') => {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    };

    const showMatchNotification = (matchedProfile) => {
        const modal = document.createElement('div');
        modal.className = 'match-modal';
        modal.innerHTML = `
            <div class="match-content">
                <h2>It's a Match! 🎉</h2>
                <p>You and ${matchedProfile.name} liked each other</p>
                <div class="match-actions">
                    <button onclick="startChat(${matchedProfile.id})" class="btn btn-primary">Send Message</button>
                    <button onclick="closeMatchModal()" class="btn btn-secondary">Keep Browsing</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    };

    // Обработка фотографий профиля
    const initializePhotoUpload = () => {
        const photoInput = document.getElementById('photo-upload');
        const previewContainer = document.getElementById('photo-preview');
        
        if (photoInput) {
            photoInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewContainer.innerHTML = `
                            <img src="${e.target.result}" class="photo-preview">
                            <button type="button" class="btn btn-danger" onclick="removePhotoPreview()">Remove</button>
                        `;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
    };

    const removePhotoPreview = () => {
        const photoInput = document.getElementById('photo-upload');
        const previewContainer = document.getElementById('photo-preview');
        
        photoInput.value = '';
        previewContainer.innerHTML = '';
    };

    // Фильтры поиска
    const initializeSearchFilters = () => {
        const filterForm = document.getElementById('search-filters');
        if (filterForm) {
            filterForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const queryString = new URLSearchParams(formData).toString();
                window.location.href = `/matching/browse/?${queryString}`;
            });
        }
    };

    // Геолокация
    const getUserLocation = () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                
                fetch('/profiles/update-location/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ latitude, longitude })
                });
            });
        }
    };

    // Инициализация всех компонентов
    initializePhotoUpload();
    initializeSearchFilters();
    getUserLocation();
    
    // Инициализация всплывающих подсказок Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});