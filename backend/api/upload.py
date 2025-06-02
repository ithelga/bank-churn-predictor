import os
import traceback
from io import StringIO
import pandas as pd
import joblib
from fastapi import APIRouter, HTTPException, UploadFile, File
from services.db_service import save_upload_record, save_clients

router = APIRouter()

# Пути к файлам модели
ARTIFACTS_DIR = os.path.join("model", "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")
PREPROCESSOR_PATH = os.path.join(ARTIFACTS_DIR, "preprocessor.pkl")

# Загрузка модели и препроцессора
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    if not os.path.exists(PREPROCESSOR_PATH):
        raise FileNotFoundError(f"Preprocessor file not found at {PREPROCESSOR_PATH}")

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model or preprocessor: {str(e)}")

REQUIRED_COLUMNS = [
    "RowNumber", "CustomerId", "Surname", "CreditScore", "Geography", "Gender",
    "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember",
    "EstimatedSalary", "Exited"
]

@router.post("/fine-tune/")
async def post_fine_tune(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported.")

        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )

        # Предобработка и предсказание
        X = df.drop(columns=['Exited'])
        X_clean = preprocessor._clean_data(X)
        X_proc = preprocessor.transform(X_clean)
        surnames = df.loc[X_clean.index, 'Surname'].tolist()
        preds = model.predict(X_proc)
        probs = model.predict_proba(X_proc)[:, 1]

        df_result = df.copy()
        df_result = df_result.loc[X_clean.index].copy()
        df_result["Surname"] = surnames
        df_result["ChurnProbability"] = probs
        df_result["Prediction"] = preds
        df_result["Correct"] = df_result["Exited"] == df_result["Prediction"]

        # Сохранение в БД
        file_uid = save_upload_record(file.filename)
        save_clients(file_uid, df_result.to_dict(orient="records"))

        return {
            "success": True,
            "count": len(df_result),
            "file_uid": file_uid
        }

    except Exception as e:
        error_detail = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Evaluation error:\n{error_detail}")
