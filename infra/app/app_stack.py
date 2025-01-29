import os
import subprocess
from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
# from aws_cdk.aws_lambda_python_alpha import PythonFunction
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

        # copy the lambda source code files into the package folder so it sits next to the installed dependencies when packaged.
        subprocess.run(["cp", "../backend/api-lambda/app.py", "../backend/api-lambda/package/app.py"])
        subprocess.run(["cp", "../backend/import-lambda/lambda.py", "../backend/import-lambda/package/lambda.py"])

        # Define the API Lambda function
        fastapi_lambda = lambda_.Function(
            self, "getExhibitionsLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.handler",
            code=lambda_.Code.from_asset("../backend/api-lambda/package"),
            memory_size=128,
            timeout=Duration.seconds(5),
            architecture=lambda_.Architecture.ARM_64
        )

        # Define the Exhibition Import Lambda function
        import_lambda = lambda_.Function(
            self, "importExhibitionsLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda.lambda_handler",
            code=lambda_.Code.from_asset("../backend/import-lambda/package"),
            memory_size=256,
            timeout=Duration.seconds(60),
            architecture=lambda_.Architecture.ARM_64
        )

        table.grant_write_data(import_lambda)
        table.grant_read_data(fastapi_lambda)

        # Create an API Gateway to expose the Lambda function
        api = apigateway.LambdaRestApi(
            self, "ExhibitionsEndpoint",
            handler=fastapi_lambda,
            proxy=True,
            binary_media_types=["application/json"]
        )

        CfnOutput(self, "API Gateway URL", value=api.url)
