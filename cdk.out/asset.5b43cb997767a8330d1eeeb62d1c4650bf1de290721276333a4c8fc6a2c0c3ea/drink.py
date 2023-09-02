import json
import random


def random_drink():
    drinks = ["Coffee", "Tea", "Water"]
    return random.choice(drinks)


def lambda_handler(event, context):
    drink = random_drink()
    message = f"Your drink is {drink}"

    return {
        'statusCode': 200,
        'body': json.dumps({"message": message}),
    }
