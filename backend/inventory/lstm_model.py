import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import MinMaxScaler
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def train_lstm(file_path: str, window_size: int = 7, batch_size: int = 32,
                epochs: int = 50, units: int = 50) -> Sequential:
    """
    Train an LSTM model for product demand prediction.
    
    Args:
        file_path (str): Path to the Excel file containing historical sales data
        window_size (int): Number of previous time steps to use as input
        batch_size (int): Number of samples per gradient update
        epochs (int): Number of training epochs
        units (int): Number of LSTM units
        
    Returns:
        Sequential: Trained LSTM model
    """
    try:
        # Load and preprocess data
        logging.info("Loading data from Excel file")
        df = pd.read_excel(file_path)
        
        # Check for required columns
        required_columns = ['date', 'quantity_sold']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        # Convert date to datetime and sort
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Extract features and target
        features = df[['quantity_sold', 'price', 'promotion']]  # Add more features as needed
        target = df['quantity_sold']
        
        # Handle missing values
        features = features.fillna(0)
        
        # Normalize data
        logging.info("Normalizing data")
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_features = scaler.fit_transform(features)
        scaled_target = scaler.fit_transform(target.values.reshape(-1, 1))
        
        # Create time-series sequences
        logging.info("Creating time series sequences")
        def create_sequences(data: np.ndarray, target: np.ndarray, window_size: int):
            X, y = [], []
            for i in range(len(data) - window_size):
                X.append(data[i:i+window_size])
                y.append(target[i+window_size])
            return np.array(X), np.array(y)
        
        X, y = create_sequences(scaled_features, scaled_target, window_size)
        
        # Build LSTM model
        logging.info("Building LSTM model")
        model = Sequential()
        model.add(LSTM(units, activation='relu', input_shape=(X.shape[1], X.shape[2])))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        # Define callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('inventory/best_lstm_model.h5', save_best_only=True)
        
        # Train model
        logging.info("Training LSTM model")
        history = model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            callbacks=[early_stopping, model_checkpoint],
            verbose=1
        )
        
        # Save final model
        model.save('inventory/lstm_model.h5')
        
        # Log performance metrics
        logging.info(f"Best validation loss: {min(history.history['val_loss'])}")
        logging.info(f"Best validation MAE: {min(history.history['val_mae'])}")
        
        return model
        
    except Exception as e:
        logging.error(f"Error during model training: {str(e)}")
        raise