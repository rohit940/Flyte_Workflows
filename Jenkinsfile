pipeline {
    agent any
    stages {
        stage("register flyte workflow"){
            steps{
                sh "pyflyte --config adminconfig.yaml run --remote video_process_with_monitoring.py monitoring_workflow_new_05 --config_file config.yaml"
                // sh "cat workflows/video_process/config.yaml"
                // sh "sudo pyflyte --config workflows/video_process/adminconfig.yaml register workflows/video_process/video_process_with_monitoring.py --version ${BUILD_NUMBER} "
            }
        }
    }
}
