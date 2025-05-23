import pickle
from pathlib import Path
from typing import Any, Dict
import numpy as np
import pandas as pd
from app.core.config import settings

class ModelLoader:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self.load_model()

    def load_model(self) -> None:
        """Cargar el modelo de Random Forest desde el archivo pickle."""
        try:
            model_path = Path(settings.MODEL_PATH)
            if not model_path.exists():
                raise FileNotFoundError(f"Modelo no encontrado en {model_path}")
            
            with open(model_path, 'rb') as f:
                self._model = pickle.load(f)
                
        except Exception as e:
            raise Exception(f"Error al cargar el modelo: {str(e)}")

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realizar una predicción utilizando el modelo cargado.
        
        Args:
            features (Dict[str, Any]): Diccionario con los valores de las características
            
        Returns:
            Dict[str, Any]: Diccionario con la predicción y la probabilidad de depresión
        """
        try:
            # Crear un DataFrame con una sola fila
            df = pd.DataFrame([features])
            
            # Realizar predicción (0: No depresión, 1: Depresión)
            prediction = self._model.predict(df)[0]
            
            # Obtener las probabilidades de predicción [prob_no_depresión, prob_depresión]
            probabilities = self._model.predict_proba(df)[0]
            depression_probability = float(probabilities[1])  # Probabilidad de depresión (class 1)
            
            return {
                "prediction": int(prediction),  # 0: No depression, 1: Depression
                "probability": depression_probability,  # Probabilidad de depresión
                "interpretation": "Depresión detectada" if prediction == 1 else "Depresión no detectada"
            }
        except Exception as e:
            raise Exception(f"Error al realizar la predicción: {str(e)}")

# Create a singleton instance
model_loader = ModelLoader() 