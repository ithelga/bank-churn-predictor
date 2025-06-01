from services.db_service import load_clients_df
from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter()


@router.get("/analytics/{file_uid}")
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


def get_age_group_stats(df):
    df_copy = df.copy()
    df_copy["AgeGroup"] = pd.cut(df_copy["Age"], bins=[0, 30, 40, 50, 60, 150],
                                 labels=["<30", "30-40", "40-50", "50-60", "60+"])
    return df_copy.groupby("AgeGroup")["ChurnProbability"].mean().round(3).to_dict()


def get_gender_stats(df):
    return df.groupby("Gender")["ChurnProbability"].mean().round(3).to_dict()


def get_geography_stats(df):
    return df.groupby("Geography")["ChurnProbability"].mean().round(3).to_dict()


def get_credit_score_stats(df):
    df_copy = df.copy()
    df_copy["CreditGroup"] = pd.cut(df_copy["CreditScore"], bins=[300, 500, 650, 750, 850],
                                    labels=["Low", "Medium", "High", "Very High"])
    return df_copy.groupby("CreditGroup")["ChurnProbability"].mean().round(3).to_dict()


def get_activity_stats(df):
    return df.groupby("IsActiveMember")["ChurnProbability"].mean().round(3).to_dict()


def get_balance_stats(df):
    df_copy = df.copy()
    df_copy["BalanceGroup"] = pd.cut(df_copy["Balance"], bins=[-1, 10000, 50000, 100000, 150000, 200000],
                                     labels=["0–10K", "10K–50K", "50K–100K", "100K–150K", "150K+"])
    return df_copy.groupby("BalanceGroup")["ChurnProbability"].mean().round(3).to_dict()


def get_tenure_stats(df):
    return df.groupby("Tenure")["ChurnProbability"].mean().round(3).to_dict()


def get_products_stats(df):
    return df.groupby("NumOfProducts")["ChurnProbability"].mean().round(3).to_dict()


def get_credit_card_stats(df):
    return df.groupby("HasCrCard")["ChurnProbability"].mean().round(3).to_dict()


def get_salary_stats(df):
    df_copy = df.copy()
    df_copy["SalaryGroup"] = pd.cut(df_copy["EstimatedSalary"],
                                    bins=[-1, 20000, 50000, 100000, 150000, 200000],
                                    labels=["<20K", "20K–50K", "50K–100K", "100K–150K", "150K+"])
    return df_copy.groupby("SalaryGroup")["ChurnProbability"].mean().round(3).to_dict()
