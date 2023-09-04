from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Stack,
    Duration,
)
from constructs import Construct


class IACStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        random_name_lambda = _lambda.Function(
            self, "soma_two_numbers",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("../src"),
            handler="name.lambda_handler",
        )

        api = apigw.RestApi(
            self, "apaeleilaoimtapi",
        )

        api.root.add_resource("soma").add_method("POST", apigw.LambdaIntegration(random_name_lambda))

