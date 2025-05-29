import os
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import traceback
from analytics.churn_stats import get_age_group_stats, get_gender_stats, get_geography_stats, get_credit_score_stats, \
    get_activity_stats, get_balance_stats, get_tenure_stats, get_products_stats, get_credit_card_stats, get_salary_stats
from analytics.client_info import get_clients_info

app = FastAPI(title="Bank Churn Predictor API")

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пути к файлам
ARTIFACTS_DIR = os.path.join("model", "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")
PREPROCESSOR_PATH = os.path.join(ARTIFACTS_DIR, "preprocessor.pkl")
TEST_DATA_PATH = os.path.join(ARTIFACTS_DIR, "test_raw.csv")

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


@app.get("/")
def read_root():
    return {
        "message": "Bank Churn Predictor API is running!",
        "endpoints": {
            "GET /": "Info page",
            "GET /test-evaluate/": "Evaluate model on saved test data"
        }
    }


@app.get("/test-evaluate/")
async def test_evaluate():
    import traceback
    try:
        if not os.path.exists(TEST_DATA_PATH):
            raise HTTPException(status_code=404, detail="Test data not found.")

        df = pd.read_csv(TEST_DATA_PATH)

        if 'Exited' not in df.columns:
            raise HTTPException(status_code=400, detail="Missing 'Exited' column in test data.")

        X = df.drop(columns=['Exited'])

        X_clean = preprocessor._clean_data(X)
        X_proc = preprocessor.transform(X_clean)
        surnames = df.loc[X_clean.index, 'Surname'].tolist()

        preds = model.predict(X_proc)
        probs = model.predict_proba(X_proc)[:, 1]

        df_result = df.loc[X_clean.index].copy()
        df_result["Surname"] = surnames
        df_result["ChurnProbability"] = probs
        df_result["Prediction"] = preds
        df_result["Correct"] = df_result["Exited"] == df_result["Prediction"]

        output = {
            "success": True,
            "count": len(df_result),
            "clients_info": get_clients_info(df_result, top_n=50),
            "analytics": {
                "age_groups": get_age_group_stats(df_result),
                "gender": get_gender_stats(df_result),
                "geography": get_geography_stats(df_result),
                "credit_score": get_credit_score_stats(df_result),
                "activity": get_activity_stats(df_result),
                "balance": get_balance_stats(df_result),
                "tenure": get_tenure_stats(df_result),
                "num_of_products": get_products_stats(df_result),
                "has_credit_card": get_credit_card_stats(df_result),
                "estimated_salary": get_salary_stats(df_result)
            }
        }

        return output

    except Exception as e:
        error_detail = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Evaluation error:\n{error_detail}")


def run_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run_server()
