import aws_cdk as core
import aws_cdk.assertions as assertions

from cdkapp.app_stack import AppStack

def test_stack_created():
    app = core.App()
    stack = AppStack(app, "app")
    template = assertions.Template.from_stack(stack)
