from typing import List

from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct


def create_table(self,
                 name: str,
                 partition_key: str,
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
                                  attributes: List = None,
                                  ) -> None:
    table.add_global_secondary_index(
        index_name=index_name,
        partition_key=dynamodb.Attribute(
            name=partition_key,
            type=dynamodb.AttributeType.STRING
        ),
        sort_key=sort_key,
        non_key_attributes=attributes,
        projection_type=dynamodb.ProjectionType.ALL
    )


class DynamoDBStack(Construct):

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "ApaeLeilao_DynamoDB")

        self.__user_table = create_table(self, "UserApaeLeilao", "user_id")
        create_global_secondary_index(self.__user_table, "EmailIndex", "email")
        create_global_secondary_index(self.__user_table, "CpfIndex", "cpf")
        create_global_secondary_index(self.__user_table,
                                      "SuspensionIndex",
                                      "user_id",
                                      "suspension_id",
                                      ["suspension_id", "reason", "date_suspension",
                                       "date_reactivation", "status_suspension"]
                                      )

        self.__auction_table = create_table(self, "AuctionApaeLeilao", "auction_id")

        self.__bid_table = create_table(self, "BidApaeLeilao", "bid_id")
        create_global_secondary_index(self.__bid_table, "AuctionIdIndex", "auction_id")
        create_global_secondary_index(self.__bid_table, "UserIdIndex", "user_id")

        self.__payment_table = create_table(self, "PaymentApaeLeilao", "payment_id")
        create_global_secondary_index(self.__payment_table, "AuctionIdIndex", "auction_id")
        create_global_secondary_index(self.__payment_table, "UserIdIndex", "user_id")

    @property
    def user_table(self) -> dynamodb.Table:
        return self.__user_table

    @property
    def auction_table(self) -> dynamodb.Table:
        return self.__auction_table

    @property
    def bid_table(self) -> dynamodb.Table:
        return self.__bid_table

    @property
    def payment_table(self) -> dynamodb.Table:
        return self.__payment_table
