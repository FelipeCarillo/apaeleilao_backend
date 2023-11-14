from typing import Dict, Tuple, List
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct


class LambdaWebhookStack(Construct):

    def create_lambda(self, function_name: str,
                      environment_variables: Dict[str, str],
                      method: str = None,
                      restapi_resource: apigw.Resource = None,
                      origins: List = apigw.Cors.ALL_ORIGINS,
                      more_layers: List[_lambda.LayerVersion] = None,
                      ) -> _lambda.Function:

        layers = [self.shared_layer, self.jwt_layer, self.bcrypt_layer]
        layers.extend(more_layers) if more_layers else None

        function = _lambda.Function(
            self, (function_name + "_apae_leilao").title(),
            function_name=(function_name + "_apae_leilao").title(),
            environment=environment_variables,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(f"../src/modules/{function_name}"),
            handler=f"app.{function_name}_presenter.lambda_handler",
            layers=layers,
            timeout=Duration.seconds(15),
            memory_size=512,
        )

        restapi_resource.add_resource(function_name.replace("_", "-"),
                                      default_cors_preflight_options=
                                      {
                                          "allow_origins": origins,
                                          "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                          "allow_headers": ["*"]
                                      }
                                      ).add_method(method, integration=apigw.LambdaIntegration(function))

        return function

    def __init__(self, scope: Construct, restapi_resource: apigw.Resource,
                 environment_variables: Dict[str, str]) -> None:
        super().__init__(scope, "ApaeLeilao_Lambdas_Webhook")

        self.bcrypt_layer = _lambda.LayerVersion(
            self, "Bcrypt_Layer",
            code=_lambda.Code.from_asset("./bcrypt_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
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

        self.urllib3 = _lambda.LayerVersion(
            self, "Urllib3_Layer",
            code=_lambda.Code.from_asset("./urllib3_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        )

        self.update_payment = self.create_lambda(
            function_name="update_payment",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
            origins=["https://www.mercadopago.com.ar"],
            more_layers=[self.mercadopago, self.urllib3],
        )

    @property
    def functions_need_user_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )

    @property
    def functions_need_auction_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.update_payment,
        )

    @property
    def functions_need_events_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )

    @property
    def functions_need_lambda_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )
