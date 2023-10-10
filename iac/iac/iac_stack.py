import os

from aws_cdk import (
    aws_apigateway as apigw,
    Stack,
    aws_s3 as s3,
    RemovalPolicy,
)

from constructs import Construct
from .lambda_stack import LambdaStack
from .dynamodb_stack import DynamoDBStack


class IACStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = os.environ.get("STAGE", "test")
        bucket_name = os.environ.get("BUCKET_NAME", "")
        ses_sender = os.environ.get("SES_SENDER", "")
        ses_region = os.environ.get("SES_REGION", "")
        encrypted_key = os.environ.get("ENCRYPTED_KEY", "")

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "SES_SENDER": ses_sender,
            "SES_REGION": ses_region,
            "ENCRYPTED_KEY": encrypted_key,
        }

        self.__bucket = s3.Bucket(
            self, f"Apae_Leilao_Bucket_{stage}",
            bucket_name=bucket_name,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.__restapi = apigw.RestApi(
            self, f"Apae_Leilao_Restapi",
            rest_api_name=f"Apae_Leilao_RestApi",
            description="This service serves Apae Leilao RestApi",
            default_cors_preflight_options=
            {
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ['*']
            },
            deploy_options=apigw.StageOptions(
                stage_name=stage,
            ),
        )

        restapi_resourse = self.__restapi.root.add_resource("apae-leilao", default_cors_preflight_options=
        {
            "allow_origins": apigw.Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": apigw.Cors.DEFAULT_HEADERS + ['Host', 'Token', 'Content-Type', 'email', 'password']
        })

        self.dynamodb_stack = DynamoDBStack(self)

        self.lambda_function = LambdaStack(self, restapi_resource=restapi_resourse,
                                           environment_variables=ENVIRONMENT_VARIABLES)

        for function in self.lambda_function.functions_need_user_table_permission:
            self.dynamodb_stack.user_table.grant_read_write_data(function)

        for function in self.lambda_function.functions_need_auction_table_permission:
            self.dynamodb_stack.auction_table.grant_read_write_data(function)
