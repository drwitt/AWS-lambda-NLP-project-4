import json
import boto3
import botocore

######################################
#LOADING JSON FILE FROM S3
######################################

s3 = boto3.resource('s3')

# Define input s3 bucket
bucket_in = s3.Bucket('covid-processed-form')

######################################
#CREATING NEW RECORD IN DYNAMODB TABLE
######################################
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('covid-papers')

for obj in bucket_in.objects.all():
    # Get body of bucket object (i.e., .json file body contents)
    body = obj.get()['Body'].read().decode('utf-8')
    json_content = json.loads(body)
    paper_id = json_content['paper_id']
    title = json_content['title'] 
    abstract = json_content['abstract']
    try:
        table.put_item(
            Item={
                'paper_id' : paper_id,
                'title' : title,
                'abstract' : abstract
            }
        )
        print('Item {} added to DynamoDB table.'.format(paper_id))
    except:
        print('No abstract item for paper {}; not added to database.'.format(paper_id))
    
