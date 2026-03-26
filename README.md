# 🚀 Automated Docker Image Deployment to Amazon ECR with Jenkins & Lambda Integration

![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![ECR](https://img.shields.io/badge/AWS-ECR-yellow)
![Lambda](https://img.shields.io/badge/AWS-Lambda-purple)
![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-blue)
![SNS](https://img.shields.io/badge/AWS-SNS-green)

---

# 📌 Project Overview

This project implements a **CI/CD pipeline** that automatically builds Docker images using **Jenkins**, pushes them to **Amazon Elastic Container Registry (ECR)**, and triggers **AWS Lambda** for post-deployment automation.

The pipeline eliminates manual Docker builds and ensures:

* Automated image building
* Consistent versioning
* Event-driven automation
* Deployment logging
* Email notifications

---

# 🧩 Scenario

Your company currently builds Docker images manually and pushes them to Amazon ECR.

This manual workflow causes several problems:

* Version conflicts
* Missed image updates
* No automated post-deployment tasks

To solve this problem, a **CI/CD pipeline using Jenkins and AWS services** was implemented.

---

# 🎯 Objective

Design and implement a CI/CD pipeline where:

* Jenkins builds Docker images automatically
* Images are pushed to Amazon ECR
* AWS Lambda is triggered automatically
* Deployment events are logged and notifications are sent

---

# 🏗️ Architecture Diagram

<img width="1536" height="1024" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/1124a990-b055-480a-8652-9438a7f07c8d" />


```
Developer
   │
   ▼
GitHub Repository
   │
   ▼
Jenkins Pipeline
   │
   ├── Build Docker Image
   ├── Tag Image (Build Number)
   └── Push Image to AWS ECR
            │
            ▼
        Amazon ECR
            │
            ▼
       EventBridge Rule
            │
            ▼
        AWS Lambda
        /        \
       ▼          ▼
   Amazon SNS   DynamoDB
  Email Alerts  Deployment Logs
```

---

# 🛠️ Technologies & Tools

| Technology      | Purpose                |
| --------------- | ---------------------- |
| Docker          | Containerization       |
| Jenkins         | CI/CD Pipeline         |
| GitHub          | Source Code Management |
| Amazon ECR      | Docker Image Registry  |
| AWS Lambda      | Serverless Automation  |
| Amazon SNS      | Email Notification     |
| Amazon DynamoDB | Deployment Logging     |
| CloudWatch      | Monitoring & Logs      |

---

# 📂 Project Structure

```
docker-ecr-jenkins-project
│
├── Dockerfile
├── Jenkinsfile
│
├── app
│   └── app.py
│
└── lambda
    └── lambda_function.py
```

---

# 🐳 Docker Setup

### Dockerfile

```
FROM python:3.9-slim

WORKDIR /app

COPY app/ /app/

RUN pip install flask

EXPOSE 5000

CMD ["python","app.py"]
```

### Build Docker Image

```
docker build -t docker-ecr-jenkins-project .
```

### Run Container

```
docker run -p 5000:5000 docker-ecr-jenkins-project
```

---

# ☁️ Amazon ECR Setup

### Login to ECR

```
aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
```

### Tag Image

```
docker tag docker-ecr-jenkins-project:latest \
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/docker-ecr-jenkins-project:latest
```

### Push Image

```
docker push ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/docker-ecr-jenkins-project:latest
```

---

# ⚙️ Jenkins Pipeline

The Jenkins pipeline automates the Docker build and deployment process.

### Pipeline Stages

1. Pull code from GitHub
2. Build Docker image
3. Tag image with build number
4. Push image to Amazon ECR

### Jenkinsfile

```
pipeline {
 agent any

 environment {
  AWS_REGION = 'ap-south-1'
  ACCOUNT_ID = '718383533665'
  REPO_NAME = 'jenkins-docker-demo'
  IMAGE_TAG = "${BUILD_NUMBER}"
 }

 stages {

  stage('Pull Code') {
   steps {
    git branch: 'main', url: 'https://github.com/your-repo.git'
   }
  }

  stage('Build Docker Image') {
   steps {
    sh 'docker build -t $REPO_NAME:$IMAGE_TAG .'
   }
  }

  stage('Tag Image') {
   steps {
    sh '''
    docker tag $REPO_NAME:$IMAGE_TAG \
    $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG
    '''
   }
  }

  stage('Push Image') {
   steps {
    sh '''
    docker push \
    $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG
    '''
   }
  }
 }
}
```

---

# ⚡ Lambda Integration

When a Docker image is pushed to ECR, **EventBridge triggers AWS Lambda**.

### Lambda Responsibilities

* Capture repository name
* Capture image tag
* Send SNS notification
* Store deployment logs in DynamoDB

### Lambda Code

```
import json
import boto3
from datetime import datetime

sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('ecr-image-logs')

def lambda_handler(event, context):

 repo = event['detail']['repository-name']
 tag = event['detail']['image-tag']

 message = f"New image pushed {repo}:{tag}"

 sns.publish(
  TopicArn="YOUR_SNS_TOPIC_ARN",
  Message=message,
  Subject="Docker Deployment"
 )

 table.put_item(
  Item={
   "imageTag": tag,
   "repository": repo,
   "timestamp": str(datetime.utcnow())
  }
 )

 return message
```

---

# 📧 SNS Notification

Whenever a new Docker image is pushed, an email notification is sent.

Example email:

```
Subject: Docker Deployment

New image pushed docker-deplyoment-alert:15
```

---

# 🗄️ DynamoDB Logging

Table Name:

```
ecr-image-logs
```

Example Data:

| imageTag | repository                 | timestamp  |
| -------- | -------------------------- | ---------- |
| 15       | docker-ecr-jenkins-project | 2026-03-15 |

---

# 📸 Screenshots

Jenkins Pipeline Output
<img width="1366" height="734" alt="Screenshot (75)" src="https://github.com/user-attachments/assets/2962a986-a94e-44e4-a4af-7100d126cd03" />

ECR Repository
<img width="1366" height="727" alt="Screenshot (70)" src="https://github.com/user-attachments/assets/debd0782-ccc8-4ca0-91bd-4549f203dbe2" />

Lambda Logs
<img width="1536" height="1024" alt="Lambda Logs" src="https://github.com/user-attachments/assets/a7ddc4e0-947b-4b73-a4b5-d6ad07a83b73" />

Jenkins Pipeline Output
<img width="1366" height="734" alt="Screenshot (75)" src="https://github.com/user-attachments/assets/2962a986-a94e-44e4-a4af-7100d126cd03" />

ECR Repository
<img width="1366" height="727" alt="Screenshot (70)" src="https://github.com/user-attachments/assets/debd0782-ccc8-4ca0-91bd-4549f203dbe2" />

Lambda Logs
<img width="1536" height="1024" alt="Lambda Logs" src="https://github.com/user-attachments/assets/a7ddc4e0-947b-4b73-a4b5-d6ad07a83b73" />

SNS Email Notification
<img width="1536" height="1024" alt="SNS Notification" src="https://github.com/user-attachments/assets/532a7ee8-3e2a-47e5-895f-c72fdbf601d9" />

DynamoDB Logs
<img width="1536" height="1024" alt="DynamoDB Logs" src="https://github.com/user-attachments/assets/84e9b8bc-5890-4f14-b81d-c9bff508f534" />

EventBridge Trigger
<img width="1366" height="768" alt="EventBridge Rule" src="https://github.com/user-attachments/assets/e4b4f42a-9fb9-4f1b-8456-5626ac31eed4" /> 

<img width="1366" height="768" alt="EventBridge Target" src="https://github.com/user-attachments/assets/043c0a3e-a592-4f18-afc8-83a2165b3949" />

Application Running in Docker Container
<img width="1366" height="727" alt="Application Output" src="https://github.com/user-attachments/assets/3748f55e-53c6-42a7-b8f5-3e17bff35c5d" />



---

# 📦 Deliverables

The project includes:

* Dockerfile
* Jenkinsfile
* Lambda Function Code
* GitHub Repository
* Architecture Diagram
* README Documentation
* Pipeline Execution Screenshots

---

# 📈 Benefits

* Fully automated Docker CI/CD pipeline
* Eliminates manual deployment
* Event-driven automation
* Real-time notifications
* Deployment history tracking

---

---

# ⭐ Conclusion

This project demonstrates how **Jenkins CI/CD pipelines can be integrated with AWS services to automate Docker image deployment and post-deployment automation using Lambda.**

The solution provides a scalable, automated, and event-driven DevOps workflow.
