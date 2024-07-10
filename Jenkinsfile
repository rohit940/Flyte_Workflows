pipeline {
    agent any
    stages {
        stage("git checkout"){
            steps{
                sh "git clone https://github.com/AnimelaAsif/Jenkins_monitoring.git"
            }
        }
        stage("ls"){
            steps{
                sh "ls -lah"
            }
        }
    }
}
