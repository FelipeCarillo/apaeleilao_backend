#!/usr/bin/env python3
import os
import aws_cdk as cdk
from iac.iac_stack import IACStack
from .adjust_layer_directory import adjust_layer_directory

app = cdk.App()

aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
aws_region = os.environ.get("AWS_REGION")

adjust_layer_directory(shared_dir_name="shared", destination="apaeleilao_layer")

IACStack(app, os.environ.get("STACK_NAME"),
         env=cdk.Environment(account=aws_account_id, region=aws_region))

app.synth()
