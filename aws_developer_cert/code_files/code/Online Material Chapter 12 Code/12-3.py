import boto3
# Variables for the bucket name and the region we will be using.
# Important Note: Be sure to use the same bucket names you used I the previous two exercises
bucketInputName = "shoe-company-ingestion-csv-demo"
bucketOutputName = "shoe-company-final-json-demo"
bucketRegion = "us-west-1"

# Creates an s3 Resource; this is a higher level API type service for s3.
s3 = boto3.resource('s3')

# Get all of the buckets
bucket_iterator = s3.buckets.all()

# Loop through the buckets

for bucket in bucket_iterator:
    if bucket.name == bucketInputName:
        print("Found the input bucket\t:\t", bucket.name)
    if bucket.name == bucketOutputName:
        print("Found the output bucket\t:\t", bucket.name)
