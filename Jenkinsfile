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
                    sh 'docker build --no-cache -t $DOCKER_CREDENTIALS_USR/$JOB_NAME:$BUILD_NUMBER .'
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'azure-registry') {
                        docker.image("$DOCKER_CREDENTIALS_USR/$JOB_NAME:$BUILD_NUMBER").push()
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