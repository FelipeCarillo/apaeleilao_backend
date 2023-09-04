import json


def soma_two_numbers(event, context):
    number1 = event["number1"]
    number2 = event["number2"]
    soma = number1 + number2
    return soma


def lambda_handler(event, context):
    soma = soma_two_numbers(event, context)
    message = f"O resultado da soma é {soma}"

    return {
        'statusCode': 200,
        'body': json.dumps({"message": message}),
    }
