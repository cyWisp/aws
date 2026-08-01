from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_s3_notifications as s3_notifications,
)
from constructs import Construct

class S3LambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket for input
        input_bucket = s3.Bucket(self, "InputBucket")

        # Create a separate S3 bucket for output
        output_bucket = s3.Bucket(self, "OutputBucket")

        # Create a Lambda function
        my_function = _lambda.Function(
            self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_inline(
                """
import json
import boto3

s3_client = boto3.client('s3')

def handler(event, context):
    print("Event:", json.dumps(event))
    input_bucket_name = event['Records'][0]['s3']['bucket']['name']
    input_key = event['Records'][0]['s3']['object']['key']
    output_bucket_name = "OUTPUT_BUCKET_NAME"  # Placeholder for the output bucket name
    output_key = f"processed-{input_key}"
    s3_client.put_object(Bucket=output_bucket_name, Key=output_key, Body="File processed by Lambda!")
    return {"statusCode": 200, "body": "File processed!"}
                """
            ),
        )

        # Grant read access to the input bucket and write access to the output bucket
        input_bucket.grant_read(my_function)
        output_bucket.grant_write(my_function)

        # Add a notification to trigger the Lambda function on object creation in the input bucket
        input_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(my_function),
        )

        # Set the output bucket name in the Lambda environment
        my_function.add_environment("OUTPUT_BUCKET_NAME", output_bucket.bucket_name)


