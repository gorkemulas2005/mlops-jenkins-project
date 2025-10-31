pipeline {
    agent any

    environment {
        // 🔒 ZenML import karışıklığını engeller
        PYTHONPATH = "/usr/local/lib/python3.11/site-packages"
        VENV_NAME = ".venv_regression"
        MLFLOW_TRACKING_URI = "http://mlflow_ui:5000"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Checking out repository..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    echo "🚀 Setting up Python virtual environment..."
                    sh '''
                        set -euo pipefail
                        if [ ! -d "$VENV_NAME" ]; then
                            echo "🆕 Creating new venv..."
                            python3 -m venv $VENV_NAME
                        else
                            echo "♻️ Found existing venv at $VENV_NAME — reusing."
                        fi

                        . $VENV_NAME/bin/activate
                        echo "📦 Upgrading pip and core tools..."
                        $VENV_NAME/bin/pip install --upgrade pip setuptools wheel

                        echo "📚 Installing regression pipeline dependencies..."
                        $VENV_NAME/bin/pip install --force-reinstall \\
                            "zenml==0.74.0" \\
                            "mlflow==2.9.2" \\
                            "scikit-learn==1.3.2" \\
                            "pandas==1.5.3" \\
                            "numpy==1.24.3" \\
                            "matplotlib==3.7.2" \\
                            "joblib==1.3.2"
                    '''
                }
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                script {
                    echo "🏋️‍♂️ Running regression training pipeline..."
                    sh '''
                        set -e
                        . $VENV_NAME/bin/activate
                        python pipelines/regression_pipeline.py
                    '''
                }
            }
        }

        stage('Track in MLflow') {
            steps {
                script {
                    echo "📊 Tracking results in MLflow..."
                    sh '''
                        . $VENV_NAME/bin/activate
                        echo "MLflow UI: $MLFLOW_TRACKING_URI"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed — check console logs."
        }
        always {
            echo "📦 Archiving MLflow artifacts..."
            archiveArtifacts artifacts: '**/mlruns/**', allowEmptyArchive: true
        }
    }
}
