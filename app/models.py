from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from app.database import Base

class Fund(Base):
    __tablename__ = 'funds'

    fund_id = Column(Integer, primary_key=True, nullable=False)
    fund_name = Column(String, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    performance = Column(String, nullable=False)
    description = Column(String, nullable=False, server_default="")
    nav = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

