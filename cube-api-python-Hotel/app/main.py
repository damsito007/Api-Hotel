from fastapi import FastAPI
from .api.router import api_router

app = FastAPI(title="API del Data Warehouse Hotel Plata Paradise")

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Data Warehouse API"}
