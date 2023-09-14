import os
import json


def get_user(event, context):
    stage = os.environ.get("STAGE")
    body = json.loads(event['body'])
    email = body['email']
    fullname = body['password']
    return {
        'statusCode': 200,
        'body': json.dumps({"message": f"Hello! Your email is {email}"}),
    }

def lambda_handler(event, context):
    return get_user(event, context)

