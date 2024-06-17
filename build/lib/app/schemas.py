from pydantic import BaseModel, EmailStr, field_validator, validator, ValidationError
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str
    created_at: datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    # created_at: datetime
    # password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Fund(BaseModel):
    fund_id: int
    fund_name: str
    manager_id: int
    performance: str
    description: Optional[str] = ''
    nav: str
    created_at: datetime = datetime.now()
    
    @field_validator('performance')
    def validate_percentage(cls, v):
        # Check if the value ends with a '%' sign
        if not v.endswith('%'):
            raise ValueError('Input must end with "%"')
        
        # Remove the '%' sign and check if the remaining is a valid number
        try:
            value = float(v[:-1])
        except ValueError:
            raise ValueError('Input must be a number followed by "%"')
        
        # Check if the value is between 0 and 100
        if not (0 <= value <= 100):
            raise ValueError('Input must be between 0 and 100')
        
        return v

class FundCreate(BaseModel):
    fund_name: str
    manager: str
    performance: str
    description: Optional[str] = ''
    nav: str

class FundUpdatePerformance(BaseModel):
    fund_id: int
    # fund_name: str
    performance: str
    pass
