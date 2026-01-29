import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 設定你持有的代號 (加上 .TW 後綴)
tickers = ['0050.TW', '0056.TW', '006208.TW', '00679B.TW', '00878.TW']

def get_data(list_of_tickers):
    data_list = []
    for t in list_of_tickers:
        stock = yf.Ticker(t)
        hist = stock.history(period="1y") # 抓取一年數據
        
        current_price = hist['Close'].iloc[-1]
        high_1y = hist['High'].max()
        # 計算距離一年高點落差 %
        drop_from_high = ((current_price - high_1y) / high_1y) * 100
        
        data_list.append({
            "代號": t,
            "現價": round(current_price, 2),
            "一年最高": round(high_1y, 2),
            "距高點落差 %": f"{round(drop_from_high, 2)}%"
        })
    return pd.DataFrame(data_list)

# 2. 建立 Streamlit 介面
st.title("📈 我的專屬投資儀表板")

if st.button('更新數據'):
    df = get_data(tickers)
    # 使用 st.dataframe 讓表格美觀且可排序
    st.dataframe(df.style.highlight_max(axis=0, subset=['現價']))