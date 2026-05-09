#!/usr/bin/env python
import os
import logging
import pandas as pd
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
    log.info(f'Parsing all EDI files in {FILE_PATH}')
    content = list()

    for file in file_list:
        try:
            content.append(parse(file).to_dataframe())
        except Exception as e:
            log.error(f'Unable to parse {file}:\n{e}')

    return content


if __name__ == '__main__':
    files = get_files(FILE_PATH)
    log.info(files)

    file_content = read_files(files)
    log.info(f'Files read: {len(file_content)}')

    log.info(file_content)
    log.info('Done.')