import logging
import boto3
import json

from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)


class STSClient:
    def __init__(self):
        self._client = boto3.client('sts')

    def __str__(self):
        return vars(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def get_caller_identity(self):
        try:
            return self._client.get_caller_identity()

        except ClientError as e:
            log.error(e)


if __name__ == '__main__':
    with STSClient() as sts:
        log.info(json.dumps(sts.get_caller_identity(), indent=4))
