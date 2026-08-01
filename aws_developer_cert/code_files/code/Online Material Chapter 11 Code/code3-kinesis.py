import boto3
import random
import json

# Create the client.
kinesis_client = boto3.client('kinesis')

# Create the stream.
kinesis_client.create_stream(
  StreamName='donut-sales',
  ShardCount=2)

# Wait for stream to be created.
waiter = kinesis_client.get_waiter('stream_exists')
waiter.wait(StreamName='donut-sales')

# Store each donut sale using location as partition key.
location = 'california'
data = b'{"flavor":"chocolate","quantity":12}'
kinesis_client.put_record(
    StreamName='donut-sales',
    PartitionKey=location, Data=data)
print("put_record: " + location + " -> " + data)

# Next lets put some random records.

# List of location, flavors, quantities.
locations = ['california', 'oregon', 'washington', 'alaska']
flavors = ['chocolate', 'glazed', 'apple', 'birthday']
quantities = [1, 6, 12, 20, 40]

# Generate some random records.
for i in xrange(20):

    # Generate random record.
    flavor = random.choice(flavors)
    location = random.choice(locations)
    quantity = random.choice(quantities)
    data = json.dumps({"flavor": flavor, "quantity": quantity})

    # Put record onto the stream.
    kinesis_client.put_record(
        StreamName='donut-sales',
        PartitionKey=location, Data=data)
    print("put_record: " + location + " -> " + data)

# Get the records.

# Get shard_ids.
response = kinesis_client.list_shards(StreamName='donut-sales')
shard_ids = [shard['ShardId'] for shard in response['Shards']] 
print("list_shards: " + str(shard_ids))

# For each shard_id print out the records.
for shard_id in shard_ids:

    # Print current shard_id.
    print("shard_id=" + shard_id)

    # Get a shard iterator from this shard.
    # TRIM_HORIZON means start from earliest record.
    response = kinesis_client.get_shard_iterator(
        StreamName='donut-sales',
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON')
    shard_iterator = response['ShardIterator']

    # Get records on shard and print them out.
    response = kinesis_client.get_records(ShardIterator=shard_iterator)
    records = response['Records']
    for record in records:
        location = record['PartitionKey']
        data = record['Data']
        print("get_records: " + location + " -> " + data)

# Delete the stream.
kinesis_client.delete_stream(
  StreamName='donut-sales')

# Wait for stream to be deleted.
waiter = kinesis_client.get_waiter('stream_not_exists')
waiter.wait(StreamName='donut-sales')

