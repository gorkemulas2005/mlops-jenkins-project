from zenml import step
from datetime import datetime
from typing import Dict, Any
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_vectorizer() -> Annotated[Dict[str, Any], "vector_results"]:
    """TAM RAG SİSTEMİ - TEST VERİLERİ İLE"""
    print(" TAM RAG VECTORIZER - BAŞLADI")
    
    try:
        from llm_engineering.infrastructure.db.qdrant import QdrantDatabaseConnector
        from sentence_transformers import SentenceTransformer
        
        print(" Embedding modeli yükleniyor...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print(" Embedding modeli yüklendi")
        
        # TEST VERİLERİ - 20 kayıt
        test_texts = [
            "Fatih Terim Galatasaray başarıları ve şampiyonlukları",
            "Fatih Terim milli takım teknik direktörlüğü kariyeri",
            "Fatih Terim İtalya'da Milan ve Fiorentina deneyimleri", 
            "Fatih Terim oyun sistemi ve taktik dehası",
            "Fatih Terim disiplin anlayışı ve yönetim tarzı",
            "Fatih Terim genç yetenekleri geliştirme becerisi",
            "Fatih Terim transfer politikaları ve oyuncu seçimleri",
            "Fatih Terim Avrupa kupalarındaki başarıları",
            "Fatih Terim basın toplantıları ve açıklamaları",
            "Fatih Terim futbol felsefesi ve vizyonu",
            "Fatih Terim Türk futboluna katkıları ve etkisi",
            "Fatih Terim başarı hikayesi ve kariyer yolculuğu",
            "Fatih Terim oyuncu ilişkileri ve yıldız oyuncularla çalışması",
            "Fatih Terim taktik değişiklikleri ve maç yönetimi",
            "Fatih Terim şampiyonlukları ve kupaları",
            "Fatih Terim liderlik özellikleri ve karizması",
            "Fatih Terim antrenman metodları ve hazırlık süreçleri",
            "Fatih Terim futbolcu gelişim programları",
            "Fatih Terim Galatasaray efsanesi ve mirası",
            "Fatih Terim Türk futbol tarihindeki yeri"
        ]
        
        print(f" {len(test_texts)} test metni embedding'e dönüştürülüyor...")
        
        # Embedding oluştur - TÜM TEST VERİLERİ
        embeddings = model.encode(test_texts)
        print(f" {len(embeddings)} embedding oluşturuldu")
        
        # Qdrant'a kaydet
        qdrant_client = QdrantDatabaseConnector()
        
        # Collection önce oluştur
        collection_name = "fatih_terim_articles"
        
        try:
            from qdrant_client.http import models
            qdrant_client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=len(embeddings[0]),
                    distance=models.Distance.COSINE
                )
            )
            print(f" Collection oluşturuldu: {collection_name}")
        except Exception as e:
            print(f" Collection zaten var: {collection_name}")
        

        points = []
        for i, (text, embedding) in enumerate(zip(test_texts, embeddings)):
            points.append({
                'id': i,
                'vector': embedding.tolist(),
                'payload': {
                    'text': text,
                    'title': f"Fatih Terim Konu {i+1}",
                    'source': 'fatih_terim_test_rag',
                    'timestamp': datetime.now().isoformat(),
                    'content': f"{text}. Bu konu Fatih Terim'in kariyeri ve başarıları hakkında detaylı bilgiler içermektedir."
                }
            })
        

        print(f" {len(points)} vektör Qdrant'a yükleniyor...")
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        result_msg = f" {len(points)} vektör Qdrant'a yüklendi (TAM RAG HAZIR!)"
        print(result_msg)
        
        return {
            "rag_status": "success", 
            "vectors_uploaded": len(points),
            "total_documents": len(test_texts),
            "collection": collection_name,
            "embedding_dim": len(embeddings[0])
        }
        
    except Exception as e:
        error_msg = f" RAG Vectorizer hatası: {e}"
        print(error_msg)
        return {"rag_status": "error", "error": str(e)}