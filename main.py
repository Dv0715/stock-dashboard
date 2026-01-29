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

# 更新你的持股字典 (填入你之前 Excel 中的數據)
MY_PORTFOLIO = {
    "0050.TW": {"name": "元大台灣50", "avg_cost": 50.99, "shares": 2170},
    "0056.TW": {"name": "元大高股息", "avg_cost": 35.78, "shares": 1650},
    "006208.TW": {"name": "富邦台50", "avg_cost": 109.81, "shares": 525},
    "00679B.TW": {"name": "元大美債20年", "avg_cost": 28.0, "shares": 2365},
}



# ... (保留原本的 import 與 CORS 設定)
@app.get("/api/stocks")
def get_stocks():
    results = []
    # 填入你的投資均價與股數，讓損益不再是 undefined
    MY_PORTFOLIO = {
        "0050.TW": {"name": "元大台灣50", "avg": 50.99, "shares": 2170},
        "0056.TW": {"name": "元大高股息", "avg": 35.78, "shares": 1650},
        "006208.TW": {"name": "富邦台50", "avg": 109.81, "shares": 525},
        "00679B.TW": {"name": "元大美債20年", "avg": 28.0, "shares": 2365}
    }

    for symbol, info in MY_PORTFOLIO.items():
        try:
            stock = yf.Ticker(symbol)
            hist_all = stock.history(period="max")
            if hist_all.empty: continue
            
            # 定義時間切片 (週: 5, 三月: 63)
            hist_1y = hist_all.tail(252)
            hist_6m = hist_all.tail(126)
            hist_3m = hist_all.tail(63)
            hist_1w = hist_all.tail(5)
            
            current_price = hist_all['Close'].iloc[-1]
            prev_price = hist_all['Close'].iloc[-2]
            
            # 損益計算
            profit_pct = ((current_price - info['avg']) / info['avg']) * 100
            current_value = current_price * info['shares']

            results.append({
                "symbol": symbol,
                "name": info['name'],
                "price": round(current_price, 2),
                "change_daily": round(((current_price - prev_price) / prev_price) * 100, 2),
                "profit_pct": round(profit_pct, 2),
                "max_1w": round(hist_1w['High'].max(), 2), "min_1w": round(hist_1w['Low'].min(), 2),
                "max_3m": round(hist_3m['High'].max(), 2), "min_3m": round(hist_3m['Low'].min(), 2),
                "max_6m": round(hist_6m['High'].max(), 2), "min_6m": round(hist_6m['Low'].min(), 2),
                "max_1y": round(hist_1y['High'].max(), 2), "min_1y": round(hist_1y['Low'].min(), 2),
                "sparkline": hist_all['Close'].tail(30).tolist(), # 最近 30 天數據
                "market_value": round(current_value, 0)
            })
        except Exception as e: print(f"Error {symbol}: {e}")
    return results