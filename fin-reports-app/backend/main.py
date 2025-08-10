from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
from typing import List, Dict, Any
import json

from database import get_db, Asset, Price

app = FastAPI(title="Financial Reports API", description="API for financial data and reports")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login():
    return {"access_token": "fake-token", "token_type": "bearer"}

@app.get("/reports")
def get_reports(
    asset: str, 
    from_date: str, 
    to_date: str, 
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get financial data for a specific asset within date range"""
    try:
        # Parse dates
        start_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        
        # Find asset
        asset_obj = db.query(Asset).filter(Asset.symbol == asset.upper()).first()
        if not asset_obj:
            raise HTTPException(status_code=404, detail=f"Asset {asset} not found")
        
        # Get prices for the asset in date range
        prices = db.query(Price).filter(
            and_(
                Price.asset_id == asset_obj.id,
                Price.date >= start_date,
                Price.date <= end_date
            )
        ).order_by(Price.date).all()
        
        # Format data for charts
        chart_data = []
        for price in prices:
            chart_data.append({
                "date": price.date.isoformat(),
                "open": float(price.open) if price.open else None,
                "high": float(price.high) if price.high else None,
                "low": float(price.low) if price.low else None,
                "close": float(price.close) if price.close else None,
                "volume": int(price.volume) if price.volume else None
            })
        
        return {
            "asset": asset.upper(),
            "asset_name": asset_obj.name,
            "from": from_date,
            "to": to_date,
            "data": chart_data,
            "count": len(chart_data)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/assets")
def get_assets(db: Session = Depends(get_db)):
    """Get list of available assets"""
    assets = db.query(Asset).all()
    return [{"symbol": asset.symbol, "name": asset.name} for asset in assets]

@app.get("/")
def root():
    return {"message": "Financial Reports API", "endpoints": ["/reports", "/assets", "/token"]}
