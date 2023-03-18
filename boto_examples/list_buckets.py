#!/usr/bin/env python
import boto3


if __name__ == '__main__':

    # Create a resource object
    s3 = boto3.resource('s3')

    # List bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
