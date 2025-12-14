pipeline {
    agent { label 'php-agent' }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                dir('lab05/php-app') {
                    sh 'composer install --no-interaction --prefer-dist'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running PHPUnit tests...'
                dir('lab05/php-app') {
                    sh 'php vendor/bin/phpunit --testdox'
                }
            }
        }
    }

    post {
        always {
            echo 'pipeline completed.'
        }
        success {
            echo 'all tests passed successfully!'
        }
        failure {
            echo 'tests failed.'
        }
    }
}
