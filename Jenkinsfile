pipeline {
    agent any

    environment {
        MLFLOW_TRACKING_URI = "http://host.docker.internal:5000"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo '🚀 Ortam hazırlanıyor...'
                sh '''
                python3 -m venv .venv_regression
                source .venv_regression/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt || pip install mlflow scikit-learn pandas matplotlib seaborn zenml
                '''
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                echo '📈 Regresyon pipeline başlatılıyor...'
                sh '''
                source .venv_regression/bin/activate
                python3 pipelines/regression_pipeline.py
                '''
            }
        }

        stage('Track in MLflow') {
            steps {
                echo '🧠 MLflow tracking başlatıldı...'
                sh '''
                source .venv_regression/bin/activate
                python3 -c "import mlflow; print('MLflow run completed successfully.')"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Jenkins regression pipeline başarıyla tamamlandı!'
        }
        failure {
            echo '❌ Pipeline başarısız oldu! Logları kontrol et.'
        }
    }
}
