import boto3
import os
from config import Config

def setup_aws():
    """Setup AWS resources"""
    try:
        # AWS credentials should be in environment variables
        # AWS_ACCESS_KEY_ID
        # AWS_SECRET_ACCESS_KEY
        # AWS_REGION
        
        ec2 = boto3.client('ec2')
        
        # Security group configuration
        security_group = ec2.create_security_group(
            GroupName='farming-assistant-sg',
            Description='Security group for Farming Assistant'
        )
        
        # Add inbound rules
        ec2.authorize_security_group_ingress(
            GroupId=security_group['GroupId'],
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        
        return security_group['GroupId']
        
    except Exception as e:
        print(f"Error setting up AWS: {str(e)}")
        return None 