from timeout_decorator import timeout
import openai
import json
import os
from datetime import datetime
from helper_functions_resume.replace_placeholders import replace_placeholders 

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# OpenAI Configuration
openai.api_key = os.environ['openai']

gpt_instructions = config["GPT_instructions"]
current_datetime = datetime.now()
formatted_date = current_datetime.strftime('%Y-%m-%d')
replacements = {
    "current_date": formatted_date,
}
gpt_instructions = replace_placeholders(gpt_instructions, replacements)

@timeout(10)
def chat_with_gpt(input=''):
    messages = [
        {"role": "system", "content": gpt_instructions},
        {"role": "user", "content": input},
    ]

    # messages = [
    #     {"role": "system", "content": "output the current date"},
    #     {"role": "user", "content": ""},
    # ]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        max_tokens=50
    )
    return response.choices[0].message['content']  