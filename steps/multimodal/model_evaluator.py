from zenml import step
import pandas as pd
from typing import Any
from typing_extensions import Annotated
import mlflow

@step(enable_cache=False)
def automm_model_evaluator(
    model: Any,
    test_data: pd.DataFrame
) -> Annotated[float, "accuracy"]:
    """Step 3: Model Evaluation"""
    print(" STEP 3: MODEL EVALUATOR ÇALIŞIYOR...")
    
    if model is None:
        print(" Model yok - değerlendirme atlanıyor")
        return 0.0
    
    try:
        predictions = model.predict(test_data)
        accuracy = float((predictions == test_data['label']).mean())
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("test_samples", len(test_data))
        
        print(f" Değerlendirme Sonuçları:")
        print(f"    Accuracy: {accuracy}")
        print(f"    Test samples: {len(test_data)}")
        
        return accuracy
        
    except Exception as e:
        print(f" Değerlendirme hatası: {e}")
        return 0.0