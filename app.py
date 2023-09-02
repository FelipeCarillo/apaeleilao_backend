#!/usr/bin/env python3
import os
import aws_cdk as cdk

from apae_mss_activity.iac.iac.iac_stack import IACStack


app = cdk.App()

IACStack(app, "ApaeMssActivityStack",
         env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()
