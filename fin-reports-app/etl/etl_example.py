#!/usr/bin/env python3
"""
Enhanced ETL script to download financial data from Yahoo Finance 
and populate the database with real data for the financial reports app.
"""

import yfinance as yf
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add backend directory to path to import database models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal, Asset, Price

def get_db_session():
    """Get database session"""
    return SessionLocal()

def ensure_asset_exists(db: Session, symbol: str, name: str = None):
    """Ensure asset exists in database"""
    asset = db.query(Asset).filter(Asset.symbol == symbol.upper()).first()
    if not asset:
        asset = Asset(
            symbol=symbol.upper(),
            name=name or symbol.upper()
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        print(f"Added new asset: {symbol.upper()}")
    return asset

def download_and_store_data(symbol: str, start_date: str, end_date: str, asset_name: str = None):
    """Download financial data and store in database"""
    
    print(f"Downloading data for {symbol} from {start_date} to {end_date}")
    
    try:
        # Download data from Yahoo Finance
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        if df.empty:
            print(f"No data found for {symbol}")
            return False
        
        # Get database session
        db = get_db_session()
        
        try:
            # Ensure asset exists
            asset = ensure_asset_exists(db, symbol, asset_name)
            
            # Clear existing data for this asset in the date range
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            db.query(Price).filter(
                Price.asset_id == asset.id,
                Price.date >= start_dt,
                Price.date <= end_dt
            ).delete()
            
            # Insert new data
            records_added = 0
            for date_index, row in df.iterrows():
                price_record = Price(
                    asset_id=asset.id,
                    date=date_index.date(),
                    open=float(row['Open']) if pd.notna(row['Open']) else None,
                    high=float(row['High']) if pd.notna(row['High']) else None,
                    low=float(row['Low']) if pd.notna(row['Low']) else None,
                    close=float(row['Close']) if pd.notna(row['Close']) else None,
                    volume=int(row['Volume']) if pd.notna(row['Volume']) else None
                )
                db.add(price_record)
                records_added += 1
            
            db.commit()
            print(f"Successfully added {records_added} price records for {symbol}")
            
            # Also save to CSV for backup
            csv_filename = f"{symbol}_prices_{start_date}_to_{end_date}.csv"
            df.to_csv(csv_filename)
            print(f"Data also saved to {csv_filename}")
            
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error downloading/storing data for {symbol}: {str(e)}")
        return False

def load_sample_data():
    """Load sample data for popular stocks"""
    
    # Define sample assets to load
    assets = [
        ("TSLA", "Tesla Inc"),
        ("AAPL", "Apple Inc"),
        ("GOOGL", "Alphabet Inc"),
        ("MSFT", "Microsoft Corporation"),
        ("NVDA", "NVIDIA Corporation")
    ]
    
    # Date range - last 6 months
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    
    print(f"Loading sample data from {start_date} to {end_date}")
    
    success_count = 0
    for symbol, name in assets:
        if download_and_store_data(symbol, start_date, end_date, name):
            success_count += 1
    
    print(f"\nCompleted loading data for {success_count}/{len(assets)} assets")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Manual mode - specify symbol
        symbol = sys.argv[1].upper()
        start = sys.argv[2] if len(sys.argv) > 2 else "2024-01-01"
        end = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")
        
        download_and_store_data(symbol, start, end)
    else:
        # Default mode - load sample data
        load_sample_data()
