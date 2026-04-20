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
# 2. 储蓄计算器（你必须保留的原版）
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
# 4. 【核心】Yahoo Finance 真实数据模块（替代Wards）
# ----------------------------
elif choice == "Yahoo Finance Data Analysis":
    st.title("Yahoo Finance Stock Data Analysis")
    st.markdown("""
    **Data Source**: Yahoo Finance (https://finance.yahoo.com)
    **Data Type**: Historical daily stock prices
    **Date Accessed**: """ + datetime.today().strftime('%d %B %Y') + """
    **Process**: Data Download → Cleaning → Analysis → Visualisation
    """)

    # 用户输入股票代码和日期范围
    ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, MSFT, GOOGL)", "AAPL")
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))

    if st.button("Load & Analyze Data"):
        with st.spinner("Downloading data from Yahoo Finance..."):
            # 1. 下载数据
            data = yf.download(ticker, start=start_date, end=end_date)

            if not data.empty:
                st.success("Data downloaded successfully!")

                # 2. 数据清洗（作业必写得分点）
                st.subheader("Step 1: Data Cleaning")
                data_clean = data.dropna()  # 删除空值
                data_clean['Daily Return'] = data_clean['Close'].pct_change() # 计算日收益率
                data_clean = data_clean.dropna() # 删除计算收益率后产生的空值
                st.write(f"Original Data Rows: {len(data)}")
                st.write(f"Cleaned Data Rows: {len(data_clean)}")
                st.dataframe(data_clean.head(10))

                # 3. 数据分析
                st.subheader("Step 2: Data Analysis")
                st.write(f"**Mean Closing Price**: ${data_clean['Close'].mean():.2f}")
                st.write(f"**Price Volatility (Std Dev)**: {data_clean['Daily Return'].std():.4f}")
                st.write(f"**Highest Price**: ${data_clean['Close'].max():.2f}")
                st.write(f"**Lowest Price**: ${data_clean['Close'].min():.2f}")

                # 4. 可视化
                st.subheader("Step 3: Price Trend Visualisation")
                fig, ax = plt.subplots(figsize=(10,4))
                ax.plot(data_clean.index, data_clean['Close'], label=f"{ticker} Close Price", color='blue')
                ax.set_title(f"{ticker} Stock Price Trend")
                ax.legend()
                st.pyplot(fig)
            else:
                st.error("Failed to download data. Please check the ticker symbol and try again.")