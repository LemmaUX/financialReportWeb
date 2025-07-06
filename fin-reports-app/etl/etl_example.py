# Script ETL de ejemplo para descargar datos de Yahoo Finance y guardarlos como CSV
import yfinance as yf
import pandas as pd

def download_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df.to_csv(f"{symbol}_prices.csv")
    print(f"Datos guardados en {symbol}_prices.csv")

if __name__ == "__main__":
    download_data("TSLA", "2024-01-01", "2024-06-30")
