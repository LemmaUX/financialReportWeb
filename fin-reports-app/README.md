# fin-reports-app

Aplicación web para reportes financieros con visualización de datos avanzada.

## ✨ Funcionalidades Principales

### 📊 **Sistema de Visualización de Datos Financieros (NUEVO)**
- **Gráficos interactivos** de precios históricos usando Chart.js
- **Múltiples activos** disponibles (TSLA, AAPL, GOOGL, MSFT, NVDA)
- **Selector de fechas** personalizable para análisis temporal
- **Estadísticas en tiempo real**: precio actual, máximo, mínimo, volumen promedio
- **Interfaz responsive** con diseño moderno y profesional

### 🔧 **Arquitectura Técnica**
- **Backend**: FastAPI con SQLAlchemy ORM
- **Frontend**: React + TypeScript + Chart.js
- **Base de Datos**: SQLite (configurable a PostgreSQL)
- **ETL**: Scripts Python para carga de datos
- **API**: RESTful con autenticación y CORS

## 🚀 Estructura del Proyecto

```
fin-reports-app/
├── backend/                    # API en FastAPI
│   ├── main.py                # Endpoints principales
│   ├── database.py            # Modelos y conexión a BD
│   ├── requirements.txt       # Dependencias Python
│   └── financial_data.db      # Base de datos SQLite
├── frontend-new/              # Aplicación React
│   ├── src/
│   │   ├── App.tsx           # Componente principal con gráficos
│   │   ├── App.css           # Estilos personalizados
│   │   └── ...
│   ├── package.json          # Dependencias Node.js
│   └── public/
├── etl/                       # Scripts de carga de datos
│   ├── load_mock_data.py     # Carga datos de prueba
│   ├── etl_example.py        # ETL con Yahoo Finance
│   └── requirements.txt
└── db/
    └── schema.sql            # Esquema de base de datos
```

## 🛠 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- npm o yarn

### 1. Backend (FastAPI)

```bash
cd backend/
pip install -r requirements.txt

# Cargar datos de prueba
cd ../etl/
python load_mock_data.py

# Iniciar servidor
cd ../backend/
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: http://localhost:8000

### 2. Frontend (React)

```bash
cd frontend-new/
npm install
npm start
```

La aplicación web estará disponible en: http://localhost:3000

## 📊 Endpoints API

### `GET /assets`
Obtiene la lista de activos disponibles.

**Respuesta:**
```json
[
  {"symbol": "TSLA", "name": "Tesla Inc"},
  {"symbol": "AAPL", "name": "Apple Inc"},
  ...
]
```

### `GET /reports`
Obtiene datos históricos de precios para un activo específico.

**Parámetros:**
- `asset`: Símbolo del activo (ej: "TSLA")
- `from_date`: Fecha inicio (formato: YYYY-MM-DD)
- `to_date`: Fecha fin (formato: YYYY-MM-DD)

**Headers:**
- `Authorization: Bearer fake-token`

**Respuesta:**
```json
{
  "asset": "TSLA",
  "asset_name": "Tesla Inc",
  "from": "2025-07-01",
  "to": "2025-08-10",
  "data": [
    {
      "date": "2025-07-01",
      "open": 238.88,
      "high": 245.95,
      "low": 241.93,
      "close": 242.29,
      "volume": 23545407
    },
    ...
  ],
  "count": 40
}
```

## 🎯 Funcionalidades de la Interfaz

### Dashboard Principal
- **Header atractivo** con gradientes y diseño moderno
- **Panel de búsqueda** con selectores intuitivos
- **Visualización de gráficos** interactivos y responsivos

### Gráficos de Precios
- **Líneas múltiples**: Precio de cierre, máximo y mínimo
- **Colores diferenciados** para cada métrica
- **Tooltips informativos** al pasar el mouse
- **Escalas automáticas** adaptativas

### Estadísticas Resumidas
- **Tarjetas de métricas** con efectos visuales
- **Cálculos en tiempo real** de estadísticas clave
- **Formato de números** profesional con separadores

### Diseño Responsive
- **Adaptable a móviles** y tablets
- **Grid flexible** para las tarjetas de estadísticas
- **Navegación optimizada** para touch

## 🔄 Carga de Datos

### Datos Mock (Incluidos)
El sistema incluye datos de prueba para 5 activos populares:
- **TSLA** (Tesla Inc)
- **AAPL** (Apple Inc) 
- **GOOGL** (Alphabet Inc)
- **MSFT** (Microsoft Corporation)
- **NVDA** (NVIDIA Corporation)

### Datos Reales (Yahoo Finance)
Para cargar datos reales, usar el script ETL mejorado:

```bash
cd etl/
# Cargar un activo específico
python etl_example.py AAPL 2024-01-01 2024-12-31

# Cargar datos de muestra
python etl_example.py
```

## 🚀 Próximas Mejoras Sugeridas

### Funcionalidades Avanzadas
1. **Indicadores técnicos** (RSI, MACD, Bollinger Bands)
2. **Comparación múltiple** de activos
3. **Alertas de precios** y notificaciones
4. **Análisis de correlación** entre activos
5. **Exportación** a PDF/Excel
6. **Análisis de portfolio** y diversificación

### Mejoras Técnicas
1. **Autenticación real** con JWT
2. **Base de datos PostgreSQL** en producción
3. **Cache con Redis** para mejor rendimiento
4. **WebSockets** para datos en tiempo real
5. **Tests automatizados** (backend y frontend)
6. **Dockerización** para deployment fácil

## 🎨 Personalización

### Temas y Colores
Los colores principales se pueden modificar en `frontend-new/src/App.css`:
- **Primary gradient**: `#667eea` a `#764ba2`
- **Secondary gradient**: `#f093fb` a `#f5576c`

### Gráficos
Los estilos de gráficos se configuran en el componente `App.tsx` usando Chart.js options.

---

**Stack tecnológico**: Python, FastAPI, React, TypeScript, Chart.js, SQLAlchemy, SQLite
