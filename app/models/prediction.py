from pydantic import BaseModel, Field
from typing import Dict, Any, Literal
from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class SleepHours(str, Enum):
    LESS_THAN_5 = "Less than 5 hours"
    BETWEEN_5_AND_6 = "5-6 hours"
    BETWEEN_7_AND_8 = "7-8 hours"
    MORE_THAN_8 = "More than 8 hours"
    OTHERS = "Others"

class Diet(str, Enum):
    HEALTHY = "Healthy"
    MODERATE = "Moderate"
    UNHEALTHY = "Unhealthy"
    OTHERS = "Others"

class MentalIllnessHistory(str, Enum):
    YES = "Yes"
    NO = "No"

class LevelCategory(str, Enum):
    BAJO = "bajo"
    MEDIO = "medio"
    MEDIO_ALTO = "medio alto"
    ALTO = "alto"

class DegreeGrouped(str, Enum):
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"
    CLASS_12 = "Class 12"
    OTHERS = "Others"

class PredictionRequest(BaseModel):
    """
    Modelo para la solicitud de predicción de depresión de estudiantes.
    """
    gender: Gender = Field(..., description="Género del estudiante")
    age: float = Field(..., ge=0, le=100, description="Edad del estudiante")
    city: str = Field(..., description="Ciudad donde vive el estudiante")
    sleep_hours: SleepHours = Field(..., description="Promedio de horas de sueño por día")
    diet: Diet = Field(..., description="Tipo de dieta")
    hours_dedicated: float = Field(..., ge=0, le=24, description="Horas dedicadas al estudio por día")
    mental_illness_history: MentalIllnessHistory = Field(..., description="Historial de enfermedades mentales")
    study_satisfaction_level_cat: LevelCategory = Field(..., description="Nivel de satisfacción con los estudios")
    financial_stress_cat: LevelCategory = Field(..., description="Nivel de estrés financiero")
    academic_pressure_cat: LevelCategory = Field(..., description="Nivel de presión académica")
    cgpa_cat: LevelCategory = Field(..., description="Categoría de GPA acumulado")
    degree_grouped: DegreeGrouped = Field(..., description="Campo de estudio")

class PredictionResponse(BaseModel):
    """
    Modelo para la respuesta de la predicción de depresión de estudiantes.
    """
    prediction: int = Field(..., description="Prediction (0: No depression, 1: Depression)")
    probability: float = Field(..., ge=0, le=1, description="Probabilidad de depresión")
    interpretation: str = Field(..., description="interpretación de la predicción") 