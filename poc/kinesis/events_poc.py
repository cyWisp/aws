import logging
import json
import boto3

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

def build_event():
    return {'example': 'event'}



if __name__ == '__main__':

    event = build_event()

    kinesis_client = boto3.client(
        'kinesis',
        region_name='us-east-1')

    data = json.dumps(event)

    response = kinesis_client.put_record(
        StreamName='<stream_name>',
        Data=(json.dumps(event) + "\n").encode("utf-8"),
        PartitionKey='<partition_key>'
    )

    log.info(json.dumps(response, indent=4))
