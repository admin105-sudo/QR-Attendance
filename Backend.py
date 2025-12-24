import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('QR_Attendance')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    student_id = body['student_id']
    today = datetime.now().strftime("%Y-%m-%d")

    response = table.get_item(
        Key={
            'student_id': student_id,
            'date': today
        }
    )

    if 'Item' in response:
        return {
            'statusCode': 200,
            'headers': cors(),
            'body': json.dumps({
                "message": "Attendance already marked"
            })
        }

    table.put_item(
        Item={
            'student_id': student_id,
            'date': today,
            'time': datetime.now().strftime("%H:%M:%S")
        }
    )

    return {
        'statusCode': 200,
        'headers': cors(),
        'body': json.dumps({
            "message": "Attendance marked successfully"
        })
    }

def cors():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
