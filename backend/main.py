from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.db import init_db
from api import upload, analytics, clients
import uvicorn

init_db()

app = FastAPI(title="Bank Churn Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analytics.router)
app.include_router(clients.router)

@app.get("/")
def root():
    return {"message": "Bank Churn API is running."}

def run_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    run_server()

