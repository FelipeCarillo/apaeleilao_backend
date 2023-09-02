import aws_cdk as core
import aws_cdk.assertions as assertions

from apae_mss_activity.iac.iac.iac_stack import ApaeMssActivityStack

# example tests. To run these tests, uncomment this file along with the example
# resource in src/iac_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApaeMssActivityStack(app, "apae-mss-activity")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
