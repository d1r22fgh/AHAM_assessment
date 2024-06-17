from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import json
from pathlib import Path

from app.models import User
from app import schemas, utils, models
from app.database import get_db
from app.utils import json_file, save_to_json

router = APIRouter(prefix="/users", tags=["Users"])

project_dir = Path(__file__).resolve().parent
parent_dir = project_dir.parent

data_json = json_file('user')

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
    save_to_json("user", data_json)
    return new_user

@router.post("/post_to_db", status_code=status.HTTP_201_CREATED)
def post_to_db(db: Session = Depends(get_db)):
    for key, user_data in data_json.items():
        user = User(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data['name'],
            password=user_data['password'],
            created_at=user_data['created_at']
        )
        db.add(user)
    db.commit()
    return {"message": "successfully upload user json to sql database"}
