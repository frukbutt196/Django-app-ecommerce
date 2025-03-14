pipeline {
    agent any  // Run the pipeline on any available agent
    
    environment {
        DOCKER_IMAGE = 'fruk196/django-simple-ecommerce:latest'  // Docker image name
        VENV_DIR = 'venv'  // Virtual environment directory
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
                    # Ensure system dependencies are installed
                    sudo apt update && sudo apt install -y python3 python3-venv python3-pip libpq-dev

                    # Set up virtual environment
                    python3 -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate

                    # Upgrade pip and install dependencies
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-django
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    pytest --ds=ecom.settings --verbosity=2 --junitxml=pytest.xml
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    dockerImage = docker.build(DOCKER_IMAGE)
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials') {
                        sh "docker push $DOCKER_IMAGE"
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }
    }
}
