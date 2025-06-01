import pandas as pd


def filter_clients_by_group(df: pd.DataFrame, group: int) -> list:
    """
    Жесткое деление клиентов по диапазонам ChurnRisk:
    group = 1 → 0.00–0.25
    group = 2 → 0.25–0.50
    group = 3 → 0.50–0.75
    group = 4 → 0.75–1.00
    group = 0 → все
    """
    if group not in [0, 1, 2, 3, 4]:
        raise ValueError("Группа должна быть от 0 до 4")

    bins = {
        1: (0.00, 0.25),
        2: (0.25, 0.50),
        3: (0.50, 0.75),
        4: (0.75, 1.01)  # чуть больше 1, чтобы включить 1.00
    }

    if group == 0:
        filtered_df = df.copy()
    else:
        lower, upper = bins[group]
        filtered_df = df[(df["ChurnProbability"] >= lower) & (df["ChurnProbability"] < upper)]

    selected_columns = [
        "Surname", "ChurnProbability", "CreditScore", "Geography", "Gender",
        "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard",
        "IsActiveMember", "EstimatedSalary"
    ]

    df_selected = filtered_df[selected_columns].copy()

    for col in df_selected.select_dtypes(include="number").columns:
        df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
    df_selected = df_selected.dropna()

    numeric_cols = df_selected.select_dtypes(include="number").columns
    df_selected[numeric_cols] = df_selected[numeric_cols].astype(float).round(3)

    df_sorted = df_selected.sort_values(by="ChurnProbability", ascending=False)

    return df_sorted.to_dict(orient="records")

