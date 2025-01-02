class MatchingManager {
    constructor() {
        this.currentIndex = 0;
        this.profiles = [];
        this.initializeSwiper();
        this.loadProfiles();
    }

    async loadProfiles() {
        try {
            const response = await fetch('/matching/get-profiles/');
            this.profiles = await response.json();
            this.renderProfile();
        } catch (error) {
            console.error('Error loading profiles:', error);
        }
    }

    initializeSwiper() {
        this.container = document.querySelector('.profile-cards');
        this.bindEvents();
    }

    bindEvents() {
        document.querySelector('.like-button').addEventListener('click', () => this.handleLike());
        document.querySelector('.dislike-button').addEventListener('click', () => this.handleDislike());
    }

    async handleLike() {
        const currentProfile = this.profiles[this.currentIndex];
        try {
            const result = await handleLike(currentProfile.id);
            if (result.match) {
                showMatchNotification(currentProfile);
            }
        } finally {
            this.nextProfile();
        }
    }

    handleDislike() {
        this.nextProfile();
    }

    nextProfile() {
        this.currentIndex++;
        if (this.currentIndex >= this.profiles.length) {
            this.loadProfiles();
        } else {
            this.renderProfile();
        }
    }

    renderProfile() {
        if (!this.profiles.length) return;
        
        const profile = this.profiles[this.currentIndex];
        this.container.innerHTML = `
            <div class="profile-card">
                <div class="profile-photos">
                    <img src="${profile.primary_photo}" alt="${profile.name}">
                </div>
                <div class="profile-info">
                    <h3>${profile.name}, ${profile.age}</h3>
                    <p>${profile.location}</p>
                    <p class="bio">${profile.bio}</p>
                    <div class="interests">
                        ${profile.interests.map(interest => 
                            `<span class="badge bg-primary">${interest}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    }
}

// Инициализация на странице матчинга
if (document.querySelector('.matching-container')) {
    new MatchingManager();
}