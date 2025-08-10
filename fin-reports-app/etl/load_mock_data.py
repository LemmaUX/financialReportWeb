#!/usr/bin/env python3
"""
Load mock financial data for testing purposes when external data sources are unavailable.
"""

import sys
import os
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

# Add backend directory to path to import database models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal, Asset, Price

def get_db_session():
    """Get database session"""
    return SessionLocal()

def generate_mock_prices(base_price: float, days: int):
    """Generate realistic mock price data"""
    prices = []
    current_price = base_price
    
    for i in range(days):
        # Generate realistic price movements
        change_percent = random.uniform(-0.05, 0.05)  # -5% to +5% daily change
        current_price *= (1 + change_percent)
        
        # Generate OHLC data
        high = current_price * random.uniform(1.001, 1.03)
        low = current_price * random.uniform(0.97, 0.999)
        open_price = current_price * random.uniform(0.98, 1.02)
        close = current_price
        volume = random.randint(1000000, 50000000)
        
        prices.append({
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })
    
    return prices

def load_mock_data():
    """Load mock data for sample assets"""
    
    # Sample assets with base prices
    assets_data = [
        ("TSLA", "Tesla Inc", 250.0),
        ("AAPL", "Apple Inc", 175.0),
        ("GOOGL", "Alphabet Inc", 140.0),
        ("MSFT", "Microsoft Corporation", 350.0),
        ("NVDA", "NVIDIA Corporation", 700.0)
    ]
    
    # Date range - last 90 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=90)
    
    print(f"Loading mock data from {start_date} to {end_date}")
    
    db = get_db_session()
    
    try:
        for symbol, name, base_price in assets_data:
            print(f"Processing {symbol}...")
            
            # Ensure asset exists
            asset = db.query(Asset).filter(Asset.symbol == symbol).first()
            if not asset:
                asset = Asset(symbol=symbol, name=name)
                db.add(asset)
                db.commit()
                db.refresh(asset)
                print(f"Added asset: {symbol}")
            
            # Clear existing data
            db.query(Price).filter(Price.asset_id == asset.id).delete()
            
            # Generate mock prices
            mock_prices = generate_mock_prices(base_price, 90)
            
            # Insert mock data
            current_date = start_date
            for i, price_data in enumerate(mock_prices):
                price_record = Price(
                    asset_id=asset.id,
                    date=current_date,
                    open=price_data['open'],
                    high=price_data['high'],
                    low=price_data['low'],
                    close=price_data['close'],
                    volume=price_data['volume']
                )
                db.add(price_record)
                current_date += timedelta(days=1)
            
            db.commit()
            print(f"Added {len(mock_prices)} price records for {symbol}")
        
        print("\nMock data loading completed successfully!")
        
        # Print summary
        total_assets = db.query(Asset).count()
        total_prices = db.query(Price).count()
        print(f"Database now contains {total_assets} assets and {total_prices} price records")
        
    except Exception as e:
        print(f"Error loading mock data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_mock_data()