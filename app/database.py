from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"  # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(
#             database="fastapi",
#             user="postgres",
#             password="postgres",
#             host="localhost",
#             port="5432",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection established")
#         break
#     except Exception as error:
#         print(f"Connecting to database failed: {error}")
#         time.sleep(2)
