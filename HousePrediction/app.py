import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the API application
app = FastAPI()

# 1. Load your saved pipeline files from disk
model = pickle.load(open("saved_models/house_model.pkl", "rb"))
scaler = pickle.load(open("saved_models/scaler.pkl", "rb"))

# CRITICAL: Load the label encoders to translate text names into numbers!
label_encoders = pickle.load(open("saved_models/label_encoders.pkl", "rb"))

# 2. Define the new user-friendly JSON schema (Accepting Strings!)
class HouseFeatures(BaseModel):
    area_type: str        # e.g., "Super built-up  Area"
    size: int             # e.g., 2 or 3 (BHK count)
    total_sqft: float     # e.g., 1200.0
    bath: float           # e.g., 2.0
    balcony: float        # e.g., 1.0
    site_location: str    # e.g., "Kharadi" or "Wakad"

@app.post("/predict")
def predict_price(features: HouseFeatures):
    try:
        # 3. Dynamic Text-to-Number Translation (Label Encoding Lookups)
        # This converts "Super built-up  Area" -> 2 and "Kharadi" -> 25 automatically!
        encoded_area = label_encoders["area_type"].transform([features.area_type])[0]
        encoded_location = label_encoders["site_location"].transform([features.site_location])[0]
        
    except ValueError as e:
        # If the user types a location name that doesn't exist in our dataset, throw a clear error
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid text entry provided. Error: {str(e)}"
        )

    # 4. Map the newly encoded numbers into our Pandas DataFrame format
    data_dict = {
        "area_type": [encoded_area],
        "size": [features.size],
        "total_sqft": [features.total_sqft],
        "bath": [features.bath],
        "balcony": [features.balcony],
        "site_location": [encoded_location]
    }
    
    input_df = pd.DataFrame(data_dict)
    
    # 5. Run standard scaling and prediction operations
    scaled_data = scaler.transform(input_df)
    prediction = model.predict(scaled_data)
    
    return {"predicted_price": float(prediction[0])}

if __name__ == "__main__":
    import uvicorn
    print("Launching Embedded Uvicorn Server with Text Mapping Active...")
    uvicorn.run(app, host="127.0.0.1", port=8000)