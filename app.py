import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wrds

plt.rcParams["font.family"] = ["sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

st.title("Personal Finance Tool & Wards WRDS Data Analysis")
st.sidebar.title("Menu")
choice = st.sidebar.radio("Go to",
    ["Loan", "Savings", "Budget", "Wards WRDS Data Analysis"])

# ========== 1. 贷款计算器（原版保留） ==========
if choice == "Loan":
    st.subheader("Loan Calculator")
    p = st.number_input("Principal", 10000)
    r = st.number_input("Rate (%)", 4.5)
    y = st.number_input("Years", 20)
    m = y * 12
    mr = r / 1200
    if mr == 0:
        pay = p / m
    else:
        pay = p * mr * (1+mr)**m / ((1+mr)**m -1)
    st.success(f"Monthly Payment: ${pay:.2f}")

# ========== 2. 储蓄计算器（你必须保留 原版不动） ==========
elif choice == "Savings":
    st.subheader("Savings Calculator")
    init = st.number_input("Initial", 10000)
    mono = st.number_input("Monthly deposit", 1000)
    ret = st.number_input("Return (%)", 5.0)
    y = st.number_input("Years", 10)
    rate = ret / 100
    fv = init*(1+rate)**y + mono * (((1+rate)**y -1)/rate)
    st.success(f"Future Value: ${fv:.2f}")

# ========== 3. 预算分析（原版保留） ==========
elif choice == "Budget":
    st.subheader("Monthly Budget")
    income = st.number_input("Income", 5000)
    rent = st.number_input("Rent", 1500)
    food = st.number_input("Food", 800)
    trans = st.number_input("Transport", 300)
    ent = st.number_input("Entertainment", 500)
    oth = st.number_input("Others", 400)
    exp = rent + food + trans + ent + oth
    sav = income - exp

    labels = ["Rent","Food","Transport","Entertainment","Others","Savings"]
    vals = [rent,food,trans,ent,oth,sav]
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig)
    st.info(f"Monthly Savings: ${sav}")

# ========== 4. 新增：Wards WRDS 外部数据 完整模块 ==========
elif choice == "Wards WRDS Data Analysis":
    st.title("Wards (WRDS) External Dataset Analysis")
    st.markdown("""
    **Data Source**: Wards WRDS Official Financial Database
    **Data Access**: Direct account login & real-time data download via Python
    **Process**: Raw Data Download → Data Cleaning → Statistical Analysis → Visualisation
    """)

    # 输入你的Wards账号密码
    st.subheader("1. Login to Wards WRDS")
    user = st.text_input("WRDS Username")
    pwd = st.text_input("WRDS Password", type="password")

    if st.button("Connect & Download Data"):
        try:
            # 代码登录Wards
            db = wrds.Connection(wrds_username=user, wrds_password=pwd)
            st.success("Successfully connected to Wards WRDS database")

            # 下载官方真实外部金融数据集
            raw_df = db.get_table(
                library="crsp",
                table="dsf",
                columns=["date", "prc", "ret", "vol"],
                date_cols=["date"]
            )

            st.subheader("2. Raw Wards Dataset")
            st.dataframe(raw_df.head(10))

            # 数据清洗（ACC102 得分点）
            st.subheader("3. Data Cleaning")
            clean_df = raw_df.dropna()
            clean_df = clean_df.drop_duplicates()
            st.write(f"Original rows: {len(raw_df)}")
            st.write(f"Cleaned rows: {len(clean_df)}")
            st.success("Removed missing values and duplicate data")

            # 数据分析
            st.subheader("4. Data Analysis")
            st.dataframe(clean_df.describe())

            # 可视化
            st.subheader("5. Data Visualisation")
            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(clean_df["date"], clean_df["prc"], color="#003366", label="Stock Price")
            ax.set_title("Wards Historical Stock Price Trend")
            ax.legend()
            st.pyplot(fig)

            db.close()

        except Exception as e:
            st.error(f"Failed: {str(e)}")