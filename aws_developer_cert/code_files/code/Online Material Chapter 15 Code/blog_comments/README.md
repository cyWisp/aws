
# Blog Comments API with AWS Lambda, DynamoDB, and X-Ray

This project is a **toy serverless application** that allows users to submit blog comments via an API Gateway. The comments are stored in a DynamoDB table, and AWS X-Ray is used to automatically trace the DynamoDB interactions. The application introduces random latency (up to 10 seconds) to simulate real-world performance variations.

## Features

- **API Gateway**: Exposes a POST endpoint to accept blog comments.
- **Lambda Function**: Handles the POST requests and writes comments to DynamoDB.
- **DynamoDB**: Stores the comments with a unique ID.
- **AWS X-Ray**: Automatically traces the Lambda function and DynamoDB interactions to monitor performance.
- **Random Latency**: Simulates random latency of up to 10 seconds before inserting a comment.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions.
- SAM CLI installed.
- Python 3.9 or later installed.

## Project Structure

```
.
├── blog-comment-lambda       # Directory containing the Lambda function code and dependencies
│   ├── index.py              # The Lambda function code
│   ├── aws_xray_sdk/         # X-Ray SDK installed via pip
├── template.yaml             # SAM template to define the infrastructure
├── README.md                 # This file
```

## Setup

### 1. Install AWS X-Ray SDK

Navigate to the `blog-comment-lambda` directory and install the AWS X-Ray SDK:

```bash
cd blog-comment-lambda
pip install aws-xray-sdk -t .
```

This will install the necessary dependencies for X-Ray instrumentation inside the Lambda deployment package.

### 2. Build the SAM Application

Use the SAM CLI to build the application:

```bash
sam build
```

### 3. Deploy the SAM Application

Deploy the application using the SAM CLI:

```bash
sam deploy --guided
```

During the guided deployment, you will be prompted to provide values for the following:
- Stack Name
- AWS Region
- Permissions for the Lambda function

### 4. Test the API

After deployment, SAM will provide an API Gateway URL. You can use this URL to submit blog comments.

Use `curl` or another HTTP client to test the POST endpoint:

```bash
curl -X POST https://<your-api-url>/Prod/add-comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "This is my test comment"}'
```

### 5. Introduced Random Latency

The Lambda function introduces a random latency of up to 10 seconds before inserting the comment into DynamoDB to simulate real-world delays. This is visible in the X-Ray traces.

## Viewing AWS X-Ray Traces

### 1. Go to the AWS X-Ray Console

Navigate to the [AWS X-Ray Console](https://console.aws.amazon.com/xray/home) in your AWS account.

### 2. Select Your Lambda Service

Find the traces for your Lambda function. You should see traces showing:
- API Gateway calling the Lambda function.
- The random latency introduced.
- DynamoDB `put_item` operations captured automatically by X-Ray.

### 3. View Service Map and Latency

You can visualize the entire flow of your request in the **Service Map**, including the random latency introduced and the DynamoDB write operation. You will see the response times and any potential issues that may arise from the delay.

## Clean Up

After you're done experimenting, you can delete the deployed resources to avoid unnecessary charges:

```bash
sam delete
```

This command will remove all the resources created by SAM, including the API Gateway, Lambda function, and DynamoDB table.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
