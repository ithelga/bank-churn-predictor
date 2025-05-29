import pandas as pd


def get_clients_info(df, top_n):
    selected_columns = [
        "Surname", "ChurnProbability", "CreditScore", "Geography", "Gender",
        "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard",
        "IsActiveMember", "EstimatedSalary"
    ]

    df_selected = df[selected_columns].copy()

    for col in df_selected.select_dtypes(include="number").columns:
        df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
    df_selected = df_selected.dropna()

    numeric_cols = df_selected.select_dtypes(include="number").columns
    df_selected[numeric_cols] = df_selected[numeric_cols].astype(float).round(3)

    df_top = df_selected.sort_values(by="ChurnProbability", ascending=False).head(top_n)

    return df_top.to_dict(orient="records")
