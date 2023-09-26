from typing import Dict
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct


class LambdaStack(Construct):

    def create_lambda(self, function_name: str, method: str, restapi_resource: apigw.Resource,
                      environment_variables: Dict[str, str]) -> _lambda.Function:
        function = _lambda.Function(
            self, (function_name + "_apae_leilao").title(),
            function_name=(function_name + "_apae_leilao").title(),
            environment=environment_variables,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(f"../src/modules/{function_name}"),
            handler=f"app.{function_name}_presenter.lambda_handler",
            layers=[],
            timeout=Duration.seconds(10),
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




