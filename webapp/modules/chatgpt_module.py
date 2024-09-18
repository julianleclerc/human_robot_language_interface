# modules/chatgpt_module.py

import os
from openai import OpenAI


# set up OpenAI API key
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'], 
)

INSTRUCTIONS = """You are a helpful assistant"""

conversation_history = []

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

def get_response(user_message):
    if not user_message:
        return "No message received!"

    try:
        # add instructions
        messages = [
            { "role": "system", "content": INSTRUCTIONS },
        ]

        # add the previous questions and answers
        if conversation_history:
            # Each exchange consists of a user message and an assistant response
            num_messages_to_include = MAX_CONTEXT_QUESTIONS * 2
            recent_history = conversation_history[-num_messages_to_include:]
            messages.extend(recent_history)

        # add the new question
        messages.append({ "role": "user", "content": user_message })

        # get response from chatgpt
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            top_p=1,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )

        # get text response
        response_text = completion.choices[0].message.content.strip()

        # update the conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": response_text})

        # Optionally, limit the conversation history to prevent exceeding token limits
        #conversation_history[:] = conversation_history[-MAX_MESSAGES:]


        return response_text
    
    except Exception as e:
        # Return an error message in case something goes wrong
        return f"Error communicating with ChatGPT API: {str(e)}"