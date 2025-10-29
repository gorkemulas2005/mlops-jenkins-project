from zenml import step
import pandas as pd
from typing import Tuple
from typing_extensions import Annotated

@step(enable_cache=False)
def multimodal_data_loader() -> Tuple[
    Annotated[pd.DataFrame, "train_data"],
    Annotated[pd.DataFrame, "test_data"]
]:
    """Step 1: Data Loading"""
    print(" STEP 1: DATA LOADER ÇALIŞIYOR...")
    
    data = {
        'label': [0, 1, 0, 1, 0, 1, 0, 1],
        'image': ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg', 'img6.jpg', 'img7.jpg', 'img8.jpg'],
        'text': ['kedi sevimli', 'köpek sadık', 'kedi miyavlar', 'köpek havlar', 'kedi temiz', 'köpek oyun', 'kedi uyur', 'köpek koşar'],
        'feature1': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
        'feature2': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    }
    
    df = pd.DataFrame(data)
    train_df = df.iloc[:6]
    test_df = df.iloc[6:]
    
    print(f" Veri hazır: {len(train_df)} train, {len(test_df)} test")
    return train_df, test_df