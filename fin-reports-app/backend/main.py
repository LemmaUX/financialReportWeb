from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login():
    return {"access_token": "fake-token", "token_type": "bearer"}

@app.get("/hello")
def hello():
    return {"message": "¡Hola! Bienvenido a la aplicación de reportes financieros"}

@app.get("/reports")
def get_reports(asset: str, from_date: str, to_date: str, token: str = Depends(oauth2_scheme)):
    # Aquí iría la lógica para consultar la base de datos
    return {"asset": asset, "from": from_date, "to": to_date, "data": []}
