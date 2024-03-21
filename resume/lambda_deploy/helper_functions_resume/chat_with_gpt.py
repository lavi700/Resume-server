from timeout_decorator import timeout
import openai
import json
import os

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# OpenAI Configuration
openai.api_key = os.environ['openai']

gpt_instructions = config["GPT_instructions"]

@timeout(10)
def chat_with_gpt(input=''):
    # messages = [
    #     {"role": "system", "content": gpt_instructions},
    #     {"role": "user", "content": input},
    # ]
    messages = [
        {"role": "system", "content": "answer shortly"},
        {"role": "user", "content": "what is the color of the sky?"},
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        max_tokens=50
    )
    return response.choices[0].message['content']  