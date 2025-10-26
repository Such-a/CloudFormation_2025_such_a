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
