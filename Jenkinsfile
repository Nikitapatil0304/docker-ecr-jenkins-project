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
                echo "Pulling code from GitHub..."
                git branch: 'main', url: 'https://github.com/Nikitapatil0304/docker-ecr-jenkins-project.git'
            }
        }

        stage('Verify Workspace') {
            steps {
                echo "Current workspace directory:"
                sh 'pwd'
                echo "Listing all files/folders in workspace:"
                sh 'ls -la'
                // Optional: check if app folder exists
                sh '''
                if [ ! -d "app" ]; then
                    echo "ERROR: app/ folder missing in workspace!"
                    exit 1
                fi
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh '''
                docker build -t $REPO_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Tag Image') {
            steps {
                echo "Tagging Docker image for ECR..."
                sh '''
                docker tag $REPO_NAME:$IMAGE_TAG \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                echo "Logging into ECR..."
                sh '''
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Push Image') {
            steps {
                echo "Pushing Docker image to ECR..."
                sh '''
                docker push \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG
                '''
            }
        }

    }
}
