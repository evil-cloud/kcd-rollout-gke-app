// Pipeline version: v1.1.6
pipeline {
    agent { label 'jenkins-jenkins-agent' }
    environment {
        IMAGE_NAME      = "d4rkghost47/gitops-api-gke"
        REGISTRY        = "https://index.docker.io/v1/"
        SHORT_SHA       = "${GIT_COMMIT[0..7]}"
        SONAR_PROJECT   = "gitops-api"
        SONAR_SOURCE    = "src"
        SONAR_HOST      = "http://sonarqube-sonarqube.sonarqube.svc.cluster.local:9000"
        TRIVY_HOST      = "http://trivy.trivy-system.svc.cluster.local:4954"
        TZ              = "America/Guatemala"  
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    logInfo("CHECKOUT", "Starting code checkout...")
                    checkout scm
                    logSuccess("CHECKOUT", "Code checkout completed.")
                }
            }
        }

        stage('Build Image') {
            steps {
                container('dind') {
                    script {
                        logInfo("BUILD", "Building Docker image...")
                        try {
                            sh '''
                            docker build --no-cache -t ${IMAGE_NAME}:${SHORT_SHA} .
                            docker tag ${IMAGE_NAME}:${SHORT_SHA} ${IMAGE_NAME}:latest
                            '''
                            logSuccess("BUILD", "Build completed.")
                        } catch (Exception e) {
                            logFailure("BUILD", "Docker build failed: ${e.message}")
                            error("Stopping pipeline due to build failure.")
                        }
                    }
                }
            }
        }
    

        stage('Push Image') {
            steps {
                container('dind') {
                    script {
                        withCredentials([string(credentialsId: 'docker-token', variable: 'DOCKER_TOKEN')]) {
                            logInfo("PUSH", "Uploading Docker image...")
                            try {
                                sh '''
                                echo "$DOCKER_TOKEN" | docker login -u "d4rkghost47" --password-stdin > /dev/null 2>&1
                                docker push ${IMAGE_NAME}:${SHORT_SHA}
                                docker push ${IMAGE_NAME}:latest
                                '''
                                logSuccess("PUSH", "Image pushed successfully.")
                            } catch (Exception e) {
                                logFailure("PUSH", "Docker push failed: ${e.message}")
                                error("Stopping pipeline due to push failure.")
                            }
                        }
                    }
                }
            }
        }

    }

    post {
        success {
            logSuccess("PIPELINE", "Pipeline completed successfully.")
        }
        failure {
            logFailure("PIPELINE", "Pipeline failed.")
        }
    }
}

def logInfo(stage, message) {
    echo "[${stage}] [INFO] ${getTimestamp()} - ${message}"
}

def logSuccess(stage, message) {
    echo "[${stage}] [SUCCESS] ${getTimestamp()} - ${message}"
}

def logFailure(stage, message) {
    echo "[${stage}] [FAILURE] ${getTimestamp()} - ${message}"
}

def getTimestamp() {
    return sh(script: "TZ='America/Guatemala' date '+%Y-%m-%d %H:%M:%S'", returnStdout: true).trim()
}

