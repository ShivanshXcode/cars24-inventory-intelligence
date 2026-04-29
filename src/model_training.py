# src/model_training.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import xgboost as xgb
import pickle
import warnings
warnings.filterwarnings('ignore')

def train_models():
    # Load cleaned data
    df = pd.read_csv('data/cleaned_data.csv')
    
    # Features for price prediction
    price_features = [
        'year', 'km_driven', 'car_age', 
        'km_per_year', 'name_encoded',
        'fuel_encoded', 'transmission_encoded',
        'owner_encoded', 'seller_type_encoded'
    ]
    
    # Remove features that dont exist
    price_features = [f for f in price_features 
                      if f in df.columns]
    
    X_price = df[price_features]
    y_price = df['selling_price']
    y_days = df['days_to_sell']
    
    # Split data
    X_train, X_test, y_price_train, y_price_test, \
    y_days_train, y_days_test = train_test_split(
        X_price, y_price, y_days,
        test_size=0.2, random_state=42
    )
    
    print("Training Price Prediction Model...")
    
    # XGBoost for price prediction
    price_model = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=7,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbosity=0
    )
    price_model.fit(X_train, y_price_train)
    
    # Evaluate price model
    price_pred = price_model.predict(X_test)
    price_r2 = r2_score(y_price_test, price_pred)
    price_mae = mean_absolute_error(y_price_test, price_pred)
    
    print(f"Price Model R² Score: {price_r2:.4f}")
    print(f"Price Model MAE: ₹{price_mae:,.0f}")
    
    print("\nTraining Days-to-Sell Model...")
    
    # Random Forest for days to sell
    days_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    days_model.fit(X_train, y_days_train)
    
    # Evaluate days model
    days_pred = days_model.predict(X_test)
    days_r2 = r2_score(y_days_test, days_pred)
    days_mae = mean_absolute_error(y_days_test, days_pred)
    
    print(f"Days Model R² Score: {days_r2:.4f}")
    print(f"Days Model MAE: {days_mae:.1f} days")
    
    # Save models
    with open('models/price_model.pkl', 'wb') as f:
        pickle.dump(price_model, f)
    
    with open('models/days_model.pkl', 'wb') as f:
        pickle.dump(days_model, f)
    
    with open('models/features.pkl', 'wb') as f:
        pickle.dump(price_features, f)
    
    print("\nModels saved successfully!")
    
    return price_r2, price_mae, days_r2, days_mae

if __name__ == "__main__":
    import os
    os.makedirs('models', exist_ok=True)
    train_models()