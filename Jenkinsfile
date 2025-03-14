pipeline {
    agent any  // Run the pipeline on any available agent
    environment {
        DOCKER_IMAGE = 'fruk196/django-simple-ecommerce:latest'  // Docker image name
        VENV_DIR = 'venv'  // Define the virtual environment directory
        K8S_PUBLIC_IP = '13.55.125.26'  // Kubernetes server IP
    }

    stages {
        stage('Checkout') {
            steps {
                 git branch: 'main', 
   		 credentialsId: '36680b80-065a-4bb4-83cc-9169b75719ea', 
   		 url: 'https://github.com/frukbutt196/Django-app-ecommerce.git'

            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Ensure Python 3 and venv are installed
                    sudo apt update && sudo apt install -y python3 python3-venv python3-pip libpq-dev

                    # Create and activate virtual environment
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate

                    # Upgrade pip and install dependencies
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Push to Docker Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sshagent(['your-ssh-credentials-id']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@${K8S_PUBLIC_IP} 'kubectl apply -f k8s/deployment.yaml'
                        ssh -o StrictHostKeyChecking=no ubuntu@${K8S_PUBLIC_IP} 'kubectl apply -f k8s/service.yaml'
                    '''
                }
            }
        }
    }
}
