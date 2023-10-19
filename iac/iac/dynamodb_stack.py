from typing import List

from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct


def create_table(self,
                 name: str,
                 partition_key: str
                 ) -> dynamodb.Table:
    table = dynamodb.Table(self,
                           name,
                           table_name=name,
                           partition_key=dynamodb.Attribute(
                               name=partition_key,
                               type=dynamodb.AttributeType.STRING
                           ),
                           billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                           removal_policy=RemovalPolicy.DESTROY
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


class DynamoDBStack(Construct):

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "ApaeLeilao_DynamoDB")

        self.__user_table = create_table(self, "User_Apae_Leilao", "user_id")
        create_global_secondary_index(self.__user_table, "email-index", "email")
        create_global_secondary_index(self.__user_table, "cpf-index", "cpf")
        create_global_secondary_index(self.__user_table, "access_key-index", "access_key")

        self.__auction_table = create_table(self, "Auction_Apae_Leilao", "auction_id")
        create_global_secondary_index(self.__auction_table, "status-auction-index", "status_auction", 'start_date',
                                      dynamodb.AttributeType.NUMBER)

    @property
    def user_table(self) -> dynamodb.Table:
        return self.__user_table

    @property
    def auction_table(self) -> dynamodb.Table:
        return self.__auction_table
