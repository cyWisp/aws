#!/usr/bin/env python3
import aws_cdk as cdk
from lambda_test import S3LambdaStack  # Adjust based on your directory structure

app = cdk.App()
S3LambdaStack(app, "S3LambdaStack")

app.synth()

