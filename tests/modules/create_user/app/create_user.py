import os
import json


def create_user(event, context):

    stage = os.environ.get("STAGE")
    body = json.loads(event['body'])
    email = body['email']
    fullname = body['fullname']




def lambda_handler(event, context):
    soma = soma_two_numbers(event, context)
    message = f"O resultado da soma é {soma}"

    return {
        'statusCode': 200,
        'body': json.dumps({"message": message}),
    }
