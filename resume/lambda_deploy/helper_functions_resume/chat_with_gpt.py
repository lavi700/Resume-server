from timeout_decorator import timeout
import openai
import json
import os

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# OpenAI Configuration
openai.api_key = os.environ['openai']

# Response Dictionaries 
response_dict_main = config["response_dict_main"]
response_dict_extra = config["response_dict_extra"]

response_dict_combined_hebrew = {**response_dict_main['Hebrew'], **response_dict_extra["Hebrew"]} 
response_dict_combined_english = {**response_dict_main['English'], **response_dict_extra["English"]} 
response_dict_combined = {
    "Hebrew": response_dict_combined_hebrew,
    "English": response_dict_combined_english
}

@timeout(5)
def chat_with_gpt(input):
    gpt_output_options = ""
    for optional_response in response_dict_combined["Hebrew"].keys():
        if optional_response == 'General information':
            continue
        gpt_output_options += optional_response + ' / '
    gpt_output_options = gpt_output_options[:-3]

    # classification:
    instructions = f"Your task is to determine which of the following subjects the user is directly and specifically inquiring about: {gpt_output_options}. In your response include only one of the options above (e.g. 'Pricing'), and if none of them is relevant, output 'None'."
    # tagging:
    # instructions = f"Your task is to determine which of the following subjects the user is directly and specifically inquiring about: {gpt_output_options}. Respond with a list of the relevant subjects (e.g. 'Pricing, Location, ...'), and if none of them is relevant, output 'None'."

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": input},
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        max_tokens=50
    )
    return response.choices[0].message['content']  