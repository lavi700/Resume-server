from helper_functions_resume.extract_text_from_pdf import extract_text_from_pdf
from helper_functions_resume.chat_with_gpt import chat_with_gpt 
from helper_functions_resume.replace_placeholders import replace_placeholders 

import boto3
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil.tz
from io import BytesIO
import time
from datetime import datetime

israel_tz = dateutil.tz.gettz("Asia/Jerusalem")

# Load the configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# AWS Configuration
region_name = config["aws"]["region_name"]
bucket_name = config["aws"]["bucket_name"]

# # DynamoDB setup
# dynamodb = boto3.resource("dynamodb", region_name=region_name)
# table = dynamodb.Table(table_name)

# # General Settings
# months_to_keep_gpt_data = config["settings"]["months_to_keep_gpt_data"]
# days_to_keep_users_data = config["settings"]["days_to_keep_users_data"]
# max_user_message_length = config["settings"]["max_user_message_length"]
# gpt_use_limit_per_user = config["settings"]["gpt_use_limit_per_user"]
# gpt_global_monthly_limit = config["settings"]["gpt_global_monthly_limit"]

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)  # You can set this to DEBUG, INFO, WARNING, ERROR

def handle_resume_event_2(event): 
    # return {'statusCode': 500, 'body': json.dumps('An internal error occurred')} # to test error case
    # try:
    s3_client = boto3.client('s3', region_name=region_name)
    body = json.loads(event['body'])
    fileUniqueNames = body.get('fileUniqueNames', [])
    role_title = body.get('role_title', [])
    resume_reports = []
    for fileUniqueName in fileUniqueNames:
        # Fetch the file object from S3, using try except in case it didnt finish uploading from client
        for j in range(3):
            try:
                file_object = s3_client.get_object(Bucket=bucket_name, Key=fileUniqueName)
                break
            except Exception as e:
                print(e)
                if j == 2:
                    return {'statusCode': 500, 'body': json.dumps('An internal error occurred')}
                time.sleep(1) 
         
        file_content = file_object['Body'].read()
        file_stream = BytesIO(file_content)
        resume_text = extract_text_from_pdf(file_stream)

        gpt_instructions = config["GPT_instructions"]
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        replacements = {
            "current_date": formatted_date,
            "role_title": role_title
        }
        gpt_instructions = replace_placeholders(gpt_instructions, replacements)
        print(gpt_instructions)

        for j in range(3):
            # try:
            gpt_output = chat_with_gpt(input=resume_text, instructions=gpt_instructions)
            print("gpt_output: ", gpt_output)
            break
            # except Exception as e:
            #     print(e)
            #     if j == 2:
            #         return {'statusCode': 500, 'body': json.dumps('An internal error occurred')}
            #     time.sleep(1)

        dict_report = json.loads(gpt_output)   

        resume_reports.append(dict_report)  

    return {
        'statusCode': 200,
        'body': json.dumps(resume_reports)
    }
        
    # except Exception as e:
    #     logger.error('An error occurred: %s', e, exc_info=True)
    #     return {'statusCode': 500, 'body': json.dumps('An internal error occurred')}


