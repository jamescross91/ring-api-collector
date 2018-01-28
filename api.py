import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-west-1'
)

table = dynamodb.Table('ring-device-events')

def latest(event, context):
    doorbell = get_latest_for_device('e04f434c8496')
    garden_left = get_latest_for_device('44ead8f4ed5b')
    garden_right = get_latest_for_device('64cfd90743fc')

    payload = {
        "doorbell": {
            "device_name": doorbell["device_name"],
            "event_time": doorbell["event_timestamp"],
            "event_type": doorbell["event_type"],
            "connection_status": doorbell["device_connection_strength"]
        },
        "garden_left": {
            "device_name": garden_left["device_name"],
            "event_time": garden_left["event_timestamp"],
            "event_type": garden_left["event_type"],
            "connection_status": garden_left["device_connection_strength"]
        },
        "garden_right": {
            "device_name": garden_right["device_name"],
            "event_time": garden_right["event_timestamp"],
            "event_type": garden_right["event_type"],
            "connection_status": garden_right["device_connection_strength"]
        }
    }

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(payload)
    }

    return response

def get_latest_for_device(device_id):
    response = table.query(
        KeyConditionExpression=Key('device').eq(device_id),
        ScanIndexForward=False,
        Limit=1
    )

    return response["Items"][0]

