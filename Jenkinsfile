pipeline {
    agent any

    environment {
        VENV_DIR = ".venv_regression"
        PYTHON = "python3"
    }

    stages {

        stage('Pre-clean') {
            steps {
                echo " Cleaning previous environments and residual ZenML modules..."
                sh '''
                    set -e
                    rm -rf ${VENV_DIR}
                    find . -type d -name "zenml" -exec rm -rf {} +
                '''
            }
        }

        stage('Checkout') {
            steps {
                echo " Checking out repository..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    echo " Setting up Python virtual environment..."
                    sh '''
                        set -euo pipefail

                        # Create venv
                        ${PYTHON} -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate

                        # Ensure Python path points inside venv
                        export PYTHONPATH="${VENV_DIR}/lib/python3.11/site-packages"

                        echo " Upgrading pip and base tools..."
                        ${VENV_DIR}/bin/pip install --upgrade pip setuptools wheel

                        echo " Installing compatible dependencies..."
                        ${VENV_DIR}/bin/pip install \
                            zenml==0.91.0 \
                            mlflow==2.13.2 \
                            packaging==24.1 \
                            scikit-learn==1.3.2 \
                            pandas==1.5.3 \
                            numpy==1.24.3 \
                            matplotlib==3.7.2 \
                            joblib==1.3.2
                    '''
                }
            }
        }

        stage('Verify Dependencies') {
            steps {
                echo " Verifying ZenML and MLflow versions..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python -c "import zenml, mlflow; print(f' ZenML {zenml.__version__} | MLflow {mlflow.__version__}')"
                '''
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                echo " Running regression pipeline..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    export PYTHONPATH="${VENV_DIR}/lib/python3.11/site-packages"
                    python run_fatih_terim.py
                '''
            }
        }

        stage('Track in MLflow') {
            steps {
                echo " Logging results to MLflow..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    export MLFLOW_TRACKING_URI="file:./mlruns"
                    echo " MLflow tracking directory set to ./mlruns"
                '''
            }
        }
    }

    post {
        success {
            echo " Pipeline completed successfully!"
            archiveArtifacts artifacts: 'mlruns/**/*', fingerprint: true
        }
        failure {
            echo " Pipeline failed — check console logs."
            archiveArtifacts artifacts: 'mlruns/**/*', allowEmptyArchive: true
        }
    }
}
