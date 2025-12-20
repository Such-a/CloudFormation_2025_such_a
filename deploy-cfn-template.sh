#!/usr/bin/env bash

# Usage: ./scripts/deploy-cfn-template.sh <BUCKET_NAME> <AWS_REGION> <HF_API_TOKEN>
if [ -z "$3" ]; then
    echo "Usage: ./scripts/deploy-cfn-template.sh <BUCKET_NAME> <AWS_REGION> <HF_API_TOKEN>"
    exit 1
fi

BUCKET_NAME="$1"
AWS_REGION="$2"
HF_API_TOKEN="$3"
STACK_NAME="my-python-lambda-stack20"


printf "\n--> Uploading Lambda code to S3 bucket %s ...\n" "${BUCKET_NAME}"


printf "\n--> Packaging CloudFormation template ...\n"
aws cloudformation package \
  --template-file ./updated_infrastructure.template \
  --s3-bucket "${BUCKET_NAME}" \
  --s3-prefix "${STACK_NAME}" \
  --output-template-file ./infrastructure-packaged.template \
  --region "${AWS_REGION}"

printf "\n--> Validating template ...\n"
aws cloudformation validate-template \
  --template-body file://infrastructure-packaged.template

printf "\n--> Deploying CloudFormation stack %s ...\n" "${STACK_NAME}"
aws cloudformation deploy \
  --template-file ./infrastructure-packaged.template \
  --stack-name "${STACK_NAME}" \
  --region "${AWS_REGION}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      LambdaExecutionRoleArn="arn:aws:iam::763884754454:role/LabRole" \
      S3BucketName="${BUCKET_NAME}" \
      HuggingFaceApiToken="${HF_API_TOKEN}"

printf "\n--> Deployment complete!\n"
