import os

from aws_cdk import (
    aws_apigateway as apigw,
    Stack,
)
from constructs import Construct
from .lambda_stack import LambdaStack


class IACStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage = os.environ.get("STAGE", "TEST").upper()
        ses_sender = os.environ.get("SES_SENDER", None)
        ses_region = os.environ.get("SES_REGION", None)

        self.__restapi = apigw.RestApi(
            self, f"Apae_Leilao_Restapi_{stage}",
            rest_api_name=f"Apae_Leilao_RestApi_{stage}",
            description="This service serves Apae Leilao RestApi",
            default_cors_preflight_options=
            {
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["*"],
            },
        )

        restapi_resourse = self.__restapi.root.add_resource("apae-leilao", default_cors_preflight_options=
        {
            "allow_origins": apigw.Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["*"],
        }
                                                            )

        ENVIROMENT_VARIABLES = {
            "STAGE": stage,
            "SES_SENDER": ses_sender,
            "SES_REGION": ses_region,
        }

        self.lambda_function = LambdaStack(self, restapi_resource=restapi_resourse,
                                           environment_variables=ENVIROMENT_VARIABLES)
