from fastapi import APIRouter, HTTPException
from app.models.prediction import PredictionRequest, PredictionResponse
from app.models.model_loader import model_loader

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Realizar una predicción utilizando el modelo de Random Forest.
    
    Args:
        request (PredictionRequest): Las características de entrada para la predicción
        
    Returns:
        PredictionResponse: El resultado de la predicción y su probabilidad
        
    Raises:
        HTTPException: Si ocurre un error durante la predicción
    """
    try:
        # Convertir la solicitud a un diccionario
        features = request.model_dump()
        
        # Realizar predicción
        result = model_loader.predict(features)
        
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 