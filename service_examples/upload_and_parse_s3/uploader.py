#!/usr/bin/env
import os
import boto3
import logging
import json
import configargparse


parser = configargparse.get_argument_parser(
    name='default',
    description='Default configuration for s3 Bucket Uploader',
    formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter
)

parser.add_argument('--log-level', type=str, required=False,
                    default='INFO', help='The log level with which to run the application.')

parser.add_argument('--upload-file-path', type=str, required=False,
                    default='upload', help='The default directory from which to upload files.')

parser.add_argument('--bucket-name', type=str, required=False,
                    default='rd-claims-store', help='The target AWS bucket to upload files to.')

cfg = parser.parse_known_args()[0]


logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.getLevelName(cfg.log_level)
)

log = logging.getLogger()
files = None


class S3Uploader:
    def __init__(
            self,
            path: str,
            bucket: str
    ):
        self.path = path
        self.bucket = bucket
        self.files, self.s3_client, self.s3_resource = None, None, None

        self.validate_target_file_path()

        if self.files:
            try:
                self.s3_client = boto3.client('s3')
                self.s3_resource = boto3.resource('s3')
            except Exception as e:
                log.error('Unable to retrieve bucket list.')

    def validate_target_file_path(self):
        try:
            log.info('Gathering files for upload.')
            self.files = [f'{os.path.abspath(self.path)}/{x}' \
                     for x in os.listdir(self.path) if x.split('.')[-1] == 'edi']

            log.info(f'Files found: {self.files}')
        except FileNotFoundError as e:
            log.error(f'No files found:\n{e}')

    def list_buckets(self):
        if self.s3_resource:
            log.info('Listing any currently existing s3 buckets.')
            log.info(f'{self.s3_resource.buckets} | {type(self.s3_resource.buckets)}')

            for bucket in self.s3_resource.buckets.all():
                log.info(bucket.name)

    def upload_to_bucket(self):
        log.info(f'Uploading files ({self.files}) to {self.bucket}.')

        if self.s3_client:
            for file in self.files:
                log.info(f'Uploading -\n\t{file} to {self.bucket} with key {file.split("/")[-1]}')

                try:
                    self.s3_client.upload_file(
                        Filename=file,
                        Bucket=self.bucket,
                        Key=f'claims/{file.split("/")[-1]}'
                    )

                    log.info('Success!')
                except Exception as e:
                    log.error(f'Failed to upload {file} -> {e}')


if __name__ == '__main__':
    logging.info('EDI File Uploader Started.')
    logging.info(f'Configuration: {json.dumps(vars(cfg), indent=4)}')

    logging.info(f'Creating s3 Uploader object.')
    new_uploader = S3Uploader(
        cfg.upload_file_path,
        cfg.bucket_name
    )

    new_uploader.list_buckets()
    new_uploader.upload_to_bucket()



