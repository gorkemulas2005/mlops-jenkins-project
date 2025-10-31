stage('Run Regression Pipeline') {
    steps {
        script {
            echo "🏋️‍♂️ Regression pipeline eğitiliyor (python:3.11 container)..."
            sh '''
                docker run --rm \
                  -v "$PWD":/workspace \
                  -w /workspace \
                  python:3.11 bash -lc "
                    python -m pip install --upgrade pip &&
                    pip install mlflow scikit-learn numpy pandas matplotlib seaborn &&
                    export MLFLOW_TRACKING_URI=http://host.docker.internal:5000 &&
                    python pipelines/regression_pipeline.py
                  "
            '''
        }
    }
}
