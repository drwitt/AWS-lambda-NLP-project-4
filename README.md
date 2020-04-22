# AWS-lambda-NLP-project-4

The repository is for code supporting a project for the ECE 590/ MIDS 690 course at Duke University in Spring 2020. 

## Introduction
The [COVID-19 Open Research Dataset Challenge (CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) is a resource of over 52,000 scholarly articles, including over 41,000 with full text, about COVID-19, SARS-CoV-2, and related coronaviruses. 

The goal of this repository and project are to present a working framework for using this data to create a database in DynamoDB and to use lambda serverless architecture within AWS to serve and apply basic NLP processing to the journal articles. 

## Steps

### 1) 
Set up github repo. 

### 2)
Access AWS via CLI/SDK or an IDE within AWS (Cloud9); I used Cloud9. 

### 3)
Generate rsa public key permission on new compute instance and add to settings in github. Then clone git repository onto cloud compute instance and set up venv with requirements.txt.

### 4)
Upload original json article files to AWS S3 bucket.

### 5)
Run scripts to extract desired features ('paper_id', 'title', 'abstract', etc.) from native json files, save in simplified json format, and upload to DynamoDB.

$ python ./s3_parse_json.py
$ python ./s3toDynamoDB.py 

### 6) 
Deploy 'producer' and 'consumer' lambda functions from within Cloud9 IDE. 

The producer lambda function (./producerapril19/producerapril19/lambda_function.py) is designed to read rows of the constructed DynamoDB database and serve them to a SQS queue. 

The consumer labmda function (./consumerapril19/consumerapril19/lambda_function.py) is designed to accept payloads from the SQS queue, apply simple NLP entity detection (via [AWS Comprehend Medical](https://aws.amazon.com/comprehend/medical/)) to the journal title, and return those features to an output s3 bucket.  

### 7)
Lambda functions can be controlled via the [AWS Lambda Service](https://aws.amazon.com/lambda/) and traffic in and out of the queue can be monitored via dashboards in [AWS Simple Queue Service (SQS)](https://aws.amazon.com/sqs/). 

## Data Source
Find data [here](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge). 

## References
https://github.com/noahgift/awslambda
