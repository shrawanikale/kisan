import os
import sys
import boto3
from botocore.exceptions import ClientError

def deploy_to_ec2():
    """Deploy application to EC2"""
    try:
        ec2 = boto3.client('ec2')
        
        # Launch EC2 instance
        instance = ec2.run_instances(
            ImageId='ami-0c55b159cbfafe1f0',  # Ubuntu 20.04 LTS
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            SecurityGroups=['farming-assistant-sg'],
            UserData='''#!/bin/bash
                sudo apt-get update
                sudo apt-get install -y python3-pip nginx
                git clone https://github.com/yourusername/farming-assistant.git
                cd farming-assistant
                pip3 install -r requirements.txt
                sudo systemctl start nginx
                python3 run.py
            '''
        )
        
        instance_id = instance['Instances'][0]['InstanceId']
        print(f"Instance launched: {instance_id}")
        
        # Wait for instance to be running
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        # Get instance public IP
        instance_info = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = instance_info['Reservations'][0]['Instances'][0]['PublicIpAddress']
        
        print(f"Application deployed at: http://{public_ip}:5000")
        return public_ip
        
    except Exception as e:
        print(f"Deployment error: {str(e)}")
        return None 