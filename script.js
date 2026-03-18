const API_URL = 'http://localhost:5000/api';

const chatBox = document.getElementById('chatBox');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const typingIndicator = document.getElementById('typingIndicator');
const topicButtons = document.querySelectorAll('.topic-btn');

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

clearBtn.addEventListener('click', clearChat);

// Topic buttons
topicButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const topic = e.target.getAttribute('data-topic');
        messageInput.value = `Tell me about ${topic}`;
        sendMessage();
    });
});

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to UI
    addMessageToUI(message, 'user');
    messageInput.value = '';

    // Show typing indicator
    typingIndicator.style.display = 'flex';

    try {
        // Send to backend
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error('Failed to get response from server');
        }

        const data = await response.json();
        
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        
        // Add bot response to UI
        addMessageToUI(data.response, 'bot');

    } catch (error) {
        console.error('Error:', error);
        typingIndicator.style.display = 'none';
        addMessageToUI('Sorry, I encountered an error. Please make sure the server is running on localhost:5000', 'bot');
    }

    // Auto-scroll to bottom
    scrollToBottom();
}

function addMessageToUI(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = formatMessage(message);

    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(timeSpan);
    chatBox.appendChild(messageDiv);
}

function formatMessage(text) {
    // Convert newlines to <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Convert **text** to <strong>text</strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *text* to <em>text</em>
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return formatted;
}

function clearChat() {
    if (confirm('Are you sure you want to clear the chat?')) {
        chatBox.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    <p>👋 Hello! I'm your healthcare assistant. I can help you with:</p>
                    <ul>
                        <li>General health information</li>
                        <li>Symptom descriptions</li>
                        <li>Wellness tips</li>
                        <li>When to see a doctor</li>
                    </ul>
                    <p><strong>Note:</strong> I'm not a replacement for professional medical advice. Please consult a doctor for serious concerns.</p>
                </div>
                <span class="message-time">Just now</span>
            </div>
        `;
    }
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Initial scroll to bottom
scrollToBottom();
