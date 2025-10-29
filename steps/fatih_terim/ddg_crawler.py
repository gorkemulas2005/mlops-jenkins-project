from zenml import step
from datetime import datetime
import time
import pandas as pd
from typing import List, Dict, Any
from typing_extensions import Annotated

@step(enable_cache=False)
def fatih_terim_ddg_crawler() -> Annotated[List[Dict[str, Any]], "search_results"]:
    """GERÇEK FATİH TERIM CRAWLER(Ornek)"""
    print(" GERÇEK FATİH TERIM CRAWLER - BAŞLADI")
    
   
    QUERIES = [
        "Fatih Terim", "imparator Fatih Terim", "Fatih Terim röportaj",
        "Fatih Terim Galatasaray", "Fatih Terim milli takım", "Fatih Terim Al Shabab",
        "Fatih Terim açıklaması", "Fatih Terim maç sonu", "Fatih Terim basın toplantısı",
        "Fatih Terim dava", "Fatih Terim itiraf", "Fatih Terim transfer",
        "Fatih Terim Netflix", "Fatih Terim UEFA", "Fatih Terim başarıları",
        "Fatih Terim sözleri", "Fatih Terim Bodrum", "Fatih Terim ailesi",
        "Fatih Terim fon davası", "Fatih Terim beIN Sports", "Fatih Terim TRT Spor",
        "Fatih Terim Hürriyet", "Fatih Terim Milliyet", "Fatih Terim Fanatik",
        "Fatih Terim Milan", "Fatih Terim Fiorentina", "Fatih Terim AC Milan", 
        "Fatih Terim İtalya", "Fatih Terim Euro 1996", "Fatih Terim Euro 2000",
        "Fatih Terim Euro 2008", "Fatih Terim Euro 2016", "Fatih Terim Dünya Kupası",
        "Fatih Terim Arda Turan", "Fatih Terim Hakan Şükür", "Fatih Terim Sneijder",
        "Fatih Terim Drogba", "Fatih Terim Muslera", "Fatih Terim Icardi",
        "Fatih Terim kavga", "Fatih Terim ceza", "Fatih Terim disiplin kurulu",
        "Fatih Terim Selçuk İnan", "Fatih Terim Şampiyonlar Ligi",
        "Fatih Terim lig şampiyonluğu", "Fatih Terim ayrılık", "Fatih Terim geri dönüş",
        "Fatih Terim İmparator belgeseli", "Fatih Terim kariyeri",
        "Fatih Terim anıları", "Fatih Terim en iyi sözleri",
        *[f"Fatih Terim {yil}" for yil in range(1996, 2025)]
    ]
    
    all_results = []
    
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        
        print(f" {len(QUERIES)} query ile arama başlatılıyor...")
        
        for i, query in enumerate(QUERIES[:10]):  # Önce 10 query ile test
            print(f" [{i+1}/{len(QUERIES[:10])}] Aranıyor: '{query}'")
            
            try:
                
                time.sleep(15)  # 15 saniye bekle
                
                results = list(ddgs.text(keywords=query, max_results=20))  
                
                for result in results:
                    all_results.append({
                        'title': result.get("title", ""),
                        'url': result.get("href", ""),
                        'snippet': result.get("body", ""),
                        'query': query,
                        'timestamp': datetime.now().isoformat(),
                        'content': f"{result.get('title', '')}. {result.get('body', '')}"
                    })
                
                print(f" '{query}' için {len(results)} sonuç bulundu")
                print(f" Toplam: {len(all_results)} veri")
                
            except Exception as e:
                print(f" '{query}' hatası: {e}")
                continue
        
        if all_results:
            print(f" BAŞARILI! {len(all_results)} gerçek veri bulundu")
            return all_results
        else:
            print(" DDG çalışmadı, geniş test verisi kullanılıyor...")
            # Geniş test verisi - 20+ kayıt
            return _create_test_data()
        
    except Exception as e:
        print(f" DDG hatası: {e}")
        return _create_test_data()

def _create_test_data() -> List[Dict[str, Any]]:
    """Geniş test verisi oluştur"""
    test_data = []
    
    # 20+ test kaydı
    test_records = [
        {"title": "Fatih Terim Galatasaray Başarıları", "topic": "başarı"},
        {"title": "Fatih Terim Milli Takım Kariyeri", "topic": "milli takım"},
        {"title": "Fatih Terim Teknik Direktörlük", "topic": "kariyer"},
        {"title": "Fatih Terim İtalya Deneyimi", "topic": "yurtdışı"},
        {"title": "Fatih Terim Röportajları", "topic": "röportaj"},
        {"title": "Fatih Terim Sözleri ve Felsefesi", "topic": "sözler"},
        {"title": "Fatih Terim Oyun Sistemi", "topic": "taktik"},
        {"title": "Fatih Terim ve Galatasaray", "topic": "kulüp"},
        {"title": "Fatih Terim Efsane Maçlar", "topic": "maçlar"},
        {"title": "Fatih Terim Disiplin Anlayışı", "topic": "disiplin"},
        {"title": "Fatih Terim Genç Yetenekler", "topic": "altyapı"},
        {"title": "Fatih Terim Transferleri", "topic": "transfer"},
        {"title": "Fatih Terim ve Avrupa Kupaları", "topic": "avrupa"},
        {"title": "Fatih Terim Basın Toplantıları", "topic": "basın"},
        {"title": "Fatih Terim Futbol Felsefesi", "topic": "felsefe"},
        {"title": "Fatih Terim ve Türk Futbolu", "topic": "türk futbolu"},
        {"title": "Fatih Terim Başarı Hikayesi", "topic": "biyografi"},
        {"title": "Fatih Terim ve Oyuncu İlişkileri", "topic": "oyuncular"},
        {"title": "Fatih Terim Taktik Dehası", "topic": "taktik"},
        {"title": "Fatih Terim ve Şampiyonluklar", "topic": "şampiyonluk"}
    ]
    
    for i, record in enumerate(test_records):
        test_data.append({
            'title': record["title"],
            'url': f'https://example.com/fatih-terim-{i}',
            'snippet': f'{record["title"]} hakkında detaylı bilgi.',
            'query': 'Fatih Terim',
            'timestamp': datetime.now().isoformat(),
            'content': f'{record["title"]}. Fatih Terim {record["topic"]} konusunda önemli başarılara imza atmıştır. Detaylı analiz ve bilgiler burada bulunabilir.'
        })
    
    print(f" {len(test_data)} test verisi oluşturuldu")
    return test_data