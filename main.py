
from register import register_user
from authenticate import authenticate_user
from fastapi import FastAPI, HTTPException
from api.routes.authenticate import authenticate_user
from api.routes.register import register_user


app = FastAPI()

@app.post("/register")
def register(name: str):
    try:
        register_user(name)
        return {"message": f"Usuario {name} registrado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/authenticate")
def authenticate():
    try:
        result = authenticate_user()
        if result:
            return {"message": "Autenticación exitosa"}
        else:
            return {"message": "Autenticación fallida"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    