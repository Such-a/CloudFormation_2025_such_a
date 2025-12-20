📌################ 🚀task9 ###########################################📌

This project demonstrates how to package and deploy an AWS Lambda function using AWS CloudFormation and the AWS CLI. It covers preparing Lambda code with dependencies, uploading artifacts to Amazon S3, generating a packaged CloudFormation template, deploying the stack, and testing the Lambda function. The project also includes automation scripts and a DynamoDB-backed Lambda example.



aws cloudformation package \
--template-file infrastructure.template \
--s3-bucket example-bucket-name \
--s3-prefix cfn-package-deploy \
--output-template-file infrastructure-packaged.template


aws cloudformation deploy \
  --template-file packaged-template.yaml \
  --stack-name my-python-lambda-stack \
  --parameter-overrides LambdaExecutionRoleArn="arn:aws:iam::123456789012:role/YourExistingLambdaRoleName" 


  aws lambda invoke \
--function-name cfn-python-function \
--payload "{\"time_zone\": \"Europe/London\"}" \
--cli-binary-format raw-in-base64-out \
response.json
