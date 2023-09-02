from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Stack,
    Duration,
)


class LambdaStack(Stack):

    def create_lambda(self, ):
        return _lambda.Function(
            self, "RandomDrinkLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("../src"),
            handler="drink.lambda_handler",
        )

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

