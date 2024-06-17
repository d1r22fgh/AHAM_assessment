from fastapi import FastAPI

from app.routers import fund, user
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(fund.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api!"}