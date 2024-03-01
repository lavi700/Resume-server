import json

def handle_cloudwatch_event(event): 
    return {"statusCode": 200, "body": json.dumps("Success")}