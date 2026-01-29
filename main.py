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

# 在 results.append 之前，為每個時段準備 K線數據 (以 1週為例)
def get_ohlc_data(df):
    return df[['Open', 'High', 'Low', 'Close']].values.tolist()


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
        "0050.TW": {"name": "元大台灣50", "avg": 57.31, "shares": 4360},
        "0056.TW": {"name": "元大高股息", "avg": 35.78, "shares": 1650},
        "006208.TW": {"name": "富邦台50", "avg": 0, "shares": 0},
        "00878.TW": {"name": "國泰永續高股息", "avg": 22.02, "shares": 3246},
        "00919.TW": {"name": "群益台灣精選高息", "avg": 0, "shares": 0},
        "00929.TW": {"name": "復華台灣科技", "avg": 0, "shares": 0},
        "00687B.TW": {"name": "國泰20年美債", "avg": 0, "shares": 0},
        "00733.TW": {"name": "富邦臺灣中小", "avg": 0, "shares": 0},

        "00937B.TW": {"name": "群益ESG投等債20+", "avg": 0, "shares": 0},
        "00679B.TW": {"name": "元大美債", "avg": 27.78, "shares": 3065},
        "00712.TW": {"name": "復華富時不動產", "avg": 0, "shares": 0},
        "00713.TW": {"name": "元大高息低波", "avg": 0, "shares": 0},
        "6219.TW": {"name": "富旺", "avg": 0, "shares": 0},
        "9906.TW": {"name": "復華台灣科技", "avg": 0, "shares": 0},
        "00687B.TW": {"name": "欣巴巴", "avg": 0, "shares": 0},
        "2882.TW": {"name": "國泰金", "avg": 0, "shares": 0},

        "00939.TW": {"name": "統一台灣", "avg": 0, "shares": 0},
        "2352.TW": {"name": "佳世達", "avg": 0, "shares": 0},
        "2603.TW": {"name": "長榮海運", "avg": 0, "shares": 0},
        "2646.TW": {"name": "星宇航空", "avg": 25.66, "shares": 900},
        "2734.TW": {"name": "易飛網", "avg": 25.89, "shares": 2270},
        "2883.TW": {"name": "開發金", "avg": 0, "shares": 0},
        "3231.TW": {"name": "緯創", "avg": 149.77, "shares": 130},
        "3687.TW": {"name": "歐買尬", "avg": 0, "shares": 0},
       
        "4743.TW": {"name": "合一", "avg": 0, "shares": 0},
        "6446.TW": {"name": "藥華藥", "avg": 0, "shares": 0},
        "2363.TW": {"name": "矽統", "avg": 0, "shares": 0},
        "2409.TW": {"name": "友達", "avg": 15.34, "shares": 750},
        "2618.TW": {"name": "長榮航", "avg": 41.27, "shares": 670},
        "2734.TW": {"name": "山富", "avg": 85.11, "shares": 595},
        "6219.TW": {"name": "富旺", "avg": 0, "shares": 0},
        "2317.TW": {"name": "鴻海", "avg": 241.39, "shares": 200},

        "5347.TW": {"name": "世界", "avg": 50.99, "shares": 2170},
        "3293.TW": {"name": "鈊象電子", "avg": 775.94, "shares": 64},
        "1438.TW": {"name": "三地開發", "avg": 109.81, "shares": 525},
        "3051.TW": {"name": "力特", "avg": 28.0, "shares": 2365},
        "2376.TW": {"name": "技嘉", "avg": 50.99, "shares": 2170},
        "6462.TW": {"name": "神盾", "avg": 35.78, "shares": 1650},

        "00858.TW": {"name": "永豐美國500大", "avg": 34.51, "shares": 160},
        "00887.TW": {"name": "永豐中國50大", "avg": 13.13, "shares": 358},
        "00916.TW": {"name": "國泰全球品牌50", "avg": 26.58, "shares": 680},
        "00936.TW": {"name": "台新永續高息中小", "avg": 15.81, "shares": 450},
        "2002.TW": {"name": "中鋼", "avg": 20.28, "shares": 862},
        "2330.TW": {"name": "台積電", "avg": 1677.5, "shares": 8},
        "2337.TW": {"name": "旺宏", "avg": 88.7, "shares": 1000},
        "2344.TW": {"name": "華邦電", "avg": 127, "shares": 50},
        "2371.TW": {"name": "大同", "avg": 39.65, "shares": 120},
        "2537.TW": {"name": "聯上發", "avg": 12.83, "shares": 680},
        "2540.TW": {"name": "愛山林", "avg": 55.41, "shares": 320},
        "2603.TW": {"name": "長榮", "avg": 190.25, "shares": 1515},
        "2615.TW": {"name": "萬海", "avg": 84.67, "shares": 300},
        "2634.TW": {"name": "漢翔", "avg": 64.38, "shares": 320},
        "2739.TW": {"name": "寒舍", "avg": 54.29, "shares": 878},
        "3481.TW": {"name": "群創", "avg": 28.75, "shares": 1000},
        "3706.TW": {"name": "神達", "avg": 93.78, "shares": 420},
        "4510.TW": {"name": "高鋒", "avg": 54.72, "shares": 200},
        "4946.TW": {"name": "辣椒", "avg": 135.5, "shares": 60},
        "6550.TW": {"name": "北極星藥業", "avg": 49.78, "shares": 1114},
        "6770.TW": {"name": "力積電", "avg": 64.85, "shares": 2000},
        "6869.TW": {"name": "雲豹能源", "avg": 159.85, "shares": 315},
        "8422.TW": {"name": "可寧衛", "avg": 43.7, "shares": 120},
        "9906.TW": {"name": "欣巴巴", "avg": 84.66, "shares": 568},
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
                "market_value": round(current_value, 0),
                "ohlc_1w": get_ohlc_data(hist_1w),
    "ohlc_3m": get_ohlc_data(hist_3m.tail(20)), # 取最近20筆避免太擠
    "ohlc_6m": get_ohlc_data(hist_6m.tail(20)),
    "ohlc_1y": get_ohlc_data(hist_1y.tail(20))
            })
        except Exception as e: print(f"Error {symbol}: {e}")
    return results