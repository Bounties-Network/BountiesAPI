import boto3
from django.conf import settings

if settings.LOCAL:
    sqs_client = boto3.client('sqs',
                              endpoint_url='http://sqs:9324',
                              region_name='elasticmq',
                              aws_secret_access_key='x',
                              aws_access_key_id='x',
                              use_ssl=False
                              )
else:
    sqs_client = boto3.client('sqs', region_name='us-east-1')
