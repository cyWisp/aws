import boto3
import logging
import json
import time

from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)



class KinesisOps:
    def __init__(
        self,
        region: str,
        stream_name: str | None = None,
        refresh_interval_seconds: int = 5,
        target_shard: int = 0,
    ):
        self._client = boto3.client('kinesis', region_name=region)
        self._stream_name: str | None = stream_name
        self._target_shard: int = target_shard
        self.refresh_interval_seconds = refresh_interval_seconds

        self._stream_info: list | None = None
        self._shards: list | None = None
        self._shard_iterator = None

        # Initialize shard iterator
        self._init()

        if not self._stream_info or not self._shards:
            raise Exception('Stream info not available')


    def __str__(self):
        return vars(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def run_stream_operations(self):
        pass

    def _init(self):
        self._get_stream_info()
        self._get_shards()
        self._get_shard_iterator()

    def _get_shards(self):
        if self._stream_info:
            try:
                log.info(f'Retrieving shards for stream {self._stream_name}')

                self._shards = [
                    shard for shard in
                    self._stream_info['StreamDescription']['Shards']
                ]

                log.info(f'SHARDS: {json.dumps(self._shards, indent=4)}')

            except KeyError:
                log.info(f'No shards found for stream {self._stream_name}')

    def _get_stream_info(self):
        if self._stream_name:
            try:
                log.info('Retriving stream info.')

                self._stream_info = self._client.describe_stream(
                    StreamName=self._stream_name
                )

            except ClientError as e:
                log.error(f'Unable to get stream info:\n{e}')

    def _get_shard_iterator(self):
        if self._shards:
            try:
                log.info(f'Retrieving shard iterator for target shard {self._target_shard}')
                log.info(f'Target shard ID: {self._shards[self._target_shard]['ShardId']}')

                self._shard_iterator = self._client.get_shard_iterator(
                    StreamName=self._stream_name,
                    ShardId=self._shards[self._target_shard]['ShardId'],
                    ShardIteratorType='LATEST'
                )['ShardIterator']

            except ClientError as e:
                log.error(f'Unable to get shard iterator:\n{e}')

    def stream_events(self):

        log.info(f'Retrieving events for stream {self._stream_name} | '
                 f'Shard: {self._shards[self._target_shard]['ShardId']}')

        while True:
            try:
                log.info('Querying for events')

                events = self._client.get_records(
                    ShardIterator=self._shard_iterator,
                    Limit=100
                )

                for record in events['Records']:
                    data = record['Data'].decode('utf-8')

                    if data:
                        log.info(f'Received event:\n{data}')
                        log.info(f'TYPE: {type(data)}')

                        data_object = json.loads(data)
                        log.info(f'EVENT TYPE: {data_object["event_type"]}')

                self._shard_iterator = events['NextShardIterator']

                log.info(f'Refresh interval: {self.refresh_interval_seconds}')
                time.sleep(self.refresh_interval_seconds)

            except ClientError as e:
                log.error(f'Unable to read shared:\n{e}')


if __name__ == '__main__':
    with KinesisOps(
        region='us-east-1',
        stream_name='<steam_name>',
        target_shard=0
    ) as kops:
        log.info(kops.__str__())
        kops.stream_events()


