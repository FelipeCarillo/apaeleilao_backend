from typing import Dict, Tuple
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration
)
from constructs import Construct


class LambdaStack(Construct):
    USER_TABLE = 'UserApaeLeilao'
    AUCTION_TABLE = 'AuctionApaeLeilao'

    def create_lambda(self, function_name: str, method: str, restapi_resource: apigw.Resource,
                      environment_variables: Dict[str, str]) -> _lambda.Function:

        shared_layer = _lambda.LayerVersion(
            self, "ApaeLeilao_Layer",
            code=_lambda.Code.from_asset("./apaeleilao_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        )

        function = _lambda.Function(
            self, (function_name + "_apae_leilao").title(),
            function_name=(function_name + "_apae_leilao").title(),
            environment=environment_variables,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(f"../src/modules/{function_name}"),
            handler=f"app.{function_name}_presenter.lambda_handler",
            layers=[shared_layer],
            timeout=Duration.seconds(15),
        )

        restapi_resource.add_resource(function_name.replace("_", "-")).add_method(method,
                                                                                  integration=apigw.LambdaIntegration(
                                                                                      function))

        return function

    def __init__(self, scope: Construct, restapi_resource: apigw.Resource,
                 environment_variables: Dict[str, str]) -> None:
        super().__init__(scope, "ApaeLeilao_Lambdas")

        self.create_user = self.create_lambda(
            function_name="create_user",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

    @property
    def functions_need_user_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.create_user,
        )

    @property
    def functions_need_auction_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )
