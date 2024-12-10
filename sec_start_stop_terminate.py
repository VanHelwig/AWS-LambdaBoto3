#!/bin/python3

import boto3

instance1_id = 'i-0445b54069ab43165'

client = boto3.client('ec2')
client.terminate_instances(InstanceIds=[instance1_id])