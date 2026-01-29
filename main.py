import os
import ssl

# 這裡解決抓取資料時的憑證問題
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

import os
import ssl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

# 解決憑證問題
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI() # 必須先定義 app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 你的持股資料
MY_PORTFOLIO = {
    "0050.TW": {"name": "元大台灣50"},
    "0056.TW": {"name": "元大高股息"},
    "006208.TW": {"name": "富邦台50"},
    "00679B.TW": {"name": "元大美債20年"},
    "00878.TW": {"name": "國泰永續高股息"}
}

@app.get("/api/stocks")
def get_stocks():
    results = []
    for symbol, info in MY_PORTFOLIO.items():
        try:
            stock = yf.Ticker(symbol)
            # 抓取歷史至今所有數據
            hist_all = stock.history(period="max")
            
            if hist_all.empty or len(hist_all) < 252:
                continue
                
            hist_1y = hist_all.tail(252)
            hist_6m = hist_all.tail(126)
            
            current_price = hist_all['Close'].iloc[-1]
            
            results.append({
                "symbol": symbol,
                "name": info['name'],
                "price": round(current_price, 2),
                "volume": int(hist_all['Volume'].iloc[-1]),
                "max_6m": round(hist_6m['High'].max(), 2),
                "min_6m": round(hist_6m['Low'].min(), 2),
                "max_1y": round(hist_1y['High'].max(), 2),
                "min_1y": round(hist_1y['Low'].min(), 2),
                "max_hist": round(hist_all['High'].max(), 2),
                "min_hist": round(hist_all['Low'].min(), 2),
            })
        except Exception as e:
            print(f"抓取 {symbol} 失敗: {e}")
            continue
    return results