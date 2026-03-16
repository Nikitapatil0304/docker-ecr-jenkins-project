import json
import boto3
from datetime import datetime

sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

topic_arn = "arn:aws:sns:ap-south-1:718383533665:docker-deployment-alert"

table = dynamodb.Table('ecr-image-logs')

def lambda_handler(event, context):

    repo = event['detail']['repository-name']
    tag = event['detail']['image-tag']

    message = f"New image pushed {repo}:{tag}"

    # SNS Notification
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject="Docker Deployment"
    )

    # DynamoDB Logging
    table.put_item(
        Item={
            'imageTag': tag,
            'repository': repo,
            'timestamp': str(datetime.now())
        }
    )

    return {
        'statusCode':200,
        'body':message
    }
