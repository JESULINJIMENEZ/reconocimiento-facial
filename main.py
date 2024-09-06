import uvicorn
from fastapi import FastAPI, Form, UploadFile, File  # Importar Form, UploadFile, File
from api.routes.register import register_user  # Importa la función del archivo register.py

app = FastAPI()

# Ruta raíz para verificar que la API está corriendo
@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de reconocimiento facial"}

# Ruta para registrar un nuevo usuario usando la función de register_user
@app.post("/register/")
async def register_user_endpoint(name: str = Form(...), frame: UploadFile = File(...)):
    return await register_user(name, frame)

# Ejecutar la aplicación usando Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
