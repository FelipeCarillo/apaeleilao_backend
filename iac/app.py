#!/usr/bin/env python3
import os
from aws_cdk import App, Environment

from iac.iac_stack import IACStack
from adjust_layer_directory import adjust_layer_directory

app = App()

aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
aws_region = os.environ.get("AWS_REGION")

adjust_layer_directory(shared_dir_name="shared", destination="apaeleilao_layer")

IACStack(app, os.environ.get("STACK_NAME"),
         env=Environment(account=aws_account_id, region=aws_region))

app.synth()
