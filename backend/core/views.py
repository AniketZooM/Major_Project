from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Defer model loading to avoid circular imports
Inventory = apps.get_model('core', 'Inventory')
Vehicle = apps.get_model('core', 'Vehicle')
Transaction = apps.get_model('core', 'Transaction')

def home(request):
    return render(request, 'home.html')

def get_forecast(request):
    if request.method == 'GET':
        try:
            # Load the LSTM model
            model = load_model('backend/inventory/lstm_model.h5')
            
            # Create a scaler object for inverse transformation
            scaler = MinMaxScaler(feature_range=(0, 1))
            
            # Dummy data for fitting the scaler - replace with your actual training data
            dummy_data = np.array([[0], [100]])  # Example range of your quantity_sold
            scaler.fit(dummy_data)
            
            # Placeholder for actual forecasting logic
            forecast = [0]  # Replace with actual forecast values
            
            return JsonResponse({'forecast': forecast}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)