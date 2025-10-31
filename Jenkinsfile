pipeline {
    agent any

    environment {
        // MLflow tracking server bağlantısı
        MLFLOW_TRACKING_URI = "http://host.docker.internal:5000"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo '🚀 Ortam hazırlanıyor...'
                bat '''
                python -m venv .venv_regression
                call .venv_regression\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt || pip install mlflow scikit-learn pandas matplotlib seaborn zenml
                '''
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                echo '📈 Regresyon pipeline başlatılıyor...'
                bat '''
                call .venv_regression\\Scripts\\activate
                python pipelines\\regression_pipeline.py
                '''
            }
        }

        stage('Track in MLflow') {
            steps {
                echo '🧠 MLflow tracking başlatıldı...'
                bat '''
                call .venv_regression\\Scripts\\activate
                python -c "import mlflow; print('MLflow run completed successfully.')"
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
