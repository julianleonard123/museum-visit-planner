import subprocess
from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_secretsmanager as secretsmanager
)
# from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct

import settings

class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self, "exhibitions",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            table_name=settings.DYNAMODB_TABLE,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # copy the lambda source code files into the package folder so it sits next to the installed dependencies when packaged.
        subprocess.run(["mkdir", "lambda_api/package/backend/"])
        subprocess.run(["cp", "lambda_api/app.py", "lambda_api/package/app.py"])
        subprocess.run(["cp", "settings.py", "lambda_api/package/backend/settings.py"])
        subprocess.run(["cp", "model.py", "lambda_api/package/backend/model.py"])
        
        subprocess.run(["mkdir", "lambda_import_exhibitions/package/backend/"])
        subprocess.run(["cp", "lambda_import_exhibitions/lambda_function.py", "lambda_import_exhibitions/package/lambda_function.py"])
        subprocess.run(["cp", "settings.py", "lambda_import_exhibitions/package/backend/settings.py"])
        subprocess.run(["cp", "model.py", "lambda_import_exhibitions/package/backend/model.py"])

        subprocess.run(["mkdir", "lambda_import_weather/package/backend/"])
        subprocess.run(["cp", "lambda_import_weather/lambda_function.py", "lambda_import_weather/package/lambda_function.py"])
        subprocess.run(["cp", "settings.py", "lambda_import_weather/package/backend/settings.py"])
        subprocess.run(["cp", "model.py", "lambda_import_weather/package/backend/model.py"])
        
        # Define the API Lambda function
        fastapi_lambda = lambda_.Function(
            self, "getExhibitionsLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.handler",
            code=lambda_.Code.from_asset("lambda_api/package"),
            memory_size=128,
            timeout=Duration.seconds(5),
            architecture=lambda_.Architecture.ARM_64
        )

        # Define the Import Exhibitions Lambda function
        import_exhibitions_lambda = lambda_.Function(
            self, "importExhibitionsLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("lambda_import_exhibitions/package"),
            memory_size=256,
            timeout=Duration.seconds(60),
            architecture=lambda_.Architecture.ARM_64
        )

        # Define the Import Weather Lambda function
        import_weather_lambda = lambda_.Function(
            self, "importWeatherLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("lambda_import_weather/package"),
            memory_size=256,
            timeout=Duration.seconds(60),
            architecture=lambda_.Architecture.ARM_64
        )

        secret = secretsmanager.Secret.from_secret_name_v2(self, settings.HARVARD_ART_MUSEUMS_API_KEY_SECRET_NAME, settings.HARVARD_ART_MUSEUMS_API_KEY_SECRET_NAME)
        secret.grant_read(import_exhibitions_lambda)
        
        table.grant_write_data(import_exhibitions_lambda)
        table.grant_read_data(import_weather_lambda)
        table.grant_write_data(import_weather_lambda)
        table.grant_read_data(fastapi_lambda)

        # Create an API Gateway to expose the FastAPI Lambda function
        api = apigateway.LambdaRestApi(
            self, "ExhibitionsEndpoint",
            handler=fastapi_lambda,
            proxy=True,
            binary_media_types=["application/json"]
        )

        CfnOutput(self, "API Gateway URL", value=api.url)
