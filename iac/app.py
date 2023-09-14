#!/usr/bin/env python3
import os
import aws_cdk as cdk

from iac.mss_auction.iac_stack import IACStack


app = cdk.App()

aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
aws_region = os.environ.get("AWS_REGION")

IACStack(app, "ApaeMssAuctionStack",
                env=cdk.Environment(account=aws_account_id, region=aws_region),)

app.synth()
