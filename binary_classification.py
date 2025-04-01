import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# Load the trained model
model = joblib.load('model.joblib')

# Load the prediction data
data = pd.read_csv('Spare_Parts_Data.csv')

# Define the mapping from actual column names to expected feature names
feature_mapping = {
    'business_partner_name': 'feature_0',
    'current_km_reading': 'feature_1',
    'invoice_date': 'feature_2',
    'invoice_line_text': 'feature_3',
    'job_card_date': 'feature_4',
    'part_description': 'feature_5',
    'quantity': 'feature_6',
    'unit_price': 'feature_7',
    'total_amount': 'feature_8',
    'purchase_date': 'feature_9'
}

# Create a DataFrame with the expected feature names using the actual data
feature_data = data[feature_mapping.keys()].copy()
feature_data = feature_data.rename(columns=feature_mapping)

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(feature_data)

# Make predictions
try:
    predictions = model.predict(data_scaled)
    print("Predictions:")
    print(predictions)
except Exception as e:
    print(f"An error occurred during prediction: {str(e)}")