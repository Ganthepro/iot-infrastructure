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
        stage('Build') {
            steps {
                script {
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/data-logger:$BUILD_NUMBER -f data_logger/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/data-logger:latest -f data_logger/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/iaq-sensor:$BUILD_NUMBER -f iaq_sensor/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/iaq-sensor:latest -f iaq_sensor/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/api:$BUILD_NUMBER -f api/Dockerfile .'
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/api:latest -f api/Dockerfile .'
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://tamtikorn.azurecr.io', 'azure-registry') {
                        docker.image("$DOCKER_CREDENTIALS_USR/data-logger:$BUILD_NUMBER").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/data-logger:latest").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/iaq-sensor:$BUILD_NUMBER").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/iaq-sensor:latest").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/api:$BUILD_NUMBER").push()
                        docker.image("$DOCKER_CREDENTIALS_USR/api:latest").push()
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