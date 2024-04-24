#!/usr/bin/env python
from edi_835_parser import parse
import pandas as pd

FILE_NAME = 'test_1.edi'

if __name__ == '__main__':
    transaction_set = parse(FILE_NAME)
    data = transaction_set.to_dataframe()

    print('Done')