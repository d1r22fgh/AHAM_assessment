# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.orm import relationship

# from app.database import Base

# class Fund(Base):
#     __tablename__ = 'fund'

#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
#     manager = Column(String, nullable=False)
#     description = Column(String, nullable=True)
#     net_asset_value = Column(String, nullable=False)
#     created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     performance = Column(String, nullable=False)
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

#     owner = relationship("User")

# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False, unique=True)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
