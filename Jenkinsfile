pipeline {
    agent any
    stages {
        stage("register flyte workflow"){
            steps{
                sh "pyflyte --config workflows/video_process/adminconfig.yaml run --remote workflows/video_process/video_process_with_monitoring.py --version ${BUILD_NUMBER}"
            }
        }
    }
}
