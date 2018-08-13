import boto3
from django.conf import settings

if settings.LOCAL:
    sqs_client = boto3.client('sqs',
                              #endpoint_url='http://sqs:9324',
                              endpoint_url='http://localstack:4576',
                              region_name='elasticmq',
                              aws_secret_access_key='x',
                              aws_access_key_id='x',
                              use_ssl=False
                              )
else:
    sqs_client = boto3.client('sqs', region_name='us-east-1')

# sqs_client.create_queue
# queues {
#     "bountiesqueue.fifo" {
#         defaultVisibilityTimeout = 31 seconds
#         delay = 0 seconds
#         isFifo = true
#         receiveMessageWait = 0 seconds
#     }
# }
