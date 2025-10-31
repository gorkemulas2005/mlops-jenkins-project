pipeline {
    agent any

    environment {
        PYTHON_VER = "3.11"
        VENV_DIR = ".venv_regression"
        GITHUB_REPO = "https://github.com/gorkemulas2005/mlops-jenkins-project.git"
        BRANCH = "main"
        CREDENTIALS_ID = "github-token"
    }

    stages {

        stage('Checkout') {
            steps {
                echo " Checking out repository..."
                git branch: "${BRANCH}", url: "${GITHUB_REPO}", credentialsId: "${CREDENTIALS_ID}"
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo " Setting up Python environment..."
                sh '''
                set -e
                if [ -d ${VENV_DIR} ]; then
                    rm -rf ${VENV_DIR}
                fi

                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate

                pip install --upgrade pip setuptools wheel
                pip install zenml==0.91.0 mlflow==2.13.2 scikit-learn==1.3.2 pandas==1.5.3 numpy==1.24.3 matplotlib==3.7.2 joblib==1.3.2 packaging==24.1
                '''
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                echo " Running MLflow Regression Pipeline..."
                sh '''
                . ${VENV_DIR}/bin/activate
                python run_fatih_terim.py || python3 run_fatih_terim.py
                '''
            }
        }

        stage('Track in MLflow') {
            steps {
                echo " Verifying MLflow logs..."
                sh '''
                . ${VENV_DIR}/bin/activate
                if [ -d "mlruns" ]; then
                    echo " MLflow tracking successful! Artifacts logged:"
                    ls -R mlruns | head -30
                else
                    echo " No mlruns directory found — check MLflow tracking configuration."
                    exit 1
                fi
                '''
            }
        }
    }

    post {
        success {
            echo " Pipeline completed successfully — Regression and MLflow tracking OK!"
        }
        failure {
            echo " Pipeline failed — Check console logs."
        }
    }
}
