pipeline {
    agent { label 'ansible-agent' }

    stages {
        stage('checkout') {
            steps {
                echo 'cloning ansible repository...'
                checkout scm
            }
        }

        stage('setup testest server') {
            steps {
                echo 'Configuring test server with Ansible...'
                dir('lab05/ansible') {
                    sh 'ansible-playbook -i hosts.ini setup_test_server.yml -v'
                }
            }
        }
    }

    post {
        always {
            echo 'ansible setup pipeline completed.'
        }
        success {
            echo 'test server configured successfully!'
        }
        failure {
            echo 'test server setup failed.'
        }
    }
}
