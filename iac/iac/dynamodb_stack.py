from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct


class DynamoDBStack(Construct):
    def __init__(self,scope:Construct) -> None:
        super().__init__(scope, "ApaeLeilao_DynamoDB")

        self.__user_table = dynamodb.Table(
            self, "UserApaeLeilao",
            table_name="UserApaeLeilao",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="email",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        self.__auction_table = dynamodb.Table(
            self, "AuctionApaeLeilao",
            table_name="AuctionApaeLeilao",
            partition_key=dynamodb.Attribute(
                name="auction_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        CfnOutput(
            self, "UserTable",
            value=self.__user_table.table_name
        )

        CfnOutput(
            self, "AuctionTable",
            value=self.__auction_table.table_name
        )

    @property
    def user_table(self) -> dynamodb.Table:
        return self.__user_table

    @property
    def auction_table(self) -> dynamodb.Table:
        return self.__auction_table
