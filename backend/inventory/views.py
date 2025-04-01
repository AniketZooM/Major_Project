from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Inventory
from .serializers import InventorySerializer
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Load the pre-trained LSTM model
model = load_model('backend/inventory/lstm_model.h5')

# Create a scaler object for inverse transformation
scaler = MinMaxScaler(feature_range=(0, 1))

# Dummy data for fitting the scaler - replace with your actual training data
dummy_data = np.array([[0], [100]])  # Example range of your quantity_sold
scaler.fit(dummy_data)

class InventoryListView(APIView):
    def get(self, request):
        items = Inventory.objects.all()
        serializer = InventorySerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        if not file.name.endswith(('.xlsx', '.csv')):
            return Response({'error': 'Invalid file format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)  # or pd.read_csv(file) if it's a CSV

            # --- Data Preprocessing ---
            # 1. Handle missing values (fill with 0 or a more appropriate strategy)
            df = df.fillna(0)

            # 2. Ensure required columns are present
            required_columns = ['date', 'part_id', 'quantity_sold']
            if not all(col in df.columns for col in required_columns):
                return Response({'error': 'Missing required columns (date, part_id, quantity_sold)'}, status=status.HTTP_400_BAD_REQUEST)

            # 3. Convert 'date' to datetime
            df['date'] = pd.to_datetime(df['date'])

            # 4. Normalize 'quantity_sold' (using the pre-fitted scaler)
            df['quantity_sold_normalized'] = scaler.transform(df[['quantity_sold']])

            # 5. Prepare data for LSTM (create sequences)
            def create_sequences(data, window_size=14):
                X, y = [], []
                for i in range(len(data) - window_size):
                    X.append(data[i:i+window_size])
                    y.append(data[i+window_size])
                return np.array(X), np.array(y)

            # Assuming you want to predict for a specific part_id, let's filter the data
            # For this example, we'll predict for the first part_id found in the data
            part_id = df['part_id'].iloc[0]
            df_part = df[df['part_id'] == part_id]
            
            X, y = create_sequences(df_part['quantity_sold_normalized'].values)

            # --- Prediction ---
            if len(X) > 0 :
                predictions_normalized = model.predict(X)

                # Inverse transform to get actual values
                predictions = scaler.inverse_transform(predictions_normalized)

                # Prepare the response data
                response_data = {
                    'part_id': part_id,
                    'predictions': predictions.flatten().tolist(),  # Convert to a list for JSON serialization
                    'dates': df_part['date'].iloc[14:].dt.strftime('%Y-%m-%d').tolist() # Corresponding dates
                }
            else:
                response_data = {'part_id': part_id, 'predictions': [], 'dates': []}

            return Response(response_data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)