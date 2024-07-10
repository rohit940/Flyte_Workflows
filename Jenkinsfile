pipeline {
    agent any
    stages {
        stage("register flyte workflow"){
            steps{
                sh "pyflyte --config workflows/video_process/adminconfig.yaml register workflows/video_process/video_process_with_monitoring.py --version ${BUILD_NUMBER} --config_file workflows/video_process/config.yaml"
            }
        }
    }
}
