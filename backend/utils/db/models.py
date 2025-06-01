from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_uid = Column(String, unique=True, nullable=False)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    file_uid = Column(String, ForeignKey("uploads.file_uid"), nullable=False)
    client_uid = Column(String, unique=True, nullable=False)

    surname = Column(String, nullable=True)
    credit_score = Column(Integer, nullable=True)
    geography = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    tenure = Column(Integer, nullable=True)
    balance = Column(Float, nullable=True)
    num_of_products = Column(Integer, nullable=True)
    has_cr_card = Column(Integer, nullable=True)
    is_active_member = Column(Integer, nullable=True)
    estimated_salary = Column(Float, nullable=True)

    prediction = Column(Integer, nullable=True)
    churn_prob = Column(Float, nullable=True)
    actual = Column(Integer, nullable=True)