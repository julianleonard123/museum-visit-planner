import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

import settings

app = FastAPI(root_path="/prod")

# Add CORS middleware to allow access to openapi spec.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
table = dynamodb.Table(settings.DYNAMODB_TABLE)

@app.get("/exhibitions")
def get_exhibitions():
    response = table.scan()
    items = response["Items"]

    return items

# Required for API Gateway + Lambda
handler = Mangum(app)
