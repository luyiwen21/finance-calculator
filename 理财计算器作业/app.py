# 个人理财计算器 | Personal Finance Calculator
# ACC102 Track 4 Streamlit 作业
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 页面设置
st.set_page_config(page_title="Personal Finance Calculator", layout="wide")
st.title("Personal Finance Calculator")
st.subheader("A simple tool for loan, savings, and budget analysis")

# 侧边栏菜单
menu = st.sidebar.radio("Choose a function", 
                        ["Loan Calculator", "Savings Calculator", "Budget Analysis"])

# ----------------------
# 1. 贷款计算器
# ----------------------
if menu == "Loan Calculator":
    st.header("Loan Monthly Payment Calculator")
    principal = st.number_input("Loan amount (本金)", min_value=1000, value=100000)
    rate = st.number_input("Annual interest rate (%)", min_value=0.1, value=4.5)
    years = st.slider("Loan term (years)", 1, 30, 20)

    months = years * 12
    monthly_rate = rate / 100 / 12
    payment = principal * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)

    st.success(f"Monthly Payment: **${payment:.2f}**")

# ----------------------
# 2. 储蓄计算器
# ----------------------
elif menu == "Savings Calculator":
    st.header("Compound Savings Calculator")
    initial = st.number_input("Initial amount", value=10000)
    monthly = st.number_input("Monthly deposit", value=1000)
    annual_return = st.number_input("Annual return rate (%)", value=5.0)
    years_save = st.slider("Years", 1, 40, 10)

    r = annual_return / 100
    total = initial * (1 + r)**years_save + monthly * (((1 + r)**years_save - 1) / r)

    st.success(f"Future Value: **${total:.2f}**")

# ----------------------
# 3. 收支分析
# ----------------------
elif menu == "Budget Analysis":
    st.header("Monthly Budget & Expense Analysis")
    income = st.number_input("Monthly Income", value=5000)
    rent = st.number_input("Rent", value=1500)
    food = st.number_input("Food", value=800)
    transport = st.number_input("Transport", value=300)
    entertainment = st.number_input("Entertainment", value=500)
    others = st.number_input("Others", value=400)

    total_exp = rent + food + transport + entertainment + others
    saving = income - total_exp

    # 数据
    labels = ["Rent", "Food", "Transport", "Entertainment", "Others", "Savings"]
    values = [rent, food, transport, entertainment, others, saving]

    # 饼图
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    st.pyplot(fig)

    # 总结
    st.info(f"Total Income: ${income} | Total Expense: ${total_exp} | Savings: ${saving}")

st.markdown("---")
st.caption("ACC102 Track 4 Data Product | Personal Finance Tool")