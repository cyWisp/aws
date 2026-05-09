import logging
import boto3
import json

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger()

if __name__ == '__main__':
    """
    Boto3 Example- connecting to SNS.
    """

    sns_client = None
    arn = 'arn:aws:sns:us-east-2:266228368403:test-topic-1'

    try:
        log.debug('Creating connection.')
        sns_client = boto3.client('sns')

        subject = 'Test'
        message = 'This is a test message'

        response = sns_client.publish(
            TargetArn=arn,
            Subject=subject,
            Message=message
        )

        log.debug(response)

    except Exception as e:
        log.error(e)