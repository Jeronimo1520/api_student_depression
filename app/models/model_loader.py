import pickle
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
import pandas as pd
from app.core.config import settings

class ModelLoader:
    _instance = None
    _model = None
    _threshold = 0.5  # Umbral por defecto para clasificar depresión

    # Valores permitidos para variables categóricas
    ALLOWED_VALUES = {
        "gender": ["Male", "Female"],
        "sleep_hours": ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"],
        "diet": ["Healthy", "Moderate", "Unhealthy"],
        "mental_illness_history": ["Yes", "No"],
        "study_satisfaction_level_cat": ["bajo", "medio", "medio alto", "alto"],
        "financial_stress_cat": ["bajo", "medio", "medio alto", "alto"],
        "academic_pressure_cat": ["bajo", "medio", "medio alto", "alto"],
        "cgpa_cat": ["bajo", "medio", "medio alto", "alto"],
        "degree_grouped": ["Bachelor", "Master", "Doctorate"]
    }

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

    def validate_features(self, features: Dict[str, Any]) -> None:
        """
        Validar que los valores de las características sean válidos.
        
        Args:
            features (Dict[str, Any]): Diccionario con los valores de las características
            
        Raises:
            ValueError: Si algún valor no es válido
        """
        # Validar variables categóricas
        for feature, allowed_values in self.ALLOWED_VALUES.items():
            if feature in features:
                if features[feature] not in allowed_values:
                    raise ValueError(
                        f"Valor inválido para {feature}: '{features[feature]}'. "
                        f"Valores permitidos: {allowed_values}"
                    )

        # Validar variables numéricas
        if "age" in features and not (0 <= features["age"] <= 100):
            raise ValueError("La edad debe estar entre 0 y 100 años")
        
        if "hours_dedicated" in features and not (0 <= features["hours_dedicated"] <= 24):
            raise ValueError("Las horas dedicadas deben estar entre 0 y 24")

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realizar una predicción utilizando el modelo cargado.
        
        Args:
            features (Dict[str, Any]): Diccionario con los valores de las características
            
        Returns:
            Dict[str, Any]: Diccionario con la predicción y la probabilidad de depresión
        """
        try:
            # Validar los valores de entrada
            self.validate_features(features)
            
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