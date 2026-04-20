import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

# 页面设置
st.set_page_config(page_title="Personal Finance Tool", layout="wide")
st.title("Personal Finance Tool & Yahoo Finance Data Analysis")
st.sidebar.title("Menu")

# 侧边栏导航
choice = st.sidebar.radio("Go to",
    ["Loan Calculator", "Savings Calculator", "Budget Analysis", "Yahoo Finance Data Analysis"])

# ----------------------------
# 1. 贷款计算器
# ----------------------------
if choice == "Loan Calculator":
    st.subheader("Loan Repayment Calculator")
    p = st.number_input("Loan Principal ($)", 10000)
    r = st.number_input("Annual Interest Rate (%)", 4.5)
    y = st.number_input("Loan Term (Years)", 20)
    m = y * 12
    mr = r / 1200
    pay = p * mr * (1+mr)**m / ((1+mr)**m -1)
    st.success(f"Monthly Payment: ${pay:.2f}")

# ----------------------------
# 2. 储蓄计算器
# ----------------------------
elif choice == "Savings Calculator":
    st.subheader("Personal Savings Future Value Calculator")
    init = st.number_input("Initial Deposit ($)", 10000)
    mono = st.number_input("Monthly Deposit ($)", 1000)
    ret = st.number_input("Annual Expected Return (%)", 5.0)
    y = st.number_input("Saving Period (Years)", 10)
    rate = ret / 100
    fv = init*(1+rate)**y + mono * (((1+rate)**y -1)/rate)
    st.success(f"Estimated Future Value: ${fv:.2f}")

# ----------------------------
# 3. 预算分析
# ----------------------------
elif choice == "Budget Analysis":
    st.subheader("Monthly Budget Analysis")
    income = st.number_input("Monthly Income ($)", 5000)
    rent = st.number_input("Rent ($)", 1500)
    food = st.number_input("Food ($)", 800)
    trans = st.number_input("Transport ($)", 300)
    ent = st.number_input("Entertainment ($)", 500)
    oth = st.number_input("Others ($)", 400)
    exp = rent + food + trans + ent + oth
    sav = income - exp

    labels = ["Rent","Food","Transport","Entertainment","Others","Savings"]
    vals = [rent,food,trans,ent,oth,sav]
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig)
    st.info(f"Monthly Savings: ${sav:.2f}")

# ----------------------------
# 4. Yahoo Finance 数据模块（完全修复版）
# ----------------------------
elif choice == "Yahoo Finance Data Analysis":
    st.title("Yahoo Finance Stock Data Analysis")
    st.markdown(f"""
    **Data Source**: Yahoo Finance (https://finance.yahoo.com)
    **Date Accessed**: {datetime.today().strftime('%d %B %Y')}
    """)

    ticker = st.text_input("Stock Ticker (e.g. AAPL, MSFT)", "AAPL")
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))

    if st.button("Load & Analyze Data"):
        with st.spinner("Downloading data..."):
            # 1. 下载数据
            data = yf.download(ticker, start=start_date, end=end_date)

            if not data.empty:
                st.success("Data downloaded successfully!")

                # 2. 处理多层索引 → 变成普通列
                data.columns = data.columns.get_level_values(0)

                # 3. 数据清洗
                st.subheader("Step 1: Data Cleaning")
                data_clean = data.dropna()
                data_clean['Daily Return'] = data_clean['Close'].pct_change()
                data_clean = data_clean.dropna()

                st.write(f"Original rows: {len(data)}")
                st.write(f"Cleaned rows: {len(data_clean)}")
                st.dataframe(data_clean.head(10))

                # 4. 数据分析（使用独立变量，彻底修复 f-string 报错）
                st.subheader("Step 2: Data Analysis")

                mean_price = data_clean['Close'].mean()
                volatility = data_clean['Daily Return'].std()
                high_price = data_clean['Close'].max()
                low_price = data_clean['Close'].min()

                st.write(f"**Mean Closing Price**: ${mean_price:.2f}")
                st.write(f"**Price Volatility (Std Dev)**: {volatility:.4f}")
                st.write(f"**Highest Price**: ${high_price:.2f}")
                st.write(f"**Lowest Price**: ${low_price:.2f}")

                # 5. 可视化
                st.subheader("Step 3: Price Trend")
                fig, ax = plt.subplots(figsize=(10,4))
                ax.plot(data_clean.index, data_clean['Close'], color='blue')
                ax.set_title(f"{ticker} Closing Price Trend")
                st.pyplot(fig)

            else:
                st.error("Data download failed. Please check the ticker symbol.")