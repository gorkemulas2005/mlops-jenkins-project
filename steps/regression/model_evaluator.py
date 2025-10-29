from zenml import step
from typing import Dict, Any
from typing_extensions import Annotated
import mlflow
import matplotlib.pyplot as plt
import tempfile
import os

@step(enable_cache=False)
def regression_model_evaluator(training_result: Dict[str, Any]) -> Annotated[Dict[str, float], "evaluation_results"]:
    """Modeli değerlendir - STEP ARTIFACT UYUMLU"""
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    import numpy as np
    import pandas as pd
    
    print(" MODEL DEĞERLENDİRME BAŞLADI...")
    
    #  STEP ARTIFACT'I DICT'E ÇEVİR
    print(" Step artifact işleniyor...")
    
    #  EĞER DIRECT DICT DEĞİLSE, VALUE ÖZELLİĞİNİ KULLAN
    if hasattr(training_result, 'value'):
        training_data = training_result.value
        print(" Step artifact .value ile açıldı")
    else:
        training_data = training_result
        print(" Direct dict kullanılıyor")
    
    #  TRAINING DATA'DAN RUN ID'Yİ AL
    run_id = training_data.get("run_id") if isinstance(training_data, dict) else None
    
    if not run_id:
        print(" Training result'ta run_id bulunamadı!")
        print(f" Training data: {training_data}")
        return {"error": "no_run_id"}
    
    print(f" Training Run ID: {run_id}")
    
    #  TEST VERİ SETİ
    test_data = {
        'feature1': [2.5, 5.5, 7.5],
        'feature2': [4.5, 7.5, 9.5], 
        'feature3': [6.5, 9.5, 11.5],
        'target': [32.5, 48.5, 58.5]
    }
    test_df = pd.DataFrame(test_data)
    
    X_test = test_df[['feature1', 'feature2', 'feature3']]
    y_test = test_df['target']
    
    #  MLflow'DAN MODELİ YÜKLE
    mlflow.set_experiment("regression_experiment")
    
    try:
        print(f" Model yükleniyor: runs:/{run_id}/regression_model")
        model_uri = f"runs:/{run_id}/regression_model"
        model = mlflow.sklearn.load_model(model_uri)
        print(" Model başarıyla yüklendi!")
        
        #  PREDICTIONS
        y_pred = model.predict(X_test)
        
        #  METRİKLER
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f" Test Metrikleri: R²={r2:.4f}, RMSE={rmse:.4f}")
        
        #  YENİ EVALUATION RUN OLUŞTUR
        with mlflow.start_run(run_name="evaluation_run"):
            # METRİKLER
            mlflow.log_metric("test_mse", mse)
            mlflow.log_metric("test_rmse", rmse) 
            mlflow.log_metric("test_mae", mae)
            mlflow.log_metric("test_r2", r2)
            mlflow.log_metric("test_samples", len(X_test))
            
            # PARAMETERS
            mlflow.log_param("evaluation_dataset", "test_set")
            mlflow.log_param("training_run_id", run_id)
            mlflow.log_param("model_source", "direct_from_training")
            
            # TAGS
            mlflow.set_tag("project", "regression_demo")
            mlflow.set_tag("task_type", "regression")
            mlflow.set_tag("evaluation", "true")
            mlflow.set_tag("pipeline", "zenml_regression_fixed")
            
            #  GÖRSELLER
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Actual vs Predicted
                plt.figure(figsize=(10, 6))
                plt.scatter(y_test, y_pred, alpha=0.7, color='blue', s=100)
                plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=3)
                plt.xlabel('Gerçek Değerler')
                plt.ylabel('Tahmin Edilen Değerler')
                plt.title(f'Gerçek vs Tahmin (R² = {r2:.4f})')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                
                plot_path = os.path.join(tmp_dir, "actual_vs_predicted.png")
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                mlflow.log_artifact(plot_path, "evaluation_plots")
                plt.close()
                
                # Residual Plot
                plt.figure(figsize=(10, 6))
                residuals = y_test - y_pred
                plt.scatter(y_pred, residuals, alpha=0.7, color='green', s=100)
                plt.axhline(y=0, color='r', linestyle='--', lw=3)
                plt.xlabel('Tahmin Edilen Değerler')
                plt.ylabel('Hatalar (Residuals)')
                plt.title('Hata Dağılımı - Residual Plot')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                
                residual_path = os.path.join(tmp_dir, "residual_plot.png")
                plt.savefig(residual_path, dpi=300, bbox_inches='tight')
                mlflow.log_artifact(residual_path, "evaluation_plots")
                plt.close()
            
            print(" EVALUATION RUN BAŞARIYLA OLUŞTURULDU!")
            print(f" Test R²: {r2:.4f}")
            print(f" Test RMSE: {rmse:.4f}")
            
            results = {
                "test_mse": mse,
                "test_rmse": rmse,
                "test_mae": mae, 
                "test_r2": r2,
                "training_run_id": run_id
            }
            
            return results
            
    except Exception as e:
        print(f" Model değerlendirme hatası: {e}")
        return {"error": str(e)}