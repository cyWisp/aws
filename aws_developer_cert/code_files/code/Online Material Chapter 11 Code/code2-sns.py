import boto3

# Create SNS client.
sns_client = boto3.client('sns')

# Send message to your mobile number.
# (Replace dummy mobile number with your number.)
sns_client.publish(
  PhoneNumber='1-222-333-3333',
  Message='Hello from your app')

