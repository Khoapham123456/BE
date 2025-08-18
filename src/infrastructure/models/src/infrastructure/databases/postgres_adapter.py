from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# import models so metadata is available
from infrastructure.models.base import Base
# import model modules to register them (if they exist)
try:
    from infrastructure.models.user_model import User  # noqa: F401
    from infrastructure.models.clinic_model import Clinic  # noqa: F401
    from infrastructure.models.service_model import Service  # noqa: F401
    from infrastructure.models.appointment_model import Appointment  # noqa: F401
except Exception:
    pass

def init_engine_and_session(database_uri: str):
    engine = create_engine(database_uri, pool_pre_ping=True, future=True)
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True))
    return engine, SessionLocal

def create_all_tables(engine):
    Base.metadata.create_all(bind=engine)
