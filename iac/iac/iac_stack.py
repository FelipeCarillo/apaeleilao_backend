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

        random_drink_lambda = _lambda.Function(
            self, "RandomDrinkLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("../src"),
            handler="drink.lambda_handler",
        )

        api = apigw.RestApi(
            self, "RandomDrinkApi",

        )

        api.root.add_resource("drink").add_method("GET", apigw.LambdaIntegration(random_drink_lambda))

