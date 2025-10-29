from zenml import pipeline
from steps.multimodal.data_loader import multimodal_data_loader
from steps.multimodal.model_trainer import automm_model_trainer  
from steps.multimodal.model_evaluator import automm_model_evaluator

@pipeline(enable_cache=False)
def multimodal_pipeline():
    """AutoMM Multimodal Pipeline"""
    print("=" * 60)
    print(" AUTOGLUON MULTIMODAL PIPELINE BAŞLADI")
    print(" MLflow + AutoMM + ZenML Steps")
    print("=" * 60)
    
    train_data, test_data = multimodal_data_loader()  #Tuple unpacking
    model = automm_model_trainer(train_data)
    accuracy = automm_model_evaluator(model, test_data)
    
    print("=" * 60)
    print(" AUTOGLUON PIPELINE TAMAMLANDI!")
    print(f" Accuracy: {accuracy}")
    print(" MLflow UI: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    multimodal_pipeline()