import pandas as pd

from utils.db.db import SessionLocal
from utils.db.models import Client


def load_clients_df(file_uid: str) -> pd.DataFrame:
    session = SessionLocal()
    clients = session.query(Client).filter(Client.file_uid == file_uid).all()
    session.close()

    if not clients:
        return pd.DataFrame()

    data = [
        {
            "Surname": c.surname,
            "CreditScore": c.credit_score,
            "Geography": c.geography,
            "Gender": c.gender,
            "Age": c.age,
            "Tenure": c.tenure,
            "Balance": c.balance,
            "NumOfProducts": c.num_of_products,
            "HasCrCard": c.has_cr_card,
            "IsActiveMember": c.is_active_member,
            "EstimatedSalary": c.estimated_salary,
            "ChurnProbability": c.churn_prob,
            "Prediction": c.prediction,
            "Exited": c.actual
        }
        for c in clients
    ]

    return pd.DataFrame(data)
