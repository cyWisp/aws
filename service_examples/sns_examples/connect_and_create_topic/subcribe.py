import logging
import boto3
import json

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger()

if __name__ == '__main__':
    """
    Boto3 Example- subcribing to SNS topic
    """

    sns_client = None
    arn = 'arn:aws:sns:us-east-2:266228368403:test-topic-1'

    try:
        log.debug('Creating connection.')
        sns_client = boto3.client('sns')

        response = sns_client.subscribe(
            TopicArn=arn,
            Protocol='email',
            Endpoint='cywisp@gmail.com'
        )

        log.debug(f'response: {json.dumps(response, indent=4)}')

    except Exception as e:
        log.error(e)