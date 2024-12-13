import json
import boto3
client = boto3.client("ec2")

def lambda_handler(event, context):
    action = event['action']
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AutoStart',
                'Values': [
                    'True',
                ]
            },
        ]
    )
    # Find list of Instance Ids
    instance_ids = []
    for reservations in response['Reservations']:
        for instance in reservations['Instances']:
            instance_ids.append(instance['InstanceId'])
    print(instance_ids)

    if action == "start":
        # start instances
        print("Inside start")
        response = client.start_instances(
            InstanceIds=instance_ids
        )
    elif action == "stop":
        print("Inside stop")
        response = client.stop_instances(
            InstanceIds=instance_ids
        )

