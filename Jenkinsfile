pipeline {
    agent any

    stages {
        stage('Run Regression Pipeline') {
            steps {
                echo 'Starting Regression Pipeline...'
                bat 'python -m zenml pipeline run regression_pipeline'
            }
        }

        stage('Evaluate Model') {
            steps {
                echo 'Evaluating model performance...'
                bat 'python evaluate.py'
            }
        }

        stage('Upload to MLflow') {
            steps {
                echo 'Logging results to MLflow...'
                bat 'python upload_to_mlflow.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
    }
}
