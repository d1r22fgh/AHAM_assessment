from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import json
from psycopg2 import sql
from pathlib import Path
from fastapi import Depends
import json

from app.config import settings
from app.models import Fund

project_dir = Path(__file__).resolve().parent

with open(f"{project_dir}/fund.json") as f:
    data_json = json.load(f)

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update(db: Session = Depends(get_db)):
    for key, fund_data in data_json.items():
        fund = Fund(
            fund_id=fund_data['fund_id'],
            fund_name=fund_data['fund_name'],
            manager_id=fund_data['manager_id'],
            performance=fund_data['performance'],
            description=fund_data.get('description', ""),
            nav=fund_data['nav'],
            created_at=fund_data['created_at']
        )
        db.add(fund)

    db.commit()

if __name__ == '__main__':
    update()

