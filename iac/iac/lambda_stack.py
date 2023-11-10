from typing import Dict, Tuple
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct


class LambdaStack(Construct):

    def create_lambda(self, function_name: str,
                      environment_variables: Dict[str, str],
                      method: str = None,
                      restapi_resource: apigw.Resource = None,
                      ) -> _lambda.Function:
        function = _lambda.Function(
            self, (function_name + "_apae_leilao").title(),
            function_name=(function_name + "_apae_leilao").title(),
            environment=environment_variables,
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(f"../src/modules/{function_name}"),
            handler=f"app.{function_name}_presenter.lambda_handler",
            layers=[self.shared_layer, self.jwt_layer, self.bcrypt_layer],
            timeout=Duration.seconds(15),
            memory_size=512,
        )

        restapi_resource.add_resource(function_name.replace("_", "-"),
                                      default_cors_preflight_options=
                                      {
                                          "allow_origins": apigw.Cors.ALL_ORIGINS,
                                          "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                          "allow_headers": ["*"]
                                      }
                                      ).add_method(method, integration=apigw.LambdaIntegration(function))

        return function

    def __init__(self, scope: Construct, restapi_resource: apigw.Resource,
                 environment_variables: Dict[str, str]) -> None:
        super().__init__(scope, "ApaeLeilao_Lambdas")

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

        self.create_user = self.create_lambda(
            function_name="create_user",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.get_user = self.create_lambda(
            function_name="get_user",
            method="GET",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.send_verification_email_code = self.create_lambda(
            function_name="send_verification_email_code",
            method="GET",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.confirm_verification_email_code = self.create_lambda(
            function_name="confirm_verification_email_code",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.send_reset_password_link = self.create_lambda(
            function_name="send_reset_password_link",
            method="GET",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.get_token = self.create_lambda(
            function_name="get_token",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.update_user = self.create_lambda(
            function_name="update_user",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.create_auction = self.create_lambda(
            function_name="create_auction",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.create_user_by_admin = self.create_lambda(
            function_name="create_user_by_admin",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.get_auction = self.create_lambda(
            function_name="get_auction",
            method="GET",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.create_bid = self.create_lambda(
            function_name="create_bid",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.get_all_auctions_menu = self.create_lambda(
            function_name="get_all_auctions_menu",
            method="GET",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.create_feedback = self.create_lambda(
            function_name="create_feedback",
            method="POST",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

    @property
    def functions_need_user_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.create_user,
            self.get_user,
            self.send_verification_email_code,
            self.confirm_verification_email_code,
            self.send_reset_password_link,
            self.get_token,
            self.update_user,
            self.create_auction,
            self.create_user_by_admin,
            self.get_auction,
            self.create_bid,
            self.get_all_auctions_menu,
            self.create_feedback
        )

    @property
    def functions_need_auction_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.create_auction,
            self.get_auction,
            self.create_bid,
            self.get_all_auctions_menu,
        )

    @property
    def functions_need_events_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.create_auction,
        )

    @property
    def functions_need_lambda_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.create_auction,
        )
