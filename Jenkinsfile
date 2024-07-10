pipeline {
    agent any
    stages {
        stage("execute flyte workflow"){
            steps{
                sh "pyflyte --config workflows/CICD/config.yaml run --remote workflows/CICD/example.py wf"
                sh "ls"
            }
        }
    }
}
