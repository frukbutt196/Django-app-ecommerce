pipeline {
    agent any  // Run the pipeline on any available agent
    environment {
        DOCKER_IMAGE = 'fruk196/django-simple-ecommerce:latest'  // Docker image name
        K8S_PUBLIC_IP = '13.55.125.26'  // Kubernetes server IP
    }
    stages {
        // Stage 1: Checkout the code
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/frukbutt196/Django-app-ecommerce.git'
            }
        }

        // Stage 2: Install Python dependencies
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        // Stage 3: Run tests
        stage('Run Tests') {
            steps {
                sh 'python manage.py test'
            }
        }

        // Stage 4: Build Docker image
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        // Stage 5: Push Docker image to Docker Hub
        stage('Push to Docker Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push ${DOCKER_IMAGE}'
                }
            }
        }

        // Stage 6: Deploy to Kubernetes
        stage('Deploy to Minikube') {
            steps {
                sshagent(['your-ssh-credentials-id']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${K8S_PUBLIC_IP} 'kubectl apply -f k8s/deployment.yaml'
                        ssh -o StrictHostKeyChecking=no ubuntu@${K8S_PUBLIC_IP} 'kubectl apply -f k8s/service.yaml'
                    """
                }
            }
        }
    }
}