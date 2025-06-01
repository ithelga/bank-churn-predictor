import os
import uuid
import traceback
from io import StringIO
from datetime import datetime
import pandas as pd
import joblib
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.db.db import init_db, SessionLocal
from utils.db.models import Upload, Client
from utils.data_loader import load_clients_df

from analytics.churn_stats import get_age_group_stats, get_gender_stats, get_geography_stats, get_credit_score_stats, \
    get_activity_stats, get_balance_stats, get_tenure_stats, get_products_stats, get_credit_card_stats, get_salary_stats
from analytics.client_info import filter_clients_by_group

# Инициализация БД
init_db()

# FastAPI app
app = FastAPI(title="Bank Churn Predictor API")

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пути к файлам модели
ARTIFACTS_DIR = os.path.join("model", "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")
PREPROCESSOR_PATH = os.path.join(ARTIFACTS_DIR, "preprocessor.pkl")
LOG_PATH = "logs"
os.makedirs(LOG_PATH, exist_ok=True)

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

import math


def safe_int(value):
    try:
        if pd.isna(value):
            return None
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value):
    try:
        if pd.isna(value) or isinstance(value, str) and value.strip() == "":
            return None
        val = float(value)
        return None if math.isinf(val) or math.isnan(val) else val
    except (ValueError, TypeError):
        return None


def safe_str(value):
    try:
        if pd.isna(value):
            return None
        return str(value)
    except Exception:
        return None


@app.post("/fine-tune/")
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
        df_result = df_result.loc[X_clean.index].copy()  # сохранить фильтрацию
        df_result["Surname"] = surnames
        df_result["ChurnProbability"] = probs
        df_result["Prediction"] = preds
        df_result["Correct"] = df_result["Exited"] == df_result["Prediction"]

        # # Работа с БД
        session = SessionLocal()
        file_uid = str(uuid.uuid4())
        upload_entry = Upload(
            filename=file.filename,
            file_uid=file_uid,
            upload_time=datetime.utcnow()
        )
        session.add(upload_entry)
        session.commit()

        for _, row in df_result.iterrows():
            client_entry = Client(
                file_uid=file_uid,
                client_uid=str(uuid.uuid4()),

                surname=safe_str(row.get("Surname")),
                credit_score=safe_int(row.get("CreditScore")),
                geography=safe_str(row.get("Geography")),
                gender=safe_str(row.get("Gender")),
                age=safe_int(row.get("Age")),
                tenure=safe_int(row.get("Tenure")),
                balance=safe_float(row.get("Balance")),
                num_of_products=safe_int(row.get("NumOfProducts")),
                has_cr_card=safe_int(row.get("HasCrCard")),
                is_active_member=safe_int(row.get("IsActiveMember")),
                estimated_salary=safe_float(row.get("EstimatedSalary")),

                prediction=safe_int(row.get("Prediction")),
                churn_prob=safe_float(row.get("ChurnProbability")),
                actual=safe_int(row.get("Exited"))
            )
            session.add(client_entry)

        session.commit()
        session.close()

        return {
            "success": True,
            "count": len(df_result),
            "file_uid": file_uid
        }

    except Exception as e:
        error_detail = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Evaluation error:\n{error_detail}")


@app.get("/analytics/{file_uid}")
def get_analytics(file_uid: str):
    df = load_clients_df(file_uid)
    if df.empty:
        raise HTTPException(status_code=404, detail="No clients found for this file_uid")

    analytics = {
        "age_groups": get_age_group_stats(df),
        "gender": get_gender_stats(df),
        "geography": get_geography_stats(df),
        "credit_score": get_credit_score_stats(df),
        "activity": get_activity_stats(df),
        "balance": get_balance_stats(df),
        "tenure": get_tenure_stats(df),
        "num_of_products": get_products_stats(df),
        "has_credit_card": get_credit_card_stats(df),
        "estimated_salary": get_salary_stats(df),
    }

    return {"analytics": analytics}


@app.get("/clients-group/{file_uid}")
def get_clients_by_group(file_uid: str, group: int = 0):
    df = load_clients_df(file_uid)
    if df.empty:
        raise HTTPException(status_code=404, detail="No clients found for this file_uid")

    try:
        result = filter_clients_by_group(df, group)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"clients_info": result}


def run_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run_server()
