import os
from typing import Dict, Optional

import json
import boto3
from datetime import datetime


class EventsTrigger:
    def __init__(self):
        self.__events = boto3.client('events')
        self.__lambda = boto3.client('lambda')

    def create_trigger(self, rule_name: str, lambda_function: str, date: int, payload: Optional[Dict] = None):

        try:
            rule_name = rule_name.title()
            lambda_function = lambda_function.title() + '_Apae_Leilao'

            try:
                self.__lambda.remove_permission(
                    FunctionName=lambda_function,
                    StatementId=rule_name
                )
            except:
                pass

            function = self.__lambda.get_function(FunctionName=lambda_function + '_Apae_Leilao')
            function_arn = function['Configuration']['FunctionArn']

            self.__lambda.add_permission(
                Action='lambda:InvokeFunction',
                FunctionName=lambda_function,
                Principal='events.amazonaws.com',
                StatementId=rule_name,
                SourceArn=f"arn:aws:events:{os.environ.get('AWS_REGION')}:"
                          f"{os.environ.get('AWS_ACCOUNT_ID').replace('ID_', '')}:"
                          f"rule/{rule_name}_Apae_Leilao",
            )

            self.__events.put_rule(
                Name=rule_name,
                ScheduleExpression=f'cron({self.__format_date(date)})',
                State='ENABLED',

            )
            self.__events.put_targets(
                Rule=rule_name,
                Targets=[
                    {
                        'Id': '1',
                        'Arn': function_arn,
                        'InputTransformer': {
                            'InputPathsMap': {
                                'body': '$.body'
                            },
                            'InputTemplate': json.dumps(payload) if payload else json.dumps({})
                        },
                    },
                ]
            )
        except Exception as e:
            return e

    def delete_rule(self, rule_name: str, lambda_function: str):
        try:
            self.__lambda.remove_permission(
                FunctionName=lambda_function + '_Apae_Leilao',
                StatementId=f'{rule_name}'
            )

            self.__events.remove_targets(
                Rule=rule_name.title() + '_Apae_Leilao',
                Ids=[
                    '1',
                ]
            )
            self.__events.delete_rule(
                Name=rule_name.title() + '_Apae_Leilao',
            )
        except Exception as e:
            return e

    @staticmethod
    def __format_date(date: int) -> str:
        date = datetime.fromtimestamp(date)

        minutes = date.minute
        hour = date.hour
        day = date.day
        month = date.month
        year = date.year

        date = f'{minutes} {hour} {day} {month} ? {year}'

        return date
