# src/data_preprocessing.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    
    print("Original shape:", df.shape)
    print("Columns:", df.columns.tolist())
    
    # Clean column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Drop missing values
    df = df.dropna()
    
    # Feature engineering
    df['car_age'] = 2024 - df['year']
    df['km_per_year'] = df['kms_driven'] / (df['car_age'] + 1)
    df['price_per_km'] = df['selling_price'] / (df['kms_driven'] + 1)
    
    # Simulate days_to_sell based on car features
    # (In real Cars24, this comes from their database)
    np.random.seed(42)
    base_days = 30
    
    # Older cars take longer to sell
    df['days_to_sell'] = (
        base_days +
        df['car_age'] * 2 +
        (df['kms_driven'] / 10000) -
        (df['selling_price'] / 100000) * 5 +
        np.random.normal(0, 5, len(df))
    ).clip(7, 120).astype(int)
    
    # Encode categorical variables
    le_dict = {}
    cat_cols = ['name', 'fuel', 'seller_type', 
                'transmission', 'owner']
    
    for col in cat_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(
                df[col].astype(str))
            le_dict[col] = le
    
    print("Cleaned shape:", df.shape)
    return df, le_dict

if __name__ == "__main__":
    df, encoders = load_and_clean_data('data/car data/car data.csv')
    df.to_csv('data/cleaned_data.csv', index=False)
    print("Data saved successfully!")
    print(df.head())