// static/js/chat.js
class ChatManager {
    constructor(conversationId) {
        this.conversationId = conversationId;
        this.messageContainer = document.querySelector('.messages-container');
        this.messageForm = document.querySelector('#message-form');
        this.messageInput = document.querySelector('#message-input');
        this.typingTimeout = null;
        this.setupWebSocket();
        this.setupEventListeners();
        this.loadPreviousMessages();
    }

    setupWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.socket = new WebSocket(
            `${wsProtocol}//${window.location.host}/ws/chat/${this.conversationId}/`
        );

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'chat_message') {
                this.addMessage(data.message, data.sender);
            } else if (data.type === 'typing') {
                this.handleTypingIndicator(data.sender, data.is_typing);
            }
        };

        this.socket.onclose = () => {
            console.log('WebSocket closed unexpectedly. Trying to reconnect...');
            setTimeout(() => this.setupWebSocket(), 3000);
        };
    }

    setupEventListeners() {
        this.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        this.messageInput.addEventListener('input', () => {
            if (this.typingTimeout) clearTimeout(this.typingTimeout);
            
            this.socket.send(JSON.stringify({
                'type': 'typing',
                'is_typing': true
            }));

            this.typingTimeout = setTimeout(() => {
                this.socket.send(JSON.stringify({
                    'type': 'typing',
                    'is_typing': false
                }));
            }, 1000);
        });

        // Загрузка изображений
        const imageInput = document.querySelector('#image-upload');
        if (imageInput) {
            imageInput.addEventListener('change', (e) => {
                this.handleImageUpload(e.target.files[0]);
            });
        }
    }

    async loadPreviousMessages() {
        try {
            const response = await fetch(`/chat/${this.conversationId}/messages/`);
            const messages = await response.json();
            
            messages.forEach(msg => {
                this.addMessage(msg.content, msg.sender, msg.timestamp, msg.attachment);
            });
            
            this.scrollToBottom();
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    sendMessage() {
        const content = this.messageInput.value.trim();
        if (!content) return;

        this.socket.send(JSON.stringify({
            'type': 'chat_message',
            'message': content
        }));

        this.messageInput.value = '';
    }

    async handleImageUpload(file) {
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch(`/chat/${this.conversationId}/upload-image/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                this.socket.send(JSON.stringify({
                    'type': 'chat_message',
                    'message': '',
                    'attachment': data.url
                }));
            }
        } catch (error) {
            console.error('Error uploading image:', error);
            showNotification('Error uploading image', 'error');
        }
    }

    addMessage(message, sender, timestamp = null, attachment = null) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(sender === currentUser ? 'message-sent' : 'message-received');

        let messageContent = '';
        
        if (attachment) {
            if (attachment.match(/\.(jpg|jpeg|png|gif)$/i)) {
                messageContent += `<img src="${attachment}" class="message-image" onclick="openImagePreview('${attachment}')">`;
            } else {
                messageContent += `<a href="${attachment}" class="message-attachment" target="_blank">Attachment</a>`;
            }
        }

        if (message) {
            messageContent += `<p>${message}</p>`;
        }

        messageElement.innerHTML = `
            <div class="message-content">
                <span class="message-sender">${sender}</span>
                ${messageContent}
                <span class="message-time">${timestamp || new Date().toLocaleTimeString()}</span>
            </div>
        `;

        this.messageContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    handleTypingIndicator(sender, isTyping) {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (isTyping) {
            if (!typingIndicator) {
                const indicator = document.createElement('div');
                indicator.className = 'typing-indicator';
                indicator.textContent = `${sender} is typing...`;
                this.messageContainer.appendChild(indicator);
                this.scrollToBottom();
            }
        } else {
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }
    }

    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}

// Функция для предпросмотра изображений
function openImagePreview(url) {
    const modal = document.createElement('div');
    modal.className = 'image-preview-modal';
    modal.innerHTML = `
        <div class="image-preview-content">
            <span class="close-preview">&times;</span>
            <img src="${url}" alt="Preview">
        </div>
    `;
    
    document.body.appendChild(modal);
    
    modal.querySelector('.close-preview').onclick = function() {
        modal.remove();
    };
    
    modal.onclick = function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    };
}

// Инициализация чата на странице
if (document.querySelector('.chat-container')) {
    const conversationId = document.querySelector('.chat-container').dataset.conversationId;
    new ChatManager(conversationId);
}