from zenml import step
from typing import Dict, Any
from typing_extensions import Annotated
import mlflow
import mlflow.sklearn

@step(enable_cache=False)
def regression_model_trainer() -> Annotated[Dict[str, Any], "training_results"]:
    """Regresyon modelini train eder - RUN ID DÖNDÜRÜR"""
    from sklearn.ensemble import RandomForestRegressor
    import pandas as pd
    
    print(" MODEL EĞİTİMİ BAŞLADI...")
    
    #  VERİ SETİ
    data = {
        'feature1': [1.2, 2.1, 3.2, 4.1, 5.3, 6.2, 7.1, 8.3],
        'feature2': [3.4, 4.3, 5.1, 6.2, 7.1, 8.3, 9.2, 10.1],
        'feature3': [5.6, 6.5, 7.8, 8.9, 9.2, 10.1, 11.3, 12.4],
        'target': [25.8, 30.2, 35.6, 40.3, 45.7, 50.4, 55.8, 60.2]
    }
    df = pd.DataFrame(data)
    
    X = df[['feature1', 'feature2', 'feature3']]
    y = df['target']
    
    #  MLflow TRACKING
    mlflow.set_experiment("regression_experiment")
    
    with mlflow.start_run(run_name="training_run") as run:
        print(" Training run oluşturuldu...")
        
        # MODEL EĞİT
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        print(" Model eğitiliyor...")
        model.fit(X, y)
        
        # PARAMETERS
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("dataset_size", len(X))
        
        # MODEL KAYDET
        print(" Model MLflow'a kaydediliyor...")
        mlflow.sklearn.log_model(model, "regression_model")
        
        # METRİKLER
        train_score = model.score(X, y)
        mlflow.log_metric("train_r2", train_score)
        
        # RUN ID'Yİ AL
        run_id = run.info.run_id
        
        print(f" Model eğitildi - Train R²: {train_score:.4f}")
        print(f" Run ID: {run_id}")
        
        return {
            "status": "success",
            "train_r2": train_score,
            "run_id": run_id,
            "model_type": "RandomForestRegressor"
        }