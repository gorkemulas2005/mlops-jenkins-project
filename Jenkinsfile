pipeline {
    agent any

    environment {
        MLFLOW_TRACKING_URI = "http://mlflow_ui:5000"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo '🚀 Ortam hazırlanıyor...'
                sh '''
                    # Sanal ortam oluştur
                    python3 -m venv .venv_regression
                    . .venv_regression/bin/activate

                    # pip upgrade ve bağımlılıklar
                    pip install --upgrade pip
                    pip install -r requirements.txt || true

                    echo "✅ Python ortamı hazır"
                '''
            }
        }

        stage('Run Regression Pipeline') {
            steps {
                echo '🏋️‍♂️ Regression pipeline eğitiliyor...'
                sh '''
                    . .venv_regression/bin/activate
                    export MLFLOW_TRACKING_URI=http://mlflow_ui:5000
                    python pipelines/regression_pipeline.py
                '''
            }
        }

        stage('Track in MLflow') {
            steps {
                echo '📈 MLflow’a metrikler kaydediliyor...'
                sh '''
                    echo "MLflow URI: $MLFLOW_TRACKING_URI"
                    echo "Run kayıtları MLflow arayüzünde görüntülenebilir."
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline başarıyla tamamlandı!'
        }
        failure {
            echo '❌ Pipeline başarısız oldu! Logları kontrol et.'
        }
    }
}
