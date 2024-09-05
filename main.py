from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from api.routes.authenticate import authenticate_user
from api.routes.register import register_user
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}

@app.post("/auth/token")
async def authenticate_user(token: Optional[str] = None):
    await authenticate_user(token)

@app.post("/register/")
async def register_user(name: str):
    await register_user(name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)