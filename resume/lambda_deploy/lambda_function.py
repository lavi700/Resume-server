from endpoints.cloudwatch import handle_cloudwatch_event
from endpoints.resume_1 import handle_resume_event_1 # the step of presinged urls
from endpoints.resume_2 import handle_resume_event_2 # the step of the output

import json
import traceback

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    print(body)
    print('source: resume')

    try:
        if "source" in event and event["source"] == "aws.events":
            return handle_cloudwatch_event(event)
        elif body.get('fileNames'): 
            return handle_resume_event_1(event)  
        elif body.get('zibi'): 
            return handle_resume_event_2(event)     
        else:
            return {'statusCode': 400, 'body': json.dumps('Invalid action')}

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return {"statusCode": 500, "body": json.dumps("Error")}
    
#  creating a deployment package with dependencies:
# pip install timeout_decorator -t .
# pip install openai==0.28 -t .
# pip install PyPDF2 -t .

# then zip all files in this directory besides urllib stuff (delete them), and upload to aws lambda:

# zip in powershell with command: 
# Get-ChildItem -Path . | Where-Object { $_.Name -notlike 'function.zip' } | Compress-Archive -DestinationPath function.zip -Force

# deploy this zip to aws lambda with command: 
# aws lambda update-function-code --function-name resume_function --zip-file fileb://function.zip    
    