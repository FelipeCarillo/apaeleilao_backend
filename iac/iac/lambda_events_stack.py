from typing import Dict, Tuple
from aws_cdk import (
    aws_lambda as _lambda,
    Duration
)
from constructs import Construct


class LambdaEventsStack(Construct):

    def create_lambda(self, function_name: str,
                      environment_variables: Dict[str, str],
                      ) -> _lambda.Function:
        function = _lambda.Function(
            self, (function_name + "_apae_leilao").title(),
            function_name=(function_name + "_apae_leilao").title(),
            environment=environment_variables,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(f"../src/modules/{function_name}"),
            handler=f"app.{function_name}_presenter.lambda_handler",
            layers=[self.shared_layer, self.jwt_layer, self.bcrypt_layer, self.mercadopago],
            timeout=Duration.seconds(15),
            memory_size=512,
        )

        return function

    def __init__(self, scope: Construct,
                 environment_variables: Dict[str, str]) -> None:
        super().__init__(scope, "ApaeLeilao_Lambdas_Events")

        self.bcrypt_layer = _lambda.LayerVersion(
            self, "Bcrypt_Layer",
            code=_lambda.Code.from_asset("./bcrypt_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        )

        self.jwt_layer = _lambda.LayerVersion(
            self, "Jwt_Layer",
            code=_lambda.Code.from_asset("./jwt_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        )

        self.shared_layer = _lambda.LayerVersion(
            self, "ApaeLeilao_Layer",
            code=_lambda.Code.from_asset("./apaeleilao_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        )

        self.mercadopago = _lambda.LayerVersion(
            self, "MercadoPago_Layer",
            code=_lambda.Code.from_asset("./mercadopago_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        )

        self.start_auction = self.create_lambda(
            function_name="start_auction",
            environment_variables=environment_variables,
        )

        self.end_auction = self.create_lambda(
            function_name="end_auction",
            environment_variables=environment_variables,
        )

    @property
    def functions_need_user_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.start_auction,
            self.end_auction,
        )

    @property
    def functions_need_auction_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.start_auction,
            self.end_auction,
        )