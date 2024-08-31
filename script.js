function addMessage(content, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user' : 'ai');
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendQuery() {
    const queryInput = document.getElementById('query');
    const query = queryInput.value;
    
    if (!query) {
        return;
    }

    addMessage(query, true);
    queryInput.value = '';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: query }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        addMessage(data.response, false);
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error processing your request.', false);
    }
}

document.getElementById('query').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendQuery();
    }
});