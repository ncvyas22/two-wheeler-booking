pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                echo 'Building updated Docker image...'
                sh 'docker build -t twowheeler-cicd:latest .'
            }
        }

        stage('3. Project Manager Approval') {
            steps {
                script {
                    mail(
                        to: 'ncvyasjobs@gmail.com',
                        subject: "Approval Required: Two-Wheeler Build #${env.BUILD_NUMBER}",
                        body: """Hello Project Manager,

A new code change for the Two-Wheeler Booking App has been built and is waiting for your approval to deploy to production.

Review & Approve here:
${env.BUILD_URL}input/

Build Details:
- Job: ${env.JOB_NAME}
- Build #: ${env.BUILD_NUMBER}
"""
                    )

                    input(
                        message: 'Deploy Two-Wheeler App to Live Server?',
                        ok: 'Approve & Deploy',
                        submitterParameter: 'APPROVED_BY'
                    )
                }
            }
        }

        stage('4. Deploy Container') {
            steps {
                echo 'Deploying approved version on port 8098...'
                sh '''
                    docker rm -f twowheeler-cicd-app || true
                    docker run -d \
                      --name twowheeler-cicd-app \
                      --network twowheeler-net \
                      -p 8098:5000 \
                      twowheeler-cicd:latest
                '''
            }
        }
    }
}
