pipeline {
    agent any

    environment {
        MLFLOW_TRACKING_URI = 'http://localhost:5000'
    }

    stages {

        // 🎯 STAGE 1: Code Quality (isteğe bağlı)
        stage('Code Quality') {
            steps {
                script {
                    echo "🔍 Kod analizi başlıyor..."
                    sh 'python -m pylint pipelines/ --fail-under=7.0 || true'
                    sh 'python -m flake8 pipelines/ --max-line-length=120 || true'
                }
            }
        }

        // 🤖 STAGE 2: Regression Pipeline Çalıştırma
        stage('Run Regression Pipeline') {
            steps {
                script {
                    echo "🏋️‍♂️ Regression pipeline eğitiliyor..."
                    sh '''
                        export MLFLOW_TRACKING_URI=http://localhost:5000
                        python pipelines/regression_pipeline.py
                    '''
                }
            }
        }

        // 📊 STAGE 3: Model Validation (MLflow'dan kontrol)
        stage('Validate Model') {
            steps {
                script {
                    echo "📈 Model doğrulama başlıyor..."
                    sh '''
                        python -c "
from mlflow.tracking import MlflowClient

client = MlflowClient()
exp = client.get_experiment_by_name('regression_experiment')
if exp:
    runs = client.search_runs(
        [exp.experiment_id],
        order_by=['attributes.start_time DESC'],
        max_results=1
    )
    if runs:
        run = runs[0]
        r2 = run.data.metrics.get('test_r2', 0)
        print(f'✅ Son Regression R²: {r2}')
        if r2 < 0.7:
            print('🚨 R² çok düşük! Pipeline başarısız.')
            exit(1)
        else:
            print('🎉 Model validation başarılı!')
else:
    print('⚠️ Regression experiment bulunamadı!')
                        "
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "📧 Build tamamlandı - ${currentBuild.result}"
        }
        success {
            echo "🎉 Build başarılı!"
        }
        failure {
            echo "❌ Build başarısız!"
        }
    }
}
