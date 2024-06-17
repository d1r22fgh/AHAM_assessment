from passlib.context import CryptContext
from pathlib import Path
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def json_file(name: str):
    project_dir = Path(__file__).resolve().parent
    json_file_path = f"{project_dir}/{name}.json"
    
    if not Path(json_file_path).exists():
        data_json = {}
        with open(json_file_path, 'w') as f:
            json.dump(data_json, f)

    with open(json_file_path) as f:
        data_json = json.load(f)
    
    return data_json

def save_to_json(name, data):
    project_dir = Path(__file__).resolve().parent
    json_file_path = f"{project_dir}/{name}.json"
    
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, default=str, indent=4)