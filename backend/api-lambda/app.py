import os
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

# ✅ Add CORS middleware to allow access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "mvp_exhibitions")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

# Create DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

@app.get("/exhibitions")
def get_exhibitions():
    # Scan the DynamoDB table
    response = table.scan()
    # read all items from DynamoDb
    items = response["Items"]

    return items

# ✅ Required for API Gateway + Lambda
handler = Mangum(app)
