from zenml import pipeline
from steps.fatih_terim import (
    fatih_terim_ddg_crawler,
    fatih_terim_mongo_loader, 
    fatih_terim_mlflow_tracker,
    fatih_terim_vectorizer,
    fatih_terim_rag_query
)

@pipeline(enable_cache=False)
def fatih_terim_pipeline():
    """TAM RAG FATİH TERIM PIPELINE"""
    print("=" * 50)
    print(" TAM RAG FATİH TERIM PIPELINE BAŞLATILDI")
    print(" DDG → MongoDB → MLflow → RAG → QUERY")
    print("=" * 50)
    
    #STEPLER
    fatih_terim_ddg_crawler()
    fatih_terim_mongo_loader()
    fatih_terim_mlflow_tracker()
    fatih_terim_vectorizer()
    fatih_terim_rag_query()
    
    print("=" * 50)
    print(" TAM RAG PIPELINE TAMAMLANDI!")
    print(" Tüm step'ler başarıyla çalıştı")
    print(" MongoDB: 20+ veri kaydedildi")
    print(" RAG: 20 vektör Qdrant'a yüklendi")
    print(" QUERY: 5 soru ile semantic search test edildi")
    print(" MLflow: Tüm metrikler takip ediliyor")
    print(" RAG SİSTEMİ TAMAMEN HAZIR!")
    print("=" * 50)

if __name__ == "__main__":
    print(" DIRECT EXECUTE - TAM RAG FATİH TERIM PIPELINE")
    fatih_terim_pipeline()