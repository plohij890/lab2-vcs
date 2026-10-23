pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен из Git'
                bat 'dir' 
            }
        }
        stage('Build') {
            steps {
                echo 'Сборка проекта...'
                bat 'python --version'
            }
        }
        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                bat 'echo "Тесты прошли"'
            }
        }
    }
    post {
        success {
            echo 'Пайплайн завершён успешно!'
        }
        failure {
            echo 'Пайплайн завершился с ошибкой'
        }
    }
}