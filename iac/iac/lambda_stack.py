from typing import Dict, Tuple, List
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration, aws_iam as iam,
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
            layers=[self.shared_layer, self.jwt_layer, self.bcrypt_layer],
            timeout=Duration.seconds(15),
            memory_size=512,
        )

        restapi_resource.add_resource(function_name.replace("_", "-")).add_method(method,
                                                                                  integration=apigw.LambdaIntegration(function))

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

        ses_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "ses:*",
            ],
            resources=["*"],
        )

        self.send_email_code = self.create_lambda(
            function_name="send_verification_email_code",
            method="GET",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

        self.send_email_code.add_to_role_policy(ses_policy)

        self.confirm_verification_email_code = self.create_lambda(
            function_name="confirm_verification_email_code",
            method="POST",
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
            method="PUT",
            restapi_resource=restapi_resource,
            environment_variables=environment_variables,
        )

    @property
    def functions_need_user_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
            self.create_user,
            self.get_user,
            self.send_email_code,
            self.confirm_verification_email_code,
            self.get_token,
            self.update_user,
        )

    @property
    def functions_need_auction_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )

    @property
    def functions_need_payment_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )

    @property
    def functions_need_bid_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )

    @property
    def functions_need_suspension_table_permission(self) -> Tuple[_lambda.Function] or None:
        return (
        )
