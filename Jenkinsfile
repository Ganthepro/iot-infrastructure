pipeline {
    agent {
        node {
            label 'main-agent'
        }
    }

    triggers {
        pollSCM('* * * * *')
    }

    environment {
        DOCKER_CREDENTIALS = credentials('azure-registry')
    }

    stages {
        stage('Get Git Tag') {
            steps {
                script {
                    env.TAG_NAME = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
                    echo "Git Tag: ${env.TAG_NAME}"
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/data-logger:$TAG_NAME -f data_logger/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/iaq-sensor:$TAG_NAME -f iaq_sensor/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/api:$TAG_NAME -f api/Dockerfile .'
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://tamtikorn.azurecr.io', 'azure-registry') {
                        docker.image("$DOCKER_CREDENTIALS_USR/data-logger:$TAG_NAME").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/iaq-sensor:$TAG_NAME").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/api:$TAG_NAME").push()
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'echo y | docker system prune -a'
            cleanWs(cleanWhenNotBuilt: false,
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true,
                patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                           [pattern: '.propsfile', type: 'EXCLUDE']])
        }
    }
}