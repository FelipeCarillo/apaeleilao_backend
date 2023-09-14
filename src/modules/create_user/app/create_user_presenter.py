import os
import json


def lambda_handler(event, context):
    stage = os.environ.get("STAGE")
    request = json.loads(event['body'])






