import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_user(client):
    user_data = {
        "name": "test1",
        "email": "darren@gmail.com",
        "password": "password123"
        }
    response = client.post("/users", json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    assert response.status_code == 201
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        "name": "test2", 
        "email": "d1r22fgh@gmail.com",
        "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_funds():
    funds_data = {
        "2": {
            "fund_id": 2,
            "fund_name": "Tesla",
            "manager_id": 3657,
            "performance": "70%",
            "description": "",
            "nav": "70%",
            "created_date": "2024-06-15 16:02:03.424575"
        },
        "3": {
            "fund_id": 3,
            "fund_name": "Tesla",
            "manager_id": 4234,
            "performance": "70%",
            "description": "",
            "nav": "70%",
            "created_date": "2024-06-15 16:02:03.424575"
        }
    }
    return funds_data