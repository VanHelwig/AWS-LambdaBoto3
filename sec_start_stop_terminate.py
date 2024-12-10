#!/bin/python3

import boto3
import argparse
import json
import os
import yaml

# Initialize the EC2 client
client = boto3.client('ec2')

def load_inventory(file_path):
    """Load the inventory file (JSON or YAML)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Inventory file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith(('.yaml', '.yml')):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format. Use JSON or YAML.")

def start_instance(instance_id):
    """Start an EC2 instance."""
    response = client.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}. Current state: {response['StartingInstances'][0]['CurrentState']['Name']}")

def stop_instance(instance_id):
    """Stop an EC2 instance."""
    response = client.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}. Current state: {response['StoppingInstances'][0]['CurrentState']['Name']}")

def terminate_instance(instance_id):
    """Terminate an EC2 instance."""
    response = client.terminate_instances(InstanceIds=[instance_id])
    print(f"Terminating instance {instance_id}. Current state: {response['TerminatingInstances'][0]['CurrentState']['Name']}")

def main():
    parser = argparse.ArgumentParser(description="Manage EC2 instances using Boto3.")
    parser.add_argument("action", choices=["start", "stop", "terminate"], help="Action to perform on the instance.")
    parser.add_argument("instance_name", help="Name of the instance as defined in the inventory file.")
    parser.add_argument("--inventory", default="inventory.json", help="Path to the inventory file (default: inventory.json).")

    args = parser.parse_args()

    # Load inventory
    try:
        inventory = load_inventory(args.inventory)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return

    # Get the instance ID from the inventory
    instance_id = inventory.get(args.instance_name)
    if not instance_id:
        print(f"Instance '{args.instance_name}' not found in the inventory file.")
        return

    # Perform the requested action
    if args.action == "start":
        start_instance(instance_id)
    elif args.action == "stop":
        stop_instance(instance_id)
    elif args.action == "terminate":
        terminate_instance(instance_id)

if __name__ == "__main__":
    main()
