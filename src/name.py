import json
import random


def random_name():
    name = ["Felipe", "Joao", "Maria"]
    return random.choice(name)


def lambda_handler(event, context):
    name = random_drink()
    message = f"Your drink is {name}"

    return {
        'statusCode': 200,
        'body': json.dumps({"message": message}),
    }
