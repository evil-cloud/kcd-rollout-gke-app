// Pipeline version: v1.1.9
pipeline {
    agent { label 'jenkins-jenkins-agent' }
    environment {
        IMAGE_NAME      = "d4rkghost47/gitops-api-gke-sec"
        REGISTRY        = "https://index.docker.io/v1/"
        SHORT_SHA       = "${GIT_COMMIT[0..7]}"
        SONAR_PROJECT   = "gitops-api-gke-sec"
        SONAR_SOURCE    = "src"
        SONAR_HOST      = "http://sonarqube-sonarqube.sonarqube.svc.cluster.local:9000"
        TRIVY_HOST      = "http://trivy.trivy-system.svc.cluster.local:4954"
        TZ              = "America/Guatemala"  
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                            extensions: [[$class: 'CleanBeforeCheckout']],
                            userRemoteConfigs: [[url: 'https://github.com/evil-cloud/kcd-rollout-app.git']]])
                }
            }
        }

        stage('Test and Analysis') {
            parallel {
                stage('Static Code Analysis') {
                    steps {
                        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                            sh '''
                            sonar-scanner \\
                                -Dsonar.projectKey=${SONAR_PROJECT} \\
                                -Dsonar.sources=${SONAR_SOURCE} \\
                                -Dsonar.host.url=${SONAR_HOST} \\
                                -Dsonar.login=$SONAR_TOKEN
                            '''
                        }
                    }
                }

                stage('Unit Tests') {
                    steps {
                        container('dind') {
                            sh '''
                            docker build -t ${IMAGE_NAME}-test -f docker/Dockerfile.test.pipeline .
                            docker run --rm ${IMAGE_NAME}-test
                            '''
                        }
                    }
                }
            }
        }

        stage('Build Image') {
            steps {
                container('dind') {
                    sh '''
                    export DOCKER_BUILDKIT=1
                    docker build -f docker/Dockerfile.pipeline -t ${IMAGE_NAME}:${SHORT_SHA} .
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                container('dind') {
                    withCredentials([string(credentialsId: 'docker-token', variable: 'DOCKER_TOKEN')]) {
                        sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "d4rkghost47" --password-stdin > /dev/null 2>&1
                        docker push ${IMAGE_NAME}:${SHORT_SHA}
                        '''
                    }
                }
            }
        }

        stage('Scan Image') {
            steps {
                sh '''
                trivy image --server ${TRIVY_HOST} ${IMAGE_NAME}:${SHORT_SHA} --severity HIGH,CRITICAL --quiet
                '''
            }
        }
    }
}