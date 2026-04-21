pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose'
        NODE_ENV = 'production'
    }

    stages {
        stage('Setup') {
            steps {
                echo 'Installing dependencies across all services...'
                sh 'cd backend && npm install'
                sh 'cd frontend && npm install'
                sh 'cd ai-service && pip install -r requirements.txt'
            }
        }

        stage('Lint & Quality') {
            steps {
                echo 'Running code quality checks...'
                sh 'cd backend && npm run lint || true'
                sh 'cd ai-service && flake8 . || true'
            }
        }

        stage('Unit Testing') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        sh 'cd backend && npm test'
                    }
                }
                stage('AI Service Tests') {
                    steps {
                        sh 'cd ai-service && pytest'
                    }
                }
            }
        }

        stage('Model Verification') {
            steps {
                echo 'Verifying AI Model weights...'
                sh 'python -c "import torch; torch.load(\'ai-service/models/tb_model.pth\', map_location=\'cpu\')"'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker Images...'
                sh "${DOCKER_COMPOSE} build"
            }
        }

        stage('Deployment') {
            steps {
                echo 'Deploying to staging/production...'
                sh "${DOCKER_COMPOSE} up -d"
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Pipeline Failed. Checking logs...'
        }
    }
}
