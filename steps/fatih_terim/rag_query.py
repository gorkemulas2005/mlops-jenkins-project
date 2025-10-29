from zenml import step
from typing import Dict, Any, List
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_rag_query() -> Annotated[Dict[str, Any], "rag_results"]:
    """RAG QUERY SİSTEMİ"""
    print(" RAG QUERY SİSTEMİ - BAŞLADI")
    
    try:
        from llm_engineering.infrastructure.db.qdrant import QdrantDatabaseConnector
        from sentence_transformers import SentenceTransformer
        
        print(" Model ve Qdrant bağlantısı yükleniyor...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        qdrant_client = QdrantDatabaseConnector()
        print(" Bağlantılar hazır")
        
        test_questions = [
            "Fatih Terim hangi takımlarda teknik direktörlük yaptı?",
            "Fatih Terim'in Galatasaray'daki başarıları neler?",
            "Fatih Terim milli takımda ne yaptı?",
            "Fatih Terim'in taktik anlayışı nasıl?",
            "Fatih Terim hangi ödülleri kazandı?"
        ]
        
        all_results = []
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n [{i}/{len(test_questions)}] Soru: '{question}'")
            
  
            query_vector = model.encode([question])[0].tolist()
            
            
            search_results = qdrant_client.search(
                collection_name="fatih_terim_articles",
                query_vector=query_vector,
                limit=3
            )
            
            question_results = {
                "question": question,
                "results": [],
                "best_match_score": 0
            }
            
            for j, hit in enumerate(search_results, 1):
                score = hit.score
                payload = hit.payload
                
                question_results["results"].append({
                    "rank": j,
                    "score": round(score, 4),
                    "title": payload.get("title", "Başlık Yok"),
                    "text": payload.get("text", "İçerik Yok")
                })
                
                if score > question_results["best_match_score"]:
                    question_results["best_match_score"] = score
                
                print(f"    {j}. Sonuç: {payload.get('title', 'Başlık Yok')[:50]}...")
                print(f"       Benzerlik: {round(score * 100, 2)}%")
            
            all_results.append(question_results)
            print(f"    {len(search_results)} sonuç bulundu")
        
        # İSTATİSTİKLER
        total_results = sum(len(result["results"]) for result in all_results)
        avg_score = sum(result["best_match_score"] for result in all_results) / len(all_results)
        
        print(f"\n RAG QUERY TAMAMLANDI!")
        print(f" Toplam: {len(test_questions)} soru, {total_results} sonuç")
        print(f" Ortalama benzerlik: {round(avg_score * 100, 2)}%")
        
        return {
            "rag_query_status": "success",
            "questions_tested": len(test_questions),
            "total_results": total_results,
            "average_score": round(avg_score, 4),
            "results": all_results
        }
        
    except Exception as e:
        error_msg = f" RAG Query hatası: {e}"
        print(error_msg)
        return {"rag_query_status": "error", "error": str(e)}