## AWS Common Services Cheatsheet

### 1. Compute Services

#### EC2 (Elastic Compute Cloud)
```bash
# Launch a new EC2 instance
aws ec2 run-instances --image-id ami-EXAMPLE --count 1 --instance-type t2.micro

# Stop an EC2 instance
aws ec2 stop-instances --instance-ids i-EXAMPLE

# Terminate an EC2 instance
aws ec2 terminate-instances --instance-ids i-EXAMPLE

# List EC2 Instances
aws ec2 describe-instances

# Create a new key pair
aws ec2 create-key-pair --key-name MyKeyPair

# Create a security group
aws ec2 create-security-group --group-name MySecurityGroup --description "My security group"
```

#### Lambda
```bash
# Create a new Lambda function
aws lambda create-function --function-name MyFunction --runtime python3.7 --role MyRole --handler lambda_function.lambda_handler --zip-file fileb://my-deployment-package.zip

# Invoke a Lambda function
aws lambda invoke --function-name MyFunction --payload '{"key": "value"}' output.txt

# Update a Lambda function's code
aws lambda update-function-code --function-name MyFunction --zip-file fileb://my-new-code.zip

# Delete a Lambda function
aws lambda delete-function --function-name MyFunction
```

### 2. Storage Services

#### S3 (Simple Storage Service)
```bash
# Create a new S3 bucket
aws s3 mb s3://my-bucket

# List S3 buckets
aws s3 ls

# Copy a file to an S3 bucket
aws s3 cp myfile.txt s3://my-bucket/myfile.txt

# Delete an S3 bucket
aws s3 rb s3://my-bucket --force

# Sync a directory with an S3 bucket
aws s3 sync my-folder s3://my-bucket

# Enable versioning on an S3 bucket
aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled
```

### 3. Database Services

#### RDS (Relational Database Service)
```bash
# Create a new RDS instance
aws rds create-db-instance --db-name mydatabase --db-instance-identifier MyDBInstance --engine MySQL --master-username masteruser --master-user-password masterpass --allocated-storage 20 --instance-class db.t2.micro

# List RDS instances
aws rds describe-db-instances

# Delete an RDS instance
aws rds delete-db-instance --db-instance-identifier MyDBInstance

# Modify an RDS instance
aws rds modify-db-instance --db-instance-identifier MyDBInstance --db-instance-class db.m4.large

# Reboot an RDS instance
aws rds reboot-db-instance --db-instance-identifier MyDBInstance
```

### 4. Networking and Content Delivery

#### VPC (Virtual Private Cloud)
```bash
# Create a new VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Delete a VPC
aws ec2 delete-vpc --vpc-id vpc-EXAMPLE

# Describe VPCs
aws ec2 describe-vpcs

# Create a subnet
aws ec2 create-subnet --vpc-id vpc-EXAMPLE --cidr-block 10.0.1.0/24
```

### 5. Developer Tools

#### CodeBuild
```bash
# Start a build project
aws codebuild start-build --project-name my-project

# List build projects
aws codebuild list-projects

# Delete a build project
aws codebuild delete-project --name my-project
```

### 6. Analytics Services

#### EMR (Elastic MapReduce)
```bash
# Create a new EMR cluster
aws emr create-cluster --name "My cluster" --release-label emr-5.28.0 --applications Name=Spark --instance-type m5.xlarge --instance-count 3

# List clusters
aws emr list-clusters --active

# Terminate clusters
aws emr terminate-clusters --cluster-ids j-EXAMPLE
```

### 7. Machine Learning Services

#### SageMaker
```bash
# Create a training job
aws sagemaker create-training-job --training-job-name my-training-job --algorithm-specification TrainingImage=my-docker-image,TrainingInputMode=File --role-arn my-iam-role --input-data-config ChannelName=train,S3Uri=s3://my-bucket/train,InputMode=File --output-data-config S3OutputPath=s3://my-bucket/output

# Create a model
aws sagemaker create-model --model-name MyModel --primary-container Image=my-docker-image,ModelDataUrl=s3://my-bucket/model.tar.gz

# Delete a model
aws sagemaker delete-model --model-name MyModel
```

### 8. Security and Identity Services

#### IAM (Identity and Access Management)
```bash
# Create a new IAM user
aws iam create-user --user-name MyUser

# Create an IAM policy
aws iam create-policy --policy-name MyPolicy --policy-document file://mypolicy.json

# Attach a policy to a user
aws iam attach-user-policy --user-name MyUser --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Delete a user
aws iam delete-user --user-name MyUser
```

### 9. Migration & Transfer

#### Snowball
```bash
# Create a new Snowball job
aws snowball create-job --job-type IMPORT --resources S3BucketArn=arn:aws:s3:::my-bucket

# List Snowball jobs
aws snowball list-jobs

# Cancel a Snowball job
aws snowball cancel-job --job-id JID123e4567-e89b-12d3-a456-426655440000

# Describe a Snowball job
aws snowball describe-job --job-id JID123e4567-e89b-12d3-a456-426655440000
```

This cheatsheet provides an overview of commonly used commands for various AWS services. For full details and additional commands, please refer to the [official AWS documentation](https://docs.aws.amazon.com/cli/latest/index.html).
