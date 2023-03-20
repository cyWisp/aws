#!/usr/bin/env python
import os
import logging
from edi_835_parser import parse

logging.basicConfig(
    format='%(asctime)s: %(message)s',
    level=logging.INFO
)
log = logging.getLogger()

FILE_PATH = 'upload'


def get_files(file_path: str) -> list:
    try:
        log.info('Gathering files for upload.')
        files = [f'{os.path.abspath(FILE_PATH)}/{x}' \
                      for x in os.listdir(FILE_PATH) if x.split('.')[-1] == 'edi']

        log.info(f'Files found: {files}')
        return files
    except FileNotFoundError as e:
        log.error(f'No files found:\n{e}')

def read_files(file_list: list) -> list:
    content = list()

    for file in file_list:
        try:
            transaction_set = parse(file)



if __name__ == '__main__':
    log.info(get_files(FILE_PATH))

