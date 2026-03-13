pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ACCOUNT_ID = '718383533665'
        REPO_NAME = 'docker-ecr-jenkins-project'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Pull Code') {
            steps {
                git 'https://github.com/Nikitapatil0304/docker-ecr-jenkins-project.git '
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

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION |
                docker login --username AWS --password-stdin \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
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
