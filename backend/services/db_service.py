import pandas as pd

from services.db_models import Client, Upload
from utils.db import SessionLocal
import uuid
from datetime import datetime


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


def save_upload_record(filename: str) -> str:
    session = SessionLocal()
    file_uid = str(uuid.uuid4())
    upload_entry = Upload(
        filename=filename,
        file_uid=file_uid,
        upload_time=datetime.utcnow()
    )
    session.add(upload_entry)
    session.commit()
    session.close()
    return file_uid


def save_clients(file_uid: str, clients_data: list[dict]) -> None:
    session = SessionLocal()
    for row in clients_data:
        client_entry = Client(
            file_uid=file_uid,
            client_uid=str(uuid.uuid4()),

            surname=row.get("Surname"),
            credit_score=row.get("CreditScore"),
            geography=row.get("Geography"),
            gender=row.get("Gender"),
            age=row.get("Age"),
            tenure=row.get("Tenure"),
            balance=row.get("Balance"),
            num_of_products=row.get("NumOfProducts"),
            has_cr_card=row.get("HasCrCard"),
            is_active_member=row.get("IsActiveMember"),
            estimated_salary=row.get("EstimatedSalary"),

            prediction=row.get("Prediction"),
            churn_prob=row.get("ChurnProbability"),
            actual=row.get("Exited"),
        )
        session.add(client_entry)

    session.commit()
    session.close()
