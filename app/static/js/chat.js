function addMessage(message, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 
'bot-message'}`;
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const inputElement = document.getElementById('user-input');
    const message = inputElement.value.trim();
    
    if (message) {
        // Add user message to chat
        addMessage(message, true);
        inputElement.value = '';

        try {
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();
            
            // Add bot response to chat
            addMessage(data.response);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your 
request.');
        }
    }
}

// Allow sending message with Enter key
document.getElementById('user-input').addEventListener('keypress', 
function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
