import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ------------------------------------------
# Helper Functions for Data Cleaning
# ------------------------------------------
def convert_sqft(value):
    try:
        if "-" in str(value):
            lo, hi = str(value).split("-")
            return (float(lo) + float(hi)) / 2
        return float(value)
    except:
        return np.nan

def extract_bhk(x):
    try:
        return int(str(x).split()[0])
    except:
        return 0

# ------------------------------------------
# Main Production Pipeline Execution
# ------------------------------------------
if __name__ == "__main__":
    
    # 1. Load dataset
    print("[1/6] Loading raw dataset...")
    df = pd.read_csv(r"G:/PYTHON/HousePrediction/Pune_House_Data.csv")

    # 2. Clean total_sqft
    print("[2/6] Cleaning data features...")
    df["total_sqft"] = df["total_sqft"].apply(convert_sqft)
    df.dropna(subset=["total_sqft"], inplace=True)

    # -----------------------------------------------------------------
    # CODE UPGRADE: Remove Extreme Outliers (Focus on typical homes)
    # This keeps square footage between 350 and 5000, and price under 500 Lakhs (5 Crore)
    # -----------------------------------------------------------------
    df = df[(df["total_sqft"] >= 350) & (df["total_sqft"] <= 5000)]
    df = df[(df["price"] > 10) & (df["price"] <= 500)]

    # 3. Handle missing numeric and text fields
    df["bath"].fillna(df["bath"].median(), inplace=True)
    df["balcony"].fillna(df["balcony"].median(), inplace=True)

    df["size"].fillna("Unknown", inplace=True)
    df["site_location"].fillna("Unknown", inplace=True)

    # 4. Convert size to numeric BHK
    df["size"] = df["size"].apply(extract_bhk)

    # -----------------------------------------------------------------
    # CODE UPGRADE: Drop 'society' & 'availability' columns to remove noise
    # -----------------------------------------------------------------
    df.drop(columns=["society", "availability"], inplace=True, errors="ignore")

    # 5. Encode remaining categorical columns
    print("[3/6] Encoding categorical variables...")
    cat_cols = ["area_type", "site_location"] # Reduced columns
    label_encoders = {}

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # 6. Separate Features and Target
    X = df.drop("price", axis=1)
    y = df["price"]

    # 7. Split data into Train and Test sets (80/20)
    print("[4/6] Splitting data into Train and Test subsets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 8. Feature Scaling
    print("[5/6] Standardizing data scales...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 9. Model Training — Random Forest Regressor
    print("[6/6] Training the Random Forest ensemble model...")
    model = RandomForestRegressor(n_estimators=300, random_state=42)
    model.fit(X_train, y_train)

    # 10. Evaluation Performance Output
    y_pred = model.predict(X_test)
    print("\n==========================================")
    print("        UPDATED MODEL PERFORMANCE METRICS")
    print("==========================================")
    print("Mean Absolute Error MAE :", mean_absolute_error(y_test, y_pred))
    print("R-Squared / Coefficient of Determination R2 :", r2_score(y_test, y_pred))
    print("==========================================\n")

    # 11. Serialize and Export Pipeline Artifacts
    print("Saving model deployment files safely to disk...")
    os.makedirs("saved_models", exist_ok=True)
    
    with open("saved_models/house_model.pkl", "wb") as f:
        pickle.dump(model, f)
        
    with open("saved_models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
        
    with open("saved_models/label_encoders.pkl", "wb") as f:
        pickle.dump(label_encoders, f)
        
    print("Pipeline compilation complete! Saved inside folder: /saved_models")