from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

def get_response(messages):
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages,
        )
        content = completion.choices[0].message.content.strip()
        return content

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
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )


        response_text = completion.choices[0].message.content.strip()

        # Return the response back to the frontend as JSON
        return jsonify({'response': response_text})

    except Exception as e:
        # Return an error message in case something goes wrong
        return jsonify({'response': f'Error communicating with ChatGPT API: {str(e)}'}), 500

if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5001)
