📌# CloudFormation_2025_such_a

📌################ 🚀task1 ###########################################📌

Create a CloudFormation template in YAML or JSON format.
In the template, specify the S3 bucket resource that will host the website.

In the Properties section of the S3 bucket resource, view the WebsiteConfiguration parameter.
In the WebsiteConfiguration parameters, specify the IndexDocument and ErrorDocument parameters, which are the Index and Error files of your website (for example, index.html, error.html).

Create a Bucket Policy in JSON format that allows public access to your website files.
In the CloudFormation template, specify the BucketPolicy.

Create, retrieve, or generate a simple static website (for example, with HTML, CSS, and JavaScript files).
Using the AWS Management Console or the AWS CLI, upload your website files to the S3 bucket.
 
📌################## 🚀task2 ############################################📌

create a cloudformation EC2 template that will create an EC2 instance and an S3 bucket to store the EC2 logs (depending on the server, the logs are recorded for several more steps), add a system variable to the running system, for example LOG_BUCKET, and the value of this LOG_BUCKET variable will be the name of the S3 bucket.

None of the variables should be hardcoded, everything should be modular (look for examples in the lecture).

All sections are optional sections by default.

The choice in your template AppEnv parameter can be dev, staging, production.

Another Fn::Sub function to dynamically determine the name of the S3 bucket. The bucket name should be a multiple of the LogBucketNamePrefix 

parameter value and end with a suffix (for example, your initials or another unique identifier). For example:
${LogBucketNamePrefix}-my-logs-unique-id.

Define the EC2 instance resource ImageId: Use the Ref function with the AmiID parameter value.

InstanceType: Use the Ref function to define the InstanceType parameter value.

UserData: Use the Fn::Base64 and Fn::Sub functions to define user data A script that will run commands, for example, yum update -y, the bash script should write a S3ket with the same name LOG_BUCKET=${WebServerLogBucketnV}$App_ENV=}$APP_EN System variables.

task2.yaml is for aws learner lab, because IAM is not supported, and task2-1.yaml is for personal aws account.

📌############################## 🚀task3 ##################################📌

Aurora MySQL Database Stack

This CloudFormation template creates an Aurora MySQL database with Secrets Manager integration.

Test environment: uses a simple hardcoded secret.

Production environment: generates secure database credentials automatically.

Includes database security groups and outputs endpoint, port, and secret references.


📌##################################### 🚀task4 ############################## 📌

Create a custom rule for cfn-lint that checks for:

In AWS::EC2::Instance resources:
If the InstanceType is t2.micro, then a Tag named FreeTierEligible with a value of true is required.
If the InstanceType is m5.large, then a Tag named PerformanceCritical with a value of true or false is required.

For the VolumeType Property in AWS::EC2::Volume resources, if its value is gp3, then a Tag named Priority is required and its value must be in the range of 3000 to 16000.

For AWS::S3::Bucket resources:
If the PublicAccessBlockConfiguration Property exists and one of its parameters (for example, BlockPublicAcls) is false, then a Tag named PublicAccessAllowed with a value of true is required.

Customize your .cfnlintrc with cfn-lint to make your custom rule as customizable as possible. 



📌##################################### 🚀task6 ############################## 📌

Your company needs to automatically create two types of environments (for example, "test" and "production") using CloudFormation. Each environment may or may not have its own S3 Bucket for logging. Additionally, if an S3 Bucket is created, it must have a Bucket Policy set on it.

Create a CloudFormation template that accepts the following Parameters:

🔖 EnvironmentType (Type: String): Valid values: test or production. This parameter specifies which type of environment is being created.
CreateLoggingBucket (Type: String): Valid values: true or false. This parameter specifies whether to create an S3 Bucket for logging.

🔖 Use the Conditions section:
Create a condition called ShouldCreateLoggingBucketCondition that will be true if the value of the CreateLoggingBucket parameter is true.
Create a condition called IsProductionEnvironmentCondition that will be true if the value of the EnvironmentType parameter is production.

Create the following Resources:

🔖 S3 Bucket for Logging (AWS::S3::Bucket):
This resource should only be created if the ShouldCreateLoggingBucketCondition condition is true.

The Bucket Name (BucketName) should include the environment type (e.g., test-logs-your-unique-id or prod-logs-your-unique-id). You can do this by using the Fn::Join or Fn::Sub functions with the EnvironmentType parameter and AWS::AccountId for uniqueness.
S3 Bucket Policy (AWS::S3::BucketPolicy):

This resource should only be created if the S3 Bucket for Logging has been created (i.e., the ShouldCreateLoggingBucketCondition condition is true).
The policy should grant s3:GetObject permission on this Bucket.
Important: Creating an S3 Bucket Policy must be dependent on creating an S3 Bucket. Use the DependsOn attribute to ensure that the Bucket Policy is created only after the Bucket is successfully created.

🔖 EC2 Instance (AWS::EC2::Instance) (conditional):
This resource should only be created if the IsProductionEnvironmentCondition condition is true.
Use a test ImageId (for example, the Amazon Linux 2 AMI ID appropriate for the region) and InstanceType (for example, t2.micro).

🔖 Use Outputs:
If the S3 Bucket was created, output the LoggingBucketName (the name of the S3 Bucket).
If the EC2 Instance was created, output the ProductionInstanceId (the ID of the EC2 Instance).



📌##################################### 🚀task7 ############################## 📌

The deployment consists of four nested stacks:

🔖 VPC Stack (vpc.yaml)

Creates a VPC with two public subnets across different Availability Zones.
Includes Internet Gateway and route tables for public connectivity.
Outputs the VPC ID and subnet IDs for downstream stacks.

🔖 EC2 Stack (ec2.yaml)

Launches a web server EC2 instance in the first public subnet.
Installs Apache and PHP via cfn-init.
Displays instance metadata and outputs on the browser, including:
EC2 Instance ID
Availability Zone
AMI ID
RDS Table Name
SNS Topic Name
Associates an Elastic IP for public access.

🔖 RDS Stack (rds.yaml)

Creates a MySQL RDS instance with a security group and DB subnet group.
Uses two public subnets from the VPC stack.
Outputs the database endpoint and table name (testdb).

🔖 SNS Stack (sns.yaml)

Creates an SNS topic per environment (Dev, Test, Prod).
Outputs the topic name and ARN for integration with EC2.

🔖 Root Stack (main.yaml)

Orchestrates all nested stacks and passes outputs to EC2.
Ensures that the EC2 instance can dynamically display:
RDS table name
SNS topic name
Deploys all resources in the correct order.
Deployment Outcome
After the CloudFormation deployment completes:
Access the web server using its public IP.


🔖 The page will display:

EC2 Instance ID: i-0abc123def
Availability Zone: eu-central-1a
AMI ID: ami-123abc456
RDS Table Name: testdb
SNS Topic Name: Test-NotificationsTopic


📌##################################### 🚀task8 ############################## 📌

We had vpc and EC2 cross-stacks and I added The rds stack, which will also a cross-stack and ultimately determines the name of the rds table that should appear when going to the ec2 endpoint.


📌##################################### 🚀task10 ############################## 📌

A company needs to create a messaging system (SNS Topics) for N departments: Marketing, Sales, and Engineering. Your task is to create a CloudFormation template that will do this automatically and make it easy to add new departments in the future.
