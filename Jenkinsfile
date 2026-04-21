pipeline {
    agent any

    environment {
        // Permanent model storage on Jenkins host — copy tb_model.pth here ONCE manually
        MODEL_STORE = 'C:\\jenkins-models\\tb_model.pth'
        MODEL_DEST  = "${WORKSPACE}\\ai-service\\models\\tb_model.pth"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Divyansh010605/tb-detection-capstone---Copy.git'
            }
        }

        stage('Stop Old Containers') {
            steps {
                bat 'docker compose -p tb-detection down'
            }
        }

        stage('Prepare Model') {
            steps {
                script {
                    bat "if not exist \"%WORKSPACE%\\ai-service\\models\" mkdir \"%WORKSPACE%\\ai-service\\models\""

                    def result = bat(
                        script: "@if exist \"${env.MODEL_STORE}\" (echo EXISTS) else (echo MISSING)",
                        returnStdout: true
                    ).trim()

                    if (result.contains('EXISTS')) {
                        echo "Model found — copying to workspace..."
                        bat "copy /Y \"${env.MODEL_STORE}\" \"${env.MODEL_DEST}\""
                    } else {
                        error "Model not found at ${env.MODEL_STORE}. Run once as Admin: copy tb_model.pth to C:\\jenkins-models\\"
                    }
                }
            }
        }

        stage('Start Mongo') {
            steps {
                bat 'docker compose -p tb-detection up -d mongo'
            }
        }

        stage('Build AI Service') {
            steps {
                bat 'docker compose -p tb-detection up -d --build ai-service'
            }
        }

        stage('Build Backend') {
            steps {
                bat 'docker compose -p tb-detection up -d --build backend'
            }
        }

        stage('Build Frontend') {
            steps {
                bat 'docker compose -p tb-detection up -d --build frontend'
            }
        }

        stage('Clean Up Space') {
            steps {
                bat 'docker image prune -f'
            }
        }

        stage('Fetch Ngrok URL') {
            steps {
                powershell '''
                $response = Invoke-RestMethod -Uri 'http://127.0.0.1:4040/api/tunnels' -ErrorAction SilentlyContinue
                if ($response) {
                    Write-Host "========================================================"
                    Write-Host "DEPLOYMENT SUCCESSFUL!"
                    Write-Host "Your app is live at: $($response.tunnels[0].public_url)"
                    Write-Host "========================================================"
                } else {
                    Write-Host "Could not fetch URL. Is Ngrok running on port 3000?"
                }
                '''
            }
        }
    }
}
