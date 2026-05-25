import logging
import boto3
import os

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

class PollyClient:
    def __init__(self):
        self._client = boto3.client('polly')
        self._audio: dict | None = None

    def __str__(self):
        return vars(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def write_audio_to_file(self, file_path):
        try:
            log.info(f'Writing audio to {file_path}.')

            with open(file_path, 'wb') as f:
                f.write(self._audio['AudioStream'].read())

        except (IOError, KeyError, FileExistsError) as e:
            raise

    def say_something(self, text):
        try:
            log.info(f'Saying: {text}.')

            self._audio = self._client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                Engine='neural',
                VoiceId='Arthur'
            )

            if self._audio:
                self.write_audio_to_file(f'{os.getcwd()}\\output.mp3')

        except ClientError as e:
            log.error(e)


if __name__ == '__main__':
    with PollyClient() as polly:
        polly.say_something(f'Gracie! DO YOU WANT A TREAT?')