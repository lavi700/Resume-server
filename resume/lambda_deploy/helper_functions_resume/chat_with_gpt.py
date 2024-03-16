from timeout_decorator import timeout
import openai
import json
import os

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# OpenAI Configuration
openai.api_key = os.environ['openai']

gpt_instructions = ""

@timeout(5)
def chat_with_gpt(input=''):
    messages = [
        {"role": "system", "content": gpt_instructions},
        {"role": "user", "content": input},
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        max_tokens=50
    )
    return response.choices[0].message['content']  