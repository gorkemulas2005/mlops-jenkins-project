from zenml import step
import pandas as pd
from typing import Any
from typing_extensions import Annotated
import mlflow

@step(enable_cache=False)
def automm_model_trainer(
    train_data: pd.DataFrame
) -> Annotated[Any, "trained_model"]:
    """Step 2: Model Training"""
    print(" STEP 2: MODEL TRAINER ÇALIŞIYOR...")
    
    try:
        from autogluon.multimodal import MultiModalPredictor
        print(" AutoGluon yüklü - eğitime başlanıyor...")
    except ImportError as e:
        print(f" AutoGluon yüklü değil: {e}")
        return None
    
   
    mlflow.set_experiment("autogluon_multimodal")
    
    with mlflow.start_run(run_name="automm_baseline"):
        mlflow.log_param("model_type", "AutoMM")
        mlflow.log_param("time_limit", 120)
        mlflow.log_param("label_column", "label")
        
       
        predictor = MultiModalPredictor(
            label="label",
            problem_type="binary"
        )
        
        print(" AutoMM modeli eğitiliyor...")
        predictor.fit(
            train_data=train_data,
            time_limit=120,
            presets="medium_quality" 
        )
        
        mlflow.log_metric("training_samples", len(train_data))
        mlflow.set_tag("project", "autogluon_demo")
        
        print(" Model eğitildi ve MLflow'a kaydedildi")
        return predictor