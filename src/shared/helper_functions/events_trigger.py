import os
from typing import Dict, Optional

import json
import boto3
from datetime import datetime


class EventsTrigger:
    def __init__(self):
        self.__client = boto3.client('events')

    def set_trigger(self, rule_name: str, lambda_function: str, date: int, payload: Optional[Dict] = None):
        self.__client.put_rule(
            Name=rule_name.title() + '_Apae_Leilao',
            ScheduleExpression=f'cron({self.__format_date(date)})',
            State='ENABLED',

        )
        self.__client.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    'Id': '1',
                    'Arn': os.environ.get(lambda_function.upper()),
                    'InputTransformer': {
                        'InputPathsMap': {
                            'body': '$.body',
                        },
                        'InputTemplate': json.dumps(payload) if payload else json.dumps({"body": {}}),
                    },
                },
            ]
        )

    def delete_rule(self, rule_name: str):
        self.__client.remove_targets(
            Rule=rule_name.title() + '_Apae_Leilao',
            Ids=[
                '1',
            ]
        )
        self.__client.delete_rule(
            Name=rule_name
        )

    @staticmethod
    def __format_date(date: int) -> str:
        date = datetime.fromtimestamp(date)

        minutes = date.minute
        hour = date.hour
        day = date.day
        month = date.month
        year = date.year
        day_of_week = date.isoweekday() % 7

        date = f'{minutes} {hour} {day} {month} {day_of_week} {year}'

        return date
