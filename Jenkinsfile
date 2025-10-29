pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Environment') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y python3 python3-pip
                    pip3 install mlflow pandas scikit-learn matplotlib seaborn
                '''
            }
        }
        stage('Run ML Pipeline') {
            steps {
                sh '''
                    export MLFLOW_TRACKING_URI=http://localhost:5000
                    python3 pipelines/regression_pipeline.py
                '''
            }
        }
    }
}
