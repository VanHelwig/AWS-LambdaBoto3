import json
import boto3
import os

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    try:
        # Extract instance ID from the event
        instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
        
        # S3 bucket and object details
        bucket_name = 'jhc-auto-tagging'
        object_key = 'tags.json'
        local_file_path = '/tmp/tags.json'
        
        # Download tags.json from S3
        s3.download_file(bucket_name, object_key, local_file_path)
        print(f"Downloaded {object_key} to {local_file_path}")
        
        # Read the tags.json file
        with open(local_file_path, 'r') as file:
            tags = json.load(file)  # Load tags as a list of dictionaries
        
        # Apply tags to the EC2 instance
        ec2.create_tags(Resources=[instance_id], Tags=tags)
        print(f"Tags applied to instance {instance_id}: {tags}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Tags successfully applied to instance {instance_id}")
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
