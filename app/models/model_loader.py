import pickle
from pathlib import Path
from typing import Any, Dict
import numpy as np
import pandas as pd
from app.core.config import settings

class ModelLoader:
    _instance = None
    _model = None
    _threshold = 0.5  # Umbral por defecto para clasificar depresión

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

    def set_threshold(self, threshold: float) -> None:
        """
        Establecer el umbral para la clasificación de depresión.
        
        Args:
            threshold (float): Valor entre 0 y 1 que determina el umbral de probabilidad
                             para clasificar como depresión.
        """
        if not 0 <= threshold <= 1:
            raise ValueError("El umbral debe estar entre 0 y 1")
        self._threshold = threshold

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
            
            # Obtener las probabilidades de predicción [prob_no_depresión, prob_depresión]
            probabilities = self._model.predict_proba(df)[0]
            depression_probability = float(probabilities[1])  # Probabilidad de depresión (class 1)
            
            # Usar el umbral para determinar la predicción
            prediction = 1 if depression_probability >= self._threshold else 0
            
            return {
                "prediction": prediction,  # 0: No depression, 1: Depression
                "probability": depression_probability,  # Probabilidad de depresión
                "interpretation": "Depresión detectada" if prediction == 1 else "Depresión no detectada",
                "threshold_used": self._threshold  # Incluir el umbral usado en la respuesta
            }
        except Exception as e:
            raise Exception(f"Error al realizar la predicción: {str(e)}")

# Create a singleton instance
model_loader = ModelLoader() 