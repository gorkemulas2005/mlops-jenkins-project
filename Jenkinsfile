pipeline {
  agent any

  environment {
    VENV_DIR = ".venv_regression"
    PYTHON = "${VENV_DIR}/bin/python"
    PIP = "${VENV_DIR}/bin/pip"
    MLFLOW_TRACKING_URI = "http://mlflow_ui:5000" // compose içindeki mlflow servis adını buraya yaz
    // Eğer farklı servis adı kullanıyorsan üstteki satırı değiştir
  }

  options {
  //  ansiColor('xterm')
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python (venv)') {
      steps {
        script {
          // use bash -lc to ensure 'source' works and consistent shell
          sh '''
            set -euo pipefail
            echo ">>> Using bash to setup venv"
            if [ ! -d "${VENV_DIR}" ]; then
              echo "Creating venv at ${VENV_DIR}..."
              python3 -m venv "${VENV_DIR}"
            else
              echo "Found existing venv at ${VENV_DIR} — reusing."
            fi

            # Activate in POSIX-compatible way (works in bash -lc)
            . "${VENV_DIR}/bin/activate"

            # upgrade pip inside venv
            ${PIP} install --upgrade pip setuptools wheel

            # If requirements.txt exists, prefer it
            if [ -f "requirements.txt" ]; then
              echo "Installing from requirements.txt"
              ${PIP} install -r requirements.txt
            else
              echo "No requirements.txt - installing fallback pinned packages"
              # Replace / add the exact versions you want here.
              # If zenml wheel is included in repo (./wheels/zenml-0.74.0.whl), pip will find it.
              if [ -f "wheels/zenml-0.74.0-py3-none-any.whl" ]; then
                echo "Found local zenml wheel, installing that..."
                ${PIP} install wheels/zenml-0.74.0-py3-none-any.whl
              else
                echo "No local zenml wheel found. Trying to install zenml==0.74.0 from PyPI (may fail if not available)."
                ${PIP} install "zenml==0.74.0" || echo "zenml 0.74 not available on PyPI - skip"
              fi

              # Install the rest (these are examples based on your list — edit if needed)
              ${PIP} install "mlflow==2.9.2" "scikit-learn==1.3.2" "pandas==1.5.3" "numpy==1.24.3" "matplotlib==3.7.2" "joblib==1.3.2" || echo "Some packages failed to install — check logs"
            fi

            # sanity checks
            echo "Python: $(${PYTHON} --version || echo 'missing')"
            echo "Pip: $(${PIP} --version || echo 'missing')"
          '''
        }
      }
    }

    stage('Run Regression Pipeline') {
      steps {
        script {
          sh '''
            set -euo pipefail
            . "${VENV_DIR}/bin/activate"
            export MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI}"
            echo "MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI"
            # run your script (fail loudly on error)
            ${PYTHON} pipelines/regression_pipeline.py
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Pipeline succeeded"
    }
    failure {
      echo "❌ Pipeline failed - check console output"
      archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
    }
  }
}
