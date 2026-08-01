import boto3
# Variables for the bucket name and the region we will be using.
# Important Note: s3 Buckets are globally unique, as such you need to change the name of the bucket to something else.
# Important Note: If you would like to use us-east-1 as the region, when making the s3.create_bucket call, then do not specify any region.
bucketName = "shoe-company-final-json-demo"
bucketRegion = "us-west-1"

# Creates an s3 Resource; this is a higher level API type service for s3.
s3 = boto3.resource('s3')

# Creates a bucket
bucket = s3.create_bucket(ACL='private',Bucket=bucketName,CreateBucketConfiguration={'LocationConstraint': bucketRegion})