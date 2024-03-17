from helper_functions_resume.extract_text_from_pdf import extract_text_from_pdf
from helper_functions_resume.chat_with_gpt import chat_with_gpt 

import boto3
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil.tz
from io import BytesIO

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
    texts = []
    for fileUniqueName in fileUniqueNames:
        # Fetch the file object from S3
        file_object = s3_client.get_object(Bucket=bucket_name, Key=fileUniqueName) 
        file_content = file_object['Body'].read()

        file_stream = BytesIO(file_content)
        extracted_text = extract_text_from_pdf(file_stream)
        texts.append(extracted_text)

    return {
        'statusCode': 200,
        'body': json.dumps(texts)
    }
        
    # except Exception as e:
    #     logger.error('An error occurred: %s', e, exc_info=True)
    #     return {'statusCode': 500, 'body': json.dumps('An internal error occurred')}


