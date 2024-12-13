import boto3
client = boto3.client('s3')

file_reader = open('create_bucket.py').read()
response = client.put_object(
    ACL='private',
    Body=file_reader,
    bucket='BucketName',
    Key='create_bucket.py'
)