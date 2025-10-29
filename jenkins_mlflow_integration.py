import subprocess
import sys
import mlflow

def run_jenkins_pipeline():
    print("🚀 Jenkins + MLflow Entegrasyonu Başlıyor...")
    
    # MLflow tracking URI ayarla
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("jenkins_integration")
    
    with mlflow.start_run():
        # Pipeline'ı çalıştır
        try:
            result = subprocess.run([
                "python", "pipelines/regression_pipeline.py"
            ], capture_output=True, text=True, check=True)
            
            # Başarılı ise MLflow'a kaydet
            mlflow.log_param("pipeline", "regression")
            mlflow.log_metric("status", 1)
            mlflow.log_text(result.stdout, "pipeline_output.txt")
            print("✅ Pipeline başarıyla çalıştı!")
            
        except subprocess.CalledProcessError as e:
            # Hata durumunda MLflow'a kaydet
            mlflow.log_param("pipeline", "regression")
            mlflow.log_metric("status", 0)
            mlflow.log_text(e.stderr, "error_output.txt")
            print(f"❌ Pipeline hatası: {e}")
            sys.exit(1)

if __name__ == "__main__":
    run_jenkins_pipeline()