pipeline {
    agent any
    stages {
        stage('Print Build Number') {
            steps {
                echo "Current build number is: ${BUILD_NUMBER}"
            }
        }
        stage("execute flyte workflow"){
            steps{
                sh "cd workflows/CICD/ && pwd && pyflyte --config config.yaml run --remote example.py wf"
            }
        }
    }
}
