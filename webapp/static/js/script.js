// Function to change the image in the Robot Display section
function changeImage(imageSrc) {
    document.getElementById('robot-image').src = imageSrc;
}

// Select all buttons with the data-image attribute for image switching
const buttons = document.querySelectorAll('button[data-image]');
const robotImage = document.getElementById('robot-image');

// Attach event listeners to each button for image switching
buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Get the image path from the data-image attribute of the clicked button
        const imageSrc = button.getAttribute('data-image');
        
        // Log the image source for debugging purposes
        console.log("Switching to image:", imageSrc);

        // Change the robot image source to the selected one
        robotImage.src = imageSrc;
    });
});

// Chat functionality: Handle sending messages to the backend
document.getElementById('send-btn').addEventListener('click', function() {
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
    
    // Check if input is not empty
    if (chatInput.value.trim()) {
        const userMessage = chatInput.value;

        // Append user message to chat box
        const userMessageElement = document.createElement('p');
        userMessageElement.textContent = "You: " + userMessage;
        chatBox.appendChild(userMessageElement);

        // Clear the input field
        chatInput.value = '';

        // Send the user's message to the backend (Flask server)
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Append ChatGPT's response to the chat box
            const botMessageElement = document.createElement('p');
            botMessageElement.textContent = "Robotont: " + data.response;
            chatBox.appendChild(botMessageElement);

            // Scroll to the bottom of the chat box to show the latest messages
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            // Log any errors to the console for debugging
            console.error('Error:', error);
        });
    }
});
