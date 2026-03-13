import json
import boto3
from datetime import datetime

sns = boto3.client('sns')

topic_arn = "SNS_TOPIC_ARN"

def lambda_handler(event, context):

    repo = event['detail']['repository-name']
    tag = event['detail']['image-tag']

    message = f"New image pushed {repo}:{tag}"

    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject="Docker Deployment"
    )

    return {
        'statusCode':200,
        'body':message
    }
