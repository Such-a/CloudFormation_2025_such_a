# Serverless Dashboard – DevOps & Cloud Architecture Project

## Overview

This project implements a **production-style serverless web application on AWS**, designed using **Infrastructure as Code (IaC)** and **secure cloud networking best practices**.

The architecture emphasizes:

- Automation
- Security isolation
- Scalability
- Clear separation of frontend, backend, and database layers

All infrastructure is provisioned and managed using **AWS CloudFormation**.

---

## Architecture Components

### Frontend (Amazon S3 – Static Website Hosting)

- Static frontend hosted on **Amazon S3**
- Website hosting enabled on the bucket
- Public access configuration:
  - Public access blocks disabled
  - Bucket policy allows **read-only (GET)** access
- Security characteristics:
  - No embedded credentials
  - No direct database access
  - Communicates only with the backend API over HTTPS

---

### Backend (AWS Lambda – Python 3.12)

- AWS Lambda function running **Python 3.12**
- Deployed inside **private subnets** of a custom VPC
- Security configuration:
  - Dedicated Lambda security group
  - Outbound traffic only
- Configuration management:
  - Database connection details injected via **environment variables**
  - No hard-coded secrets
- Networking:
  - Connects to RDS using private networking
  - No public internet access required

---

### API Layer (Amazon API Gateway v2 – HTTP API)

- API Gateway **HTTP API (v2)**
- Lambda integration:
  - `AWS_PROXY` integration
  - Payload format version **2.0**
- Features:
  - Native request and response passthrough
  - No custom mapping templates
- CORS configuration:
  - Enabled for browser-based requests from the S3 website
- Deployment:
  - Default stage
  - Auto-deploy enabled

---

### Database (Amazon RDS – MySQL)

- Amazon RDS running **MySQL**
- Deployment configuration:
  - Hosted in **private subnets**
  - DB Subnet Group spanning multiple Availability Zones
- Security:
  - Public accessibility disabled
  - Security group rules:
    - Inbound access on port **3306**
    - Allowed only from:
      - Lambda security group
      - EC2 bastion host security group
- Purpose:
  - Persistent data storage
  - Fully isolated from public networks

---

## Networking Architecture (Amazon VPC)

- Custom Amazon VPC:
  - CIDR block: `10.0.0.0/16`
- Subnet design:
  - **Public subnet**
    - EC2 bastion host
  - **Private subnets**
    - AWS Lambda
    - Amazon RDS
- Internet connectivity:
  - Internet Gateway attached to the VPC
  - Public subnet associated with an internet-facing route table
  - Private subnets have no direct internet exposure

---

## Bastion Host (Amazon EC2)

- EC2 instance deployed in the **public subnet**
- Role:
  - Acts as a bastion host for administrative access
  - Enables secure connectivity to private resources
- Access method:
  - SSH enabled
  - SSH port forwarding used to access RDS
- Security benefit:
  - Database remains private and unreachable from the internet

---

## Infrastructure as Code (AWS CloudFormation)

All infrastructure is provisioned and managed using **AWS CloudFormation**, including:

- VPC, subnets, route tables, and Internet Gateway
- Security groups
- S3 buckets
- AWS Lambda function
- API Gateway configuration
- RDS MySQL instance
- EC2 bastion host
- IAM role usage

### Benefits

- Idempotent deployments
- Repeatable environments
- Full infrastructure version control
- Simplified teardown and redeployment

---

## Application Request Flow

1. User accesses the static frontend hosted on **Amazon S3**
2. Frontend sends an HTTP request to **API Gateway**
3. API Gateway invokes the **AWS Lambda** function
4. Lambda executes inside the **private VPC**
5. Lambda connects to **RDS MySQL** via private networking
6. Database response is processed by Lambda
7. API Gateway returns the response to the frontend

---

## Operational Notes

- Deployment prerequisites:
  - Existing IAM role with Lambda execution permissions
  - S3 bucket for Lambda deployment artifacts
- Deployment method:
  - AWS CLI with CloudFormation
- Configuration management:
  - Secrets and configuration injected via environment variables
  - No credentials stored in source code or frontend
- Database access:
  - Performed via EC2 bastion host
  - SSH port forwarding used for secure access
- Security posture:
  - RDS has no public endpoint
  - Network access tightly restricted via security groups

---

## Key Skills Demonstrated

- Serverless architecture design
- Secure AWS VPC networking
- Infrastructure as Code (CloudFormation)
- API Gateway and Lambda integration
- Secure database access patterns
- DevOps automation and cloud resource management
