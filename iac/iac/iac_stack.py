import os
from aws_cdk import (
    aws_apigateway as apigw,
    Stack, aws_iam as iam
)
from constructs import Construct

from .lambda_stack import LambdaStack
from .dynamodb_stack import DynamoDBStack
from .lambda_events_stack import LambdaEventsStack
from .lambda_webhook_stack import LambdaWebhookStack


def add_lambda_policies(lambda_stack):
    for lambda_function in lambda_stack.functions_need_events_permission:
        lambda_function.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["events:*"],
                resources=["*"]
            )
        )

    for lambda_function in lambda_stack.functions_need_lambda_permission:
        lambda_function.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["lambda:*"],
                resources=["*"]
            )
        )


class IACStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = os.environ.get("STAGE", "test")
        mercado_pago_token = os.environ.get("MERCADO_PAGO_ACCESS_TOKEN", "")
        bucket_name = os.environ.get("BUCKET_NAME", "")
        encrypted_key = os.environ.get("ENCRYPTED_KEY", "")
        jwt_algorithm = os.environ.get("JWT_ALGORITHM", "")
        email_sender = os.environ.get("EMAIL_SENDER", "")
        email_password = os.environ.get("EMAIL_PASSWORD", "")
        email_host = os.environ.get("EMAIL_HOST", "")
        email_port = os.environ.get("EMAIL_PORT", "")
        domain = os.environ.get("DOMAIN", "")
        dev_domain = os.environ.get("DEV_DOMAIN", "")
        AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID", "")

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "BUCKET_NAME": bucket_name,
            "ENCRYPTED_KEY": encrypted_key,
            "JWT_ALGORITHM": jwt_algorithm,
            "EMAIL_SENDER": email_sender,
            "EMAIL_PASSWORD": email_password,
            "EMAIL_HOST": email_host,
            "EMAIL_PORT": email_port,
            "DOMAIN": domain if stage == "prod" else dev_domain,
            "AWS_ACCOUNT_ID": AWS_ACCOUNT_ID,
            "MERCADO_PAGO_ACCESS_TOKEN": mercado_pago_token,
        }

        self.__restapi = apigw.RestApi(
            self, f"Apae_Leilao_Restapi",
            rest_api_name=f"Apae_Leilao_RestApi",
            description="This service serves Apae Leilao RestApi",
            default_cors_preflight_options=
            {
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["*"]
            },
            deploy_options=apigw.StageOptions(
                stage_name='prod',
            ),
        )

        restapi_resourse = self.__restapi.root.add_resource("apae-leilao", default_cors_preflight_options=
        {
            "allow_origins": apigw.Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["*"]
        })

        self.dynamodb_stack = DynamoDBStack(self)

        ENVIRONMENT_VARIABLES["USER_TABLE"] = self.dynamodb_stack.user_table.table_name
        ENVIRONMENT_VARIABLES["AUCTION_TABLE"] = self.dynamodb_stack.auction_table.table_name

        self.lambda_events_function = LambdaEventsStack(self, environment_variables=ENVIRONMENT_VARIABLES)
        self.add_lambda_database_permissions(self.lambda_events_function)
        add_lambda_policies(self.lambda_events_function)

        self.lambda_function = LambdaStack(self, restapi_resource=restapi_resourse,
                                           environment_variables=ENVIRONMENT_VARIABLES)
        self.add_lambda_database_permissions(self.lambda_function)
        add_lambda_policies(self.lambda_function)

        restapi_resourse_webhook = self.__restapi.root.add_resource("apae-leilao-webhook",
                                                                    default_cors_preflight_options=
                                                                    {
                                                                        "allow_origins": [
                                                                            "https://www.mercadopago.com.ar"],
                                                                        "allow_methods": ["GET", "POST", "PUT",
                                                                                          "DELETE", "OPTIONS"],
                                                                        "allow_headers": ["*"]
                                                                    })
        self.lambda_webhook = LambdaWebhookStack(self, restapi_resource=restapi_resourse_webhook,
                                                 environment_variables=ENVIRONMENT_VARIABLES)
        self.add_lambda_database_permissions(self.lambda_webhook)
        add_lambda_policies(self.lambda_webhook)

    def add_lambda_database_permissions(self, lambda_stack):
        for lambda_function in lambda_stack.functions_need_user_table_permission:
            self.dynamodb_stack.user_table.grant_read_write_data(lambda_function)

        for lambda_function in lambda_stack.functions_need_auction_table_permission:
            self.dynamodb_stack.auction_table.grant_read_write_data(lambda_function)
