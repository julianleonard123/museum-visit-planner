import json
import requests
import boto3
from botocore.exceptions import ClientError
from backend import settings
from backend.model import Exhibition

dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
table = dynamodb.Table(settings.DYNAMODB_TABLE)

def lambda_handler(event, context):

    exhibitions = get_exhibitions_from_api()
    
    for exhibition in exhibitions:
        put_item(exhibition)

def put_item(exhibition):
    item = json.loads(exhibition.json())
    response = table.put_item(
        Item=item
    )
    return response


def get_exhibitions_from_api():
    response = requests.get(settings.HARVARD_ART_MUSEUMS_API + get_secret())
    if response.status_code != 200:
        return {"error": "Failed to retrieve exhibitions data."}
    
    exhibitions = []

    for exhibition in response.json()["records"]:
        exhibition = Exhibition.model_validate_json(json.dumps(exhibition))
        exhibitions.append(exhibition)
    return exhibitions


def get_secret():

    secret_name = settings.HARVARD_ART_MUSEUMS_API_KEY_SECRET_NAME
    region_name = settings.AWS_REGION

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response["SecretString"])[secret_name]

    return secret
