from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from datetime import datetime
import json 
from pathlib import Path
from typing import Dict


from app import schemas

project_dir = Path(__file__).resolve().parent
parent_dir = project_dir.parent

with open(f"{parent_dir}/fund.json") as f:
    data_json = json.load(f)

def save_to_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, default=str, indent=4)

router = APIRouter(prefix="/funds", tags=["Funds"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Fund)
def create_funds(
    fund: schemas.FundCreate,
):
    new_fund_id = len(data_json) + 1
    new_fund = schemas.Fund(
        fund_id = new_fund_id, 
        fund_name = fund.fund_name, 
        manager_id = fund.manager_id, 
        performance = fund.performance,
        description = fund.description,
        nav = fund.nav,
        created_at=datetime.utcnow())

    data_json[new_fund_id] = new_fund.dict()
    save_to_json("fund", data_json)

    return new_fund

@router.get("/", response_model=Dict[str, schemas.Fund])
def get_posts():    
    return data_json

@router.get("/{id}", response_model=schemas.Fund)
def get_single_post(
    id: str, 
    
    data=data_json
    ):
    try:
        result = data[id] 
        return result
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find fund with id {id}",
        )

@router.patch("/{id}", response_model=schemas.Fund)
def update_fund_performance(
    id: int, 
    fund: schemas.FundUpdatePerformance, 
    data=data_json
):
    try:
        udpated_fund = fund.dict(exclude_unset=True)
        data[id]['performance'] = udpated_fund['performance']
        save_to_json("fund", data)
        return data[id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find fund with id {id}",
        )
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fund(
    id: str,
    data=data_json
):
    try:
        del data[id]
        save_to_json("fund", data)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find fund with id {id}",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)