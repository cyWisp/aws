import json
import uuid
import boto3
from aws_xray_sdk.core import patch_all

# Instrument all AWS SDKs (including DynamoDB)
patch_all()

dynamodb = boto3.resource('dynamodb')
table_name = 'BlogComments'  # This will be passed from environment

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    
    try:
        # Parse the request body
        data = json.loads(event['body'])

        # Insert the comment into DynamoDB (this will automatically be traced by X-Ray)
        item = {
            'id': str(uuid.uuid4()),  # Unique ID for each comment
            'comment': data['comment']
        }
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Comment added successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to add comment'})
        }

