pipeline {
    agent any

    environment {
        DOCKER_USER = "sheikhnashid"
        VM_USER     = "ans1"
        PROD_IP     = "192.168.0.241"

        SSH_CREDS_ID    = "vm-deploy-key"
        DOCKER_CREDS_ID = "docker-hub-creds"

        TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.build("${DOCKER_USER}/voting-backend:${TAG}", "./backend")
                    docker.build("${DOCKER_USER}/voting-frontend:${TAG}", "./frontend")
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: DOCKER_CREDS_ID,
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                      echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                      docker push ${DOCKER_USER}/voting-backend:${TAG}
                      docker push ${DOCKER_USER}/voting-frontend:${TAG}
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                sshagent(credentials: [SSH_CREDS_ID]) {
                    sh """
                      scp docker-compose.yml ${VM_USER}@${PROD_IP}:/home/${VM_USER}/docker-compose.yml

                      ssh ${VM_USER}@${PROD_IP} << EOF
                        docker pull ${DOCKER_USER}/voting-backend:${TAG}
                        docker pull ${DOCKER_USER}/voting-frontend:${TAG}

                        export BACKEND_IMAGE=${DOCKER_USER}/voting-backend:${TAG}
                        export FRONTEND_IMAGE=${DOCKER_USER}/voting-frontend:${TAG}

                        docker compose down
                        docker compose up -d
                      EOF
                    """
                }
            }
        }
    }
}
