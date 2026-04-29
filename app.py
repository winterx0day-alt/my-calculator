import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG ---
st.set_page_config(page_title="Check-Porn", layout="centered")

# --- CSS (ปรับให้รันได้ทุกที่) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { text-align: center; color: #1E3A8A; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">💸 น้องช่วยเช็ก.. ผ่อนไหวไหม?</h1>', unsafe_allow_html=True)

# --- INPUT AREA ---
st.subheader("👛 ข้อมูลกระเป๋าตังค์")
income = st.number_input("รายได้ต่อเดือน (บาท)", value=30000)
existing_debt = st.number_input("ยอดที่ผ่อนอยู่อื่นๆ (บาท)", value=0)

st.subheader("🛍️ ของที่อยากได้")
product_price = st.number_input("ราคาสินค้า (บาท)", value=20000)
install_months = st.selectbox("ผ่อนกี่เดือนดี?", [3, 6, 10, 12, 18, 24], index=2)

# --- CALCULATION ---
pay_per_month = product_price / install_months
total_monthly = pay_per_month + existing_debt
ratio = (total_monthly / income) * 100 if income > 0 else 0
savings = income * 0.2
leftover = income - total_monthly - savings

# --- DISPLAY ---
st.divider()
c1, c2 = st.columns(2)
c1.metric("ยอดผ่อนใหม่", f"{pay_per_month:,.0f} ฿")
c2.metric("จ่ายรวมต่อเดือน", f"{total_monthly:,.0f} ฿")

if ratio <= 10:
    st.success(f"✨ **จัดเลย!** ภาระหนี้แค่ {ratio:.1f}% ของรายได้")
elif ratio <= 20:
    st.warning(f"⚠️ **พอไหวนะ** ภาระหนี้อยู่ที่ {ratio:.1f}%")
else:
    st.error(f"🚨 **พักก่อน!** หนี้พุ่งไปที่ {ratio:.1f}% แล้วจ้า")

# --- DONUT CHART ---
st.subheader("🍕 สัดส่วนเงิน")
data = pd.DataFrame({
    'Category': ['ผ่อนรวม', 'เงินออม', 'ใช้จ่าย'],
    'Amount': [total_monthly, savings, max(0, leftover)]
})
fig = px.pie(data, values='Amount', names='Category', hole=0.5,
             color_discrete_sequence=['#FF4B4B', '#29B045', '#0068C9'])
st.plotly_chart(fig, use_container_width=True)
