pipeline {
    agent any

    environment {
        // Zmień nazwę obrazu na własne repozytorium (np. na Docker Hub)
        DOCKER_IMAGE = 'twojanazwa/simple-task-api'
        // ID poświadczeń (Credentials) skonfigurowanych w panelu Jenkinsa
        REGISTRY_CREDENTIALS_ID = 'dockerhub-credentials-id'
    }

    stages {
        // 1. Checkout kodu z repozytorium
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // 2. Instalacja zależności
        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }

        // 3. Uruchomienie testów
        stage('Run Tests') {
            steps {
                sh 'npm test'
            }
        }

        // 4. Budowanie aplikacji (opcjonalnie, jeśli projekt tego wymaga)
        stage('Build App') {
            steps {
                sh 'npm run build'
            }
        }

        // 5. Budowanie obrazu Docker
        stage('Build Docker Image') {
            steps {
                script {
                    // Tagowanie obrazu numerem builda oraz etykietą latest
                    sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        // 6. Publikowanie obrazu do rejestru Docker
        stage('Push Docker Image') {
            steps {
                // Pobieranie danych logowania z bezpiecznego magazynu Jenkinsa
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS_ID}", 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        // Logowanie do rejestru i wypchnięcie obrazów
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            // Opcjonalne czyszczenie workspace po zakończeniu builda
            cleanWs()
        }
        success {
            echo 'Pipeline zakończony pełnym sukcesem!'
        }
        failure {
            echo 'Pipeline napotkał błąd podczas wykonywania.'
        }
    }
}
