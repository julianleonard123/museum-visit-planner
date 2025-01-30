import aws_cdk as cdk
import settings
from cdkapp.app_stack import AppStack

app = cdk.App()
AppStack(app, "AppStack",
    env=cdk.Environment(account=settings.AWS_ACCOUNT_ID, region=settings.AWS_REGION),
    )

app.synth()
