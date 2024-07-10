pipeline {
    agent any
    stages {
        stage("register flyte workflow"){
            steps{
                // sh "cat workflows/video_process/config.yaml"
                sh "pyflyte --config workflows/video_process/adminconfig.yaml register workflows/video_process/video_process_with_monitoring.py --version ${BUILD_NUMBER} "
            }
        }
    }
}
