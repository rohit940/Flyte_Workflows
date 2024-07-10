pipeline {
    agent any
    stages {
        stage("ls"){
            steps{
                sh "cd workflows/CICD/ && pwd && pyflyte --config config.yml run --remote example.py wf"
            }
        }
    }
}
