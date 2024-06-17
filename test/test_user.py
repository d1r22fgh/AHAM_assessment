import pytest
from jose import jwt
from fastapi import HTTPException
from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post("/users", json={
        "name": "test", 
        "email": "testing@gmail.com", 
        "password": "password123"})
    new_user = schemas.UserOut(**response.json())
    print(new_user)
    # assert new_user.email == "testing@gmail.com"
    assert response.status_code == 201

