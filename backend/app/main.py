from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World - Minimal App Working", "port": os.environ.get("PORT")}
