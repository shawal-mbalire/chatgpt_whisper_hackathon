import streamlit as st
import requests
import pywhisper
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Define API endpoint URLs
gpt_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
whisper_url = 'https://whisper-api.herokuapp.com/'

# Define functions for making API calls
def get_gpt_response(prompt):
        headers = {'Content-Type': 'application/json',
                                  'Authorization': 'Bearer YOUR_API_KEY_HERE'}
        data = {'prompt': prompt,
                'max_tokens': 100,
                'n': 1,
                'stop': '###'}
        response = requests.post(gpt_url, headers=headers, json=data)
        return response.json()['choices'][0]['text'].strip()

def encrypt_message(message):
        key = pywhisper.generate_key()
        encrypted_message = pywhisper.encrypt(key, message)
        return key, encrypted_message

def decrypt_message(key, encrypted_message):
        return pywhisper.decrypt(key, encrypted_message)

# Define Streamlit app
def app():
        st.title('Secure Healthcare Chatbot')
        st.header('Enter your message below:')
        message = st.text_input('', key='message_input')

        if st.button('Send'):
                # Get response from GPT API
                gpt_response = get_gpt_response(message)
        # Encrypt message with Whisper API
        key, encrypted_message = encrypt_message(gpt_response)
        # Store encrypted message in Redis
        r.set('message', encrypted_message)
        # Display encrypted message
        st.text('Encrypted message:')
        st.write(encrypted_message)
        # Retrieve encrypted message from Redis
        encrypted_message = r.get('message')
        # Decrypt message with Whisper API
        decrypted_message = decrypt_message(key, encrypted_message)

        # Display decrypted message
        st.text('Decrypted message:')
        st.write(decrypted_message)

if __name__ == '__main__':
        app()

