import os
import subprocess
from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway
)
from constructs import Construct

class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self, "exhibitions",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            table_name="mvp_exhibitions",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )


        # Define the Lambda source code directory
        lambda_dir = "../backend/api/package"

        # Install dependencies in a package directory inside "lambda/"
        # requirements_path = os.path.join(lambda_dir, "requirements.txt")
        # package_dir = os.path.join(lambda_dir, "package")

        # if not os.path.exists(package_dir):
        #     os.mkdir(package_dir)

        # subprocess.run(
        #     f"pip install -r {requirements_path} -t {lambda_dir}", 
        #     shell=True, check=True
        # )

        # Define the Lambda function
        fastapi_lambda = lambda_.Function(
            self, "getExhibitionsLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.handler",
            code=lambda_.Code.from_asset(lambda_dir),
            memory_size=128,
            timeout=Duration.seconds(5),
            architecture=lambda_.Architecture.ARM_64
        )

        # Create an API Gateway to expose the Lambda function
        api = apigateway.LambdaRestApi(
            self, "ExhibitionsEndpoint",
            handler=fastapi_lambda,
            proxy=True,
            binary_media_types=["application/json"]
        )

        CfnOutput(self, "API Gateway URL", value=api.url)
