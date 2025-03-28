import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load data
data = pd.read_csv('dataset.csv')

# Display current column names and data shape
print("Current columns:", data.columns.tolist())
print("Data shape:", data.shape)

# Convert date columns to datetime objects
try:
    data['job_card_date'] = pd.to_datetime(data['job_card_date'])
    data['purchase_date'] = pd.to_datetime(data['purchase_date'])
except KeyError:
    print("Warning: Could not find date columns. Proceeding without date features.")
    pass

# Create new features from dates
if 'job_card_date' in data.columns:
    data['feature_4'] = data['job_card_date'].dt.year
    data['feature_5'] = data['job_card_date'].dt.month
if 'purchase_date' in data.columns:
    data['feature_6'] = data['purchase_date'].dt.year
    data['feature_7'] = data['purchase_date'].dt.month

# Encode categorical variables only if they are object type
categorical_cols = [col for col in data.columns if data[col].dtype == 'object']
for col in categorical_cols:
    data[col] = data[col].astype(str)  # Convert to string to handle all categorical data uniformly
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])

# Handle missing values
data.fillna(0, inplace=True)

# Ensure all required features are present
required_features = [f'feature_{i}' for i in range(1, 11)]
for feature in required_features:
    if feature not in data.columns:
        data[feature] = 0

# Drop unnecessary columns
data = data[required_features]

# Save preprocessed data
data.to_csv('preprocessed_features.csv', index=False)

# Display final results
print("\nFinal features:")
print(data.columns.tolist())
print("Final data shape:", data.shape)