from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Stack,
    Duration,
)
from constructs import Construct

class LambdaStack(Stack):

    def create_lambda(module_name: str, method: str, restapi_resource: apigw.Resource) -> _lambda.Function:
        function = _lambda.Function(
            self, module_name,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("../src/modules"),
            handler=f"app.{module_name}.lambda_handler",
        )

        restapi_resource.add_resource(function_name.replace("_", "-")).add_method(method, apigw.LambdaIntegration(function))

        return function
    def __init__(self, scope: Construct, restapi_resource: apigw.Resource) -> None:
        super().__init__(scope, "ApaeMssLambdas",)

        self.create_user = create_lambda(
            module_name="create_user",
            method="POST",
            restapi_resource=restapi_resource)



