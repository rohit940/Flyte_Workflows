pipeline {
    agent any
    stages {
        stage('Prepare') {
            steps {
                script {
                    // Ensure that the workspace contains the required files
                    sh 'ls -l /var/lib/jenkins/workspace/flytee/workflows/video_process/config.yaml'
                }
            }
        stage("register flyte workflow"){
            steps{
                // sh "pyflyte --config  workflows/video_process/adminconfig.yaml run --remote  workflows/video_process/video_process_with_monitoring.py monitoring_workflow_new_05 --config_file  workflows/video_process/config.yaml"
                // sh "cat workflows/video_process/config.yaml"
                sh "pyflyte --config workflows/video_process/adminconfig.yaml register workflows/video_process/video_process_with_monitoring.py --version ${BUILD_NUMBER} "
            }
        }
    }
}
