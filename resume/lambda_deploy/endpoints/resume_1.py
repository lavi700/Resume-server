# from helper_functions_resume.extract_text_from_pdf import extract_text_from_pdf 

import boto3
import logging
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dateutil.tz

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

def handle_resume_event_1(event): 
    # return {'statusCode': 500, 'body': json.dumps('An internal error occurred')} # to test error case
    try:
        s3_client = boto3.client('s3', region_name=region_name)
        body = json.loads(event['body'])
        file_names = body.get('fileNames', [])
        presigned_urls = {}
        for file_name in file_names:
            presigned_url = s3_client.generate_presigned_url('put_object',
                                                                Params={'Bucket': bucket_name,
                                                                        'Key': file_name,
                                                                        'ContentType': 'application/pdf'
                                                                        },
                                                                ExpiresIn=3600)  # URL expires in 1 hour
            presigned_urls[file_name] = presigned_url
            
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust CORS as needed
            },
            'body': json.dumps(presigned_urls)
        }
    
    except Exception as e:
        logger.error('An error occurred: %s', e, exc_info=True)
        return {'statusCode': 500, 'body': json.dumps('An internal error occurred')}


