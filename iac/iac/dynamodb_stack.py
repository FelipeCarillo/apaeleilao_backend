import os

from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    CfnOutput
)
import boto3
from constructs import Construct


def create_table(self,
                 name: str,
                 partition_key: str,
                 sort_key: str = None,
                 sort_key_type: dynamodb.AttributeType = None
                 ) -> dynamodb.Table:
    table = dynamodb.Table(self,
                           name,
                           table_name=name,
                           partition_key=dynamodb.Attribute(
                               name=partition_key,
                               type=dynamodb.AttributeType.STRING
                           ),
                           sort_key=dynamodb.Attribute(
                               name=sort_key,
                               type=dynamodb.AttributeType.STRING if not sort_key_type else sort_key_type
                           ) if sort_key else None,
                           billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                           removal_policy=RemovalPolicy.DESTROY,
                           )

    CfnOutput(self, f"{name}_Table",
              value=table.table_name
              )

    return table


def create_global_secondary_index(table: dynamodb.Table,
                                  index_name: str,
                                  partition_key: str,
                                  sort_key: str = None,
                                  sort_key_type: dynamodb.AttributeType = None
                                  ) -> None:
    table.add_global_secondary_index(
        index_name=index_name,
        partition_key=dynamodb.Attribute(
            name=partition_key,
            type=dynamodb.AttributeType.STRING
        ),
        sort_key=dynamodb.Attribute(
            name=sort_key,
            type=dynamodb.AttributeType.STRING if not sort_key_type else sort_key_type
        ) if sort_key else None
    )


def add_admin_user() -> None:
    client = boto3.resource('dynamodb').Table("User_Apae_Leilao")
    if not client.get_item(Key={"PK": os.environ.get("ADMIN_ID"), "SK": "USER"}).get("Item"):
        admin_user = {
            "PK": os.environ.get("ADMIN_ID"),
            "SK": "USER",
            "password": os.environ.get("ADMIN_PASSWORD"),
            "access_key": os.environ.get("ADMIN_ACCESS_KEY"),
            "type_account": "ADMIN",
            "status_account": "ACTIVE",
        }
        client.put_item(
            Item=admin_user
        )


class DynamoDBStack(Construct):

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "ApaeLeilao_DynamoDB")

        self.__user_table = create_table(self, "User_Apae_Leilao", "PK", "SK",
                                         dynamodb.AttributeType.STRING)
        create_global_secondary_index(self.__user_table, "SK_created_at-index", "SK",
                                        "created_at", dynamodb.AttributeType.NUMBER)
        create_global_secondary_index(self.__user_table, "SK_type_account-index", "SK",
                                      "type_account", dynamodb.AttributeType.STRING)
        create_global_secondary_index(self.__user_table, "email-index", "email")
        create_global_secondary_index(self.__user_table, "cpf-index", "cpf")
        create_global_secondary_index(self.__user_table, "access_key-index", "access_key")

        self.__auction_table = create_table(self, "Auction_Apae_Leilao", "PK", "SK",
                                            dynamodb.AttributeType.STRING)
        create_global_secondary_index(self.__auction_table, "SK_PK-index", "SK", "PK",
                                      dynamodb.AttributeType.STRING)
        create_global_secondary_index(self.__auction_table, "SK_start_date-index", "SK",
                                      "start_date", dynamodb.AttributeType.NUMBER)
        create_global_secondary_index(self.__auction_table, "SK_created_at-index", "SK",
                                      "created_at", dynamodb.AttributeType.NUMBER)
        create_global_secondary_index(self.__auction_table, "SK-index", "SK")
        create_global_secondary_index(self.__auction_table, "user_id-index", "user_id")
        add_admin_user()

    @property
    def user_table(self) -> dynamodb.Table:
        return self.__user_table

    @property
    def auction_table(self) -> dynamodb.Table:
        return self.__auction_table
