pipeline {
    agent any

    environment {
        VENV_DIR = ".venv_regression"
        MLFLOW_TRACKING_URI = "http://mlflow_ui:5000"
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    sh '''
                        set -euo pipefail
                        echo "🚀 Setting up Python virtual environment..."

                        if [ ! -d "$VENV_DIR" ]; then
                            python3 -m venv "$VENV_DIR"
                        else
                            echo "Found existing venv at $VENV_DIR — reusing."
                        fi

                        . "$VENV_DIR/bin/activate"

                        echo "📦 Upgrading pip and core tools..."
                        "$VENV_DIR/bin/pip" install --upgrade pip setuptools wheel

                        echo "📚 Installing regression pipeline dependencies..."
                        "$VENV_DIR/bin/pip" install --force-reinstall \
                            zenml==0.74.0 \
                            mlflow==3.0.0 \
                            scikit-learn==1.3.2 \
                            pandas==1.5.3 \
                            numpy==1.24.3 \
                            matplotlib==3.7.2 \
                            joblib==1.3.2

                        echo "✅ Python Environment Ready!"
                        "$VENV_DIR/bin/python" --version
                        "$VENV_DIR/bin/pip" --version
                    '''
                }
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                script {
                    sh '''
                        set -euo pipefail
                        echo "🏋️‍♂️ Running Regression Pipeline..."
                        . "$VENV_DIR/bin/activate"

                        export MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
                        echo "MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI"

                        "$VENV_DIR/bin/python" pipelines/regression_pipeline.py
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "📦 Archiving MLflow artifacts..."
            archiveArtifacts artifacts: '**/mlruns/**', allowEmptyArchive: true
        }
        success {
            echo "✅ Pipeline finished successfully!"
        }
        failure {
            echo "❌ Pipeline failed - check console logs."
        }
    }
}
