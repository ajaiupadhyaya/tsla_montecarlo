import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from typing import Dict, List, Tuple
import joblib
import os

class MLService:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.models = {}
        self.model_path = "models"
        os.makedirs(self.model_path, exist_ok=True)

    def prepare_data(self, data: pd.DataFrame, sequence_length: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for ML models"""
        # Create features
        df = data.copy()
        df['Returns'] = df['Close'].pct_change()
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        df['Volume_MA5'] = df['Volume'].rolling(window=5).mean()
        
        # Create target (next day's price)
        df['Target'] = df['Close'].shift(-1)
        
        # Drop NaN values
        df = df.dropna()
        
        # Select features
        features = ['Close', 'Returns', 'MA5', 'MA20', 'Volatility', 'Volume', 'Volume_MA5']
        X = df[features].values
        y = df['Target'].values
        
        # Scale the data
        X_scaled = self.scaler.fit_transform(X)
        
        # Create sequences
        X_seq, y_seq = [], []
        for i in range(len(X_scaled) - sequence_length):
            X_seq.append(X_scaled[i:(i + sequence_length)])
            y_seq.append(y[i + sequence_length])
        
        return np.array(X_seq), np.array(y_seq)

    def build_lstm_model(self, input_shape: Tuple[int, int]) -> tf.keras.Model:
        """Build LSTM model"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train_models(self, data: pd.DataFrame) -> Dict:
        """Train multiple ML models"""
        # Prepare data
        X, y = self.prepare_data(data)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Train Random Forest
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
        self.models['random_forest'] = rf_model
        
        # Train Gradient Boosting
        gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        gb_model.fit(X_train.reshape(X_train.shape[0], -1), y_train)
        self.models['gradient_boosting'] = gb_model
        
        # Train LSTM
        lstm_model = self.build_lstm_model((X_train.shape[1], X_train.shape[2]))
        lstm_model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=0)
        self.models['lstm'] = lstm_model
        
        # Evaluate models
        predictions = {}
        metrics = {}
        
        for name, model in self.models.items():
            if name == 'lstm':
                pred = model.predict(X_test)
            else:
                pred = model.predict(X_test.reshape(X_test.shape[0], -1))
            
            predictions[name] = pred
            metrics[name] = {
                'mse': mean_squared_error(y_test, pred),
                'r2': r2_score(y_test, pred)
            }
        
        # Save models
        self.save_models()
        
        return {
            'predictions': predictions,
            'metrics': metrics,
            'test_data': y_test.tolist()
        }

    def predict_next_day(self, data: pd.DataFrame) -> Dict:
        """Predict next day's price using all models"""
        X, _ = self.prepare_data(data)
        latest_sequence = X[-1:]
        
        predictions = {}
        for name, model in self.models.items():
            if name == 'lstm':
                pred = model.predict(latest_sequence)
            else:
                pred = model.predict(latest_sequence.reshape(1, -1))
            predictions[name] = float(pred[0])
        
        # Calculate ensemble prediction (weighted average)
        weights = {
            'random_forest': 0.3,
            'gradient_boosting': 0.3,
            'lstm': 0.4
        }
        
        ensemble_pred = sum(predictions[model] * weights[model] for model in predictions)
        
        return {
            'individual_predictions': predictions,
            'ensemble_prediction': ensemble_pred,
            'current_price': float(data['Close'].iloc[-1]),
            'predicted_change': (ensemble_pred - float(data['Close'].iloc[-1])) / float(data['Close'].iloc[-1]) * 100
        }

    def save_models(self):
        """Save trained models"""
        for name, model in self.models.items():
            if name == 'lstm':
                model.save(os.path.join(self.model_path, f'{name}_model.h5'))
            else:
                joblib.dump(model, os.path.join(self.model_path, f'{name}_model.joblib'))
        
        # Save scaler
        joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.joblib'))

    def load_models(self):
        """Load trained models"""
        for name in ['random_forest', 'gradient_boosting']:
            model_path = os.path.join(self.model_path, f'{name}_model.joblib')
            if os.path.exists(model_path):
                self.models[name] = joblib.load(model_path)
        
        # Load LSTM model
        lstm_path = os.path.join(self.model_path, 'lstm_model.h5')
        if os.path.exists(lstm_path):
            self.models['lstm'] = tf.keras.models.load_model(lstm_path)
        
        # Load scaler
        scaler_path = os.path.join(self.model_path, 'scaler.joblib')
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path) 