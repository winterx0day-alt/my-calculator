import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(
    page_title="น้องช่วยคำนวณผ่อน",
    page_icon="💸",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 550px;
    }

    /* ตกแต่งปุ่มและช่องกรอกข้อมูล */
    .stNumberInput, .stSelectbox {
        border-radius: 10px;
    }

    /* ปรับแต่งส่วนหัว */
    .header-box {
        text-align: center;
        background: #ffffff;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    /* ซ่อนขีดข้าง Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-box">
        <h2 style='margin-bottom:0;'>💸 น้องช่วยเช็ก.. ผ่อนไหวไหม?</h2>
        <p style='color: #777;'>คำนวณยอดผ่อน 0% ง่ายๆ ให้ชีวิตไม่ตึงเกินไป</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION 1: INPUTS (Friendly Tone) ---
st.markdown("### 👛 เล่ารายได้ให้ฟังหน่อย")
col_in1, col_in2 = st.columns(2)
with col_in1:
    income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=30000, step=1000, help="เงินเดือนหรือรายรับเฉลี่ยของคุณ")
with col_in2:
    existing_debt = st.number_input("มีของที่ผ่อนอยู่แล้วไหม (บาท)", min_value=0, value=0, step=100, help="ยอดผ่อนสินค้าอื่นๆ ต่อเดือนถ้ามี")

st.markdown("### 🛍️ ของที่อยากได้รอบนี้")
product_price = st.number_input("ราคาสินค้าตัวนี้ (บาท)", min_value=0, value=20000)
install_months = st.select_slider("กะจะผ่อนสักกี่เดือนดี?", options=[3, 6, 10, 12, 18, 24], value=10)

st.write("")

# --- CALCULATION ---
monthly_payment = product_price / install_months if install_months > 0 else 0
total_debt = monthly_payment + existing_debt
debt_ratio = (total_debt / income) if income > 0 else 0
savings_goal = income * 0.20
leftover = income - total_debt - savings_goal

# --- SECTION 2: RESULTS ---
st.markdown("### 📊 สรุปยอดออกมาแล้วจ้า")
m_col1, m_col2 = st.columns(2)
with m_col1:
    st.metric("ยอดผ่อนชิ้นนี้/เดือน", f"{monthly_payment:,.0f} ฿")
with m_col2:
    st.metric("รวมแล้วต้องจ่าย/เดือน", f"{total_debt:,.0f} ฿")

# --- STATUS ADVICE (Friendly) ---
if debt_ratio <= 0.10:
    st.success(f"✨ **จัดเลย! ปลอดภัยสุดๆ**\n\nยอดผ่อนทั้งหมดแค่ {debt_ratio:.1%} ของรายได้เอง สบายมากจ้า")
elif debt_ratio <= 0.20:
    st.warning(f"⚠️ **พอไหวนะ แต่เริ่มต้องระวัง**\n\nตอนนี้ยอดผ่อนรวมคิดเป็น {debt_ratio:.1%} ของรายได้ อย่าลืมเผื่อเงินไว้ใช้ฉุกเฉินด้วยนะ")
else:
    st.error(f"🚨 **โห.. แนะนำว่าพักก่อน!**\n\nตอนนี้ยอดผ่อนสูงถึง {debt_ratio:.1%} ของรายได้แล้วนะ มันจะตึงมือเกินไป ลองลดสเปกหรือรออีกนิดดีไหม?")

# --- SECTION 3: DONUT CHART (Premium Visualization) ---
st.write("")
st.markdown("### 🍕 สัดส่วนเงินของคุณ")

# เตรียมข้อมูลสำหรับกราฟ
chart_data = pd.DataFrame({
    'รายการ': ['ค่าผ่อนทั้งหมด', 'เงินเก็บออม (20%)', 'เงินเหลือใช้จ่าย'],
    'จำนวนเงิน': [total_debt, savings_goal, max(0, leftover)]
})

# สร้างกราฟ Donut ด้วย Plotly
fig = px.pie(
    chart_data, 
    values='จำนวนเงิน', 
    names='รายการ',
    hole=0.5, # ทำให้เป็นวงกลมมีรู (Donut)
    color_discrete_sequence=['#FF4B4B', '#29B045', '#0068C9'] # สีแดง(หนี้), เขียว(ออม), น้ำเงิน(ใช้จ่าย)
)

# ปรับแต่งการแสดงผลกราฟ
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0),
    height=350
)

st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.write("---")
st.markdown(
    "<div style='text-align: center; color: #aaa; font-size: 0.8rem;'>"
    "วางแผนการเงินดี ชีวิตก็แฮปปี้ :) <br>อ้างอิงหลักการผ่อนไม่เกิน 20% เพื่อความปลอดภัย"
    "</div>", 
    unsafe_allow_html=True
)
