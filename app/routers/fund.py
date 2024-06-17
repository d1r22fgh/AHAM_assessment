from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from datetime import datetime
import json 
from pathlib import Path
from typing import Dict
from sqlalchemy.orm import Session

from app import schemas
from app.models import Fund
from app.database import get_db

from app.utils import json_file, save_to_json

router = APIRouter(prefix="/funds", tags=["Funds"])

data_json = json_file("fund")

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
def get_all_funds():    
    return data_json

@router.get("/{id}", response_model=schemas.Fund)
def get_single_fund(
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

@router.post("/post_to_db", status_code=status.HTTP_201_CREATED)
def post_to_db(db: Session = Depends(get_db)):
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
    return {"message": "successfully upload fund json to sql database"}

    