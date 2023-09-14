from typing import Dict
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Stack,
    Duration,
)
from constructs import Construct


class LambdaStack(Stack):

    def create_lambda(self, module_name: str, method: str, restapi_resource: apigw.Resource,
                      environment_variables: Dict[str, str]) -> _lambda.Function:
        function = _lambda.Function(
            self, module_name,
            memory_size=512,
            environment=environment_variables,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}.lambda_handler",
            timeout=Duration.seconds(15),
        )

        restapi_resource.add_resource(module_name.replace("_", "-")).add_method(method,
                                                                                apigw.LambdaIntegration(function))

        return function

    def __init__(self, scope: Construct, restapi_resource: apigw.Resource,
                 environment_variables: Dict[str, str]) -> None:
        super().__init__(scope, "ApaeMssLambdas", )

        self.__create_user = self.create_lambda(
            module_name="create_user",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

