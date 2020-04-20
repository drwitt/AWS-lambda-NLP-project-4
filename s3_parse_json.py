import json
import boto3
import botocore


s3 = boto3.resource('s3')

# Define input, output s3 buckets
bucket_in = s3.Bucket('covid-raw')
bucket_out_nm = 'covid-processed-form'

def jsonifize(paper_id, title, abstract):
    return {"paper_id": paper_id,
            "title": title,
            "abstract": abstract}, '{}_cleaned.json'.format(paper_id)

for obj in bucket_in.objects.all():
    # Get body of bucket object (i.e., .json file body contents)
    body = obj.get()['Body'].read().decode('utf-8')
    #print(type(body)) # should be a str type object after using .decode()
    body_dict = json.loads(body) # returns dictionary type object
    #print(body_dict.keys())
    
    # Parse json file for paper_id, title, and abstract text strings
    paper_id =  body_dict['paper_id']
    metadata = body_dict['metadata']
    title = metadata['title']
    # Note, not all abstracts are present in json files
    try:
        abstract = body_dict['abstract'][0]
        abstract = abstract['text']
    except:
        print('{} abstract not formatted as others.'.format(paper_id))
        # Check if empty abstract
        if not abstract:
            abstract = None
            pass
        else:
            abstract = body_dict['abstract']
   
    
    # Convert into simplified json file 
    clean_body, fname = jsonifize(paper_id, 
                                  title, 
                                  abstract
                                  )
    
    s3.Object(bucket_out_nm, fname).put(Body= json.dumps(clean_body))
    print('File {} created in s3'.format(fname))

