from zenml import pipeline
from steps.regression import (
    regression_model_trainer,
    regression_model_evaluator
)

@pipeline(enable_cache=False)
def regression_pipeline():
    """MLflow ile Regresyon Modeli Pipeline'ı - STEP ARTIFACT UYUMLU"""
    print(" REGRESYON PIPELINE BAŞLATILDI")
    print(" Model Train → MLflow Tracking → Evaluation")
    print("=" * 50)
    
    #  DATA DEPENDENCY İLE SIRALAMA
    print("1.  MODEL EĞİTİMİ BAŞLATILIYOR...")
    training_result = regression_model_trainer()
    
    print("2.  MODEL DEĞERLENDİRME BAŞLATILIYOR...")
    evaluation_result = regression_model_evaluator(training_result)
    
    print("=" * 50)
    print(" REGRESYON PIPELINE TAMAMLANDI!")
    print(" Model eğitildi ve değerlendirildi")
    print(" MLflow UI'de sonuçları kontrol et: http://localhost:5000")
    print("=" * 50)

if __name__ == "__main__":
    print(" DIRECT EXECUTE - REGRESYON PIPELINE")
    regression_pipeline()