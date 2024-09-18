# app.py

from flask import Flask, request, jsonify, render_template
import os

# Import the get_response function from chatgpt_module
from modules.chatgpt_module import get_response

app = Flask(__name__)

# Route for serving the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the chat interaction
@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the frontend
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'response': 'No message received!'}), 400

    try:
        response_text = get_response(user_message)
        # Return the response back to the frontend as JSON
        return jsonify({'response': response_text})

    except Exception as e:
        # Return an error message in case something goes wrong
        return jsonify({'response': str(e)}), 500

if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5001)
