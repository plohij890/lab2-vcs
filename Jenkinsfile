pipeline {
    agent any
    
    environment {
        PROJECT_NAME = 'lab2-vcs'
        PYTHON_VERSION = '3.11'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "Клонирование проекта ${env.PROJECT_NAME}..."
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                echo 'Установка зависимостей...'
                bat 'python -m pip install -r requirements.txt || exit 0'
            }
        }
        stage('Lint') {
            steps {
                echo 'Статический анализ...'
                bat 'python -m pip install flake8'
                bat 'python -m flake8 . || exit 0'
            }
        }
        stage('Test') {
            steps {
                echo 'Запуск тестов...'
                bat 'python -m pip install pytest'
                bat 'python -m pytest test_backup.py'
            }
        }
        stage('Archive') {
            steps {
                echo 'Сохранение артефакта...'
                bat 'if not exist artifacts mkdir artifacts'
                bat 'echo Build %BUILD_NUMBER% > artifacts\\build.txt'
                archiveArtifacts artifacts: 'artifacts/**', allowEmptyArchive: true
            }
        }
    }
    post {
        always {
            echo "Pipeline завершён. Номер сборки: ${env.BUILD_NUMBER}"
        }
        success {
            echo 'Все этапы прошли успешно!'
        }
        failure {
            echo 'Один из этапов завершился с ошибкой'
        }
    }
}