from zenml import step
from typing import Dict, Any
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_mongo_loader() -> Annotated[Dict[str, Any], "mongo_results"]:  # ✅ INPUT YOK
    """Fatih Terim MongoDB"""
    print(" FATİH TERIM MONGO LOADER - BAŞLADI")
    
    # Bu step artık bağımsız çalışacak
    # Test verisi oluştur
    test_data = [
        {
            'title': 'Fatih Terim Galatasaray Başarıları',
            'url': 'https://example.com/fatih-terim-1',
            'snippet': 'Fatih Terim Galatasaray ile birçok şampiyonluk yaşadı',
            'query': 'Fatih Terim',
            'timestamp': '2024-01-01T00:00:00',
            'content': 'Fatih Terim Galatasaray teknik direktörü olarak birçok başarıya imza attı.'
        }
        # Diğer test verileri...
    ]
    
    try:
        from llm_engineering.domain.documents import ArticleDocument, UserDocument
        
    
        user_data = {
            'first_name': 'Fatih',
            'last_name': 'Terim_Crawler', 
            'full_name': 'Fatih_Terim_Crawler'
        }
        user = UserDocument(**user_data)
        user.save()
        
        
        saved_count = 0
        for data in test_data:
            article = ArticleDocument(
                content={
                    'title': data['title'],
                    'content': data['content'],
                    'snippet': data['snippet']
                },
                platform='web_crawl',
                author_full_name='Fatih_Terim_Crawler',
                author_id=user.id,
                link=data['url'],
                metadata={
                    'query': data['query'],
                    'crawl_date': data['timestamp'],
                    'project': 'fatih_terim_analysis'
                }
            )
            article.save()
            saved_count += 1
        
        print(f" {saved_count} test verisi MongoDB'ye kaydedildi")
        return {"status": "success", "count": saved_count}
        
    except Exception as e:
        print(f" MongoDB hatası: {e}")
        return {"status": "error", "error": str(e)}