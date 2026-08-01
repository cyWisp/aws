# This example shows loading of SDK via a profile

import boto3
from botocore.exceptions import ClientError

print("Loading credentials from the 'restricted' profile")
session = boto3.session.Session(profile_name="restricted")
polly = session.client('polly',region_name="eu-west-2")


# Read the lexicon contents from the a local file
with open('aws-lexicon.xml','r') as file:
    lexicon = file.read()

print("Attempting to upload lexicon...")

try:
	response = polly.put_lexicon(
    	Content=lexicon,
    	Name='awsLexicon',
	)
	print("Done!")

except ClientError as e:
	if e.response['Error']['Code'] == 'AccessDeniedException':
		print("*********************")
		print(e)
		print ("********************")
		print ("Don't panic. =) This exception is expected!")
		print ("Continue with the exercise to fix it.")
	else:
		print(e)



