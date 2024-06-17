from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import json
from pathlib import Path
from app import schemas, utils, models
# from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

project_dir = Path(__file__).resolve().parent
parent_dir = project_dir.parent

with open(f"{parent_dir}/user.json") as f:
    data_json = json.load(f)

def save_to_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, default=str, indent=4)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate, 
    ):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user_id = len(data_json) + 1
    
    new_user = schemas.User(
        id=new_user_id, 
        email=user.email, 
        name=user.name, 
        password=user.password, 
        created_at=datetime.utcnow())

    data_json[new_user_id] = new_user.dict()
    save_to_json(f"{parent_dir}/user.json", data_json)
    return new_user

