# API de Predicción con Random Forest

Esta API proporciona un endpoint para realizar predicciones utilizando un modelo de Random Forest pre-entrenado.

## Estructura del Proyecto

```
api_student_depression/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── prediction.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/
│   │   ├── prediction.py
│   │   └── model_loader.py
│   └── main.py
├── models/
│   └── random_forest_model.pkl
├── tests/
│   └── test_prediction.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Colocar el modelo pickle en la carpeta `models/`
2. Iniciar el servidor:

```bash
uvicorn app.main:app --reload
```

3. Acceder a la documentación de la API:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### POST /api/v1/predict

Realiza una predicción utilizando el modelo de Random Forest.

**Request Body:**

```json
{
    "feature1": float,
    "feature2": float,
    ...
}
```

**Response:**

```json
{
    "prediction": int,
    "probability": float
}
```

## Desarrollo

- Python 3.8+
- FastAPI
- scikit-learn
- pandas
- numpy
