from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Stack,
    Duration,
)
from constructs import Construct
from .lambda_stack import LambdaStack


class IACStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.api = apigw.RestApi(
            self, "Apae_Leilao_RestApi",
            rest_api_name="Apae_Leilao_RestApi",
            description="This service serves Apae Leilao RestApi",
            default_cors_preflight_options=
            {
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["*"],
            }
        )

        restapi_resourse= self.api.root.add_resource("apae-leilao", default_cors_preflight_options=
            {
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["*"],
            })

        self.lambda_function = LambdaStack(self, restapi_resource=restapi_resourse,)

