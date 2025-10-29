#!/usr/bin/env python3
"""
Fatih Terim Crawler - Run Script
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from pipelines.fatih_terim_crawler import fatih_terim_crawling_pipeline

def main():
    print("🚀 FATİH TERIM CRAWLER BAŞLATILIYOR...")
    
    try:
        # Pipeline'ı oluştur ve çalıştır
        pipeline_instance = fatih_terim_crawling_pipeline()
        pipeline_instance.run()
        
        print("🎉 PIPELINE BAŞARIYLA TAMAMLANDI!")
        
    except Exception as e:
        print(f"❌ PIPELINE HATASI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()