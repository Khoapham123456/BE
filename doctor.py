from sqlalchemy import Column, Integer, String
from infrastructure.models.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)   # chuyên khoa
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
