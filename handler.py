import json
from ring_doorbell import Ring
import os
import boto3

username = os.environ["USER"]
password = os.environ["PASS"]

dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-west-1'
)

table = dynamodb.Table('ring-device-events')


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def collect(event, context):
    myring = Ring(username, password)

    push_to_dynamo(myring.doorbells)
    push_to_dynamo(myring.stickup_cams)

    return "Done"

def push_to_dynamo(devices):
    print("Writing event history for " + str(devices))
    for device in devices:
        for event in device.history(limit=25):
            dynamo_event = {
                "device": device.id,
                "device_name": device.name,
                "device_connection_strength": device.wifi_signal_category,
                "device_category": device.family,
                "event_timestamp": event["created_at"].isoformat(),
                "event_type": event["kind"],
                "event_id": event["id"]
            }

            table.put_item(Item=dynamo_event)
