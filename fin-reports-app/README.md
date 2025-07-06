# fin-reports-app

Aplicación web para reportes financieros.

## Estructura
- backend/: API en FastAPI (Python)
- frontend/: App web (React)
- etl/: Scripts ETL para cargar datos
- db/: Scripts SQL para la base de datos

## Primeros pasos

### Backend
1. Instala dependencias:
   ```sh
   pip install fastapi uvicorn sqlalchemy passlib python-dotenv
   ```
2. Ejecuta el servidor:
   ```sh
   uvicorn backend.main:app --reload
   ```

### Frontend
1. Instala dependencias:
   ```sh
   npx create-react-app frontend
   cd frontend
   npm install axios
   ```
2. Ejecuta la app:
   ```sh
   npm start
   ```

### ETL
- Scripts para descargar y cargar datos financieros.

### Base de datos
- Scripts para crear tablas y poblar datos de ejemplo.

---
Stack sugerido: Python, FastAPI, React, PostgreSQL, yfinance, pandas.
