import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Smart Installment Planner",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    /* ปรับแต่ง Font และ Background */
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
    }
    .main {
        background-color: #f8f9fa;
    }
    /* สไตล์ Card สำหรับ Metric */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* ส่วนหัว Header */
    .header-style {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUT DATA ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2489/2489756.png", width=80)
    st.title("ตั้งค่าข้อมูล")
    st.subheader("📥 ข้อมูลส่วนตัว")
    
    income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=32585, step=500)
    existing_debt = st.number_input("ยอดผ่อนอื่นๆ ที่มีอยู่ (บาท/เดือน)", min_value=0, value=0)
    
    st.divider()
    st.subheader("🛍️ สินค้าใหม่ที่ต้องการผ่อน")
    product_price = st.number_input("ราคาสินค้า (บาท)", min_value=0, value=20000)
    install_months = st.select_slider("จำนวนเดือนที่ผ่อน", options=[3, 6, 10, 12, 18, 24], value=10)

# --- CALCULATION LOGIC ---
monthly_payment = product_price / install_months if install_months > 0 else 0
total_monthly_debt = monthly_payment + existing_debt
debt_ratio = (total_monthly_debt / income) if income > 0 else 0
remaining_balance = income - total_monthly_debt
recommended_savings = income * 0.20
spending_money = remaining_balance - recommended_savings

# --- MAIN CONTENT ---
st.markdown('<div class="header-style"><h1>Smart Installment Planner</h1><p>วางแผนผ่อนชำระ 0% อย่างชาญฉลาด ไม่กระทบเงินเก็บ</p></div>', unsafe_allow_html=True)

# ROW 1: Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("ยอดผ่อนชิ้นใหม่", f"{monthly_payment:,.2f} ฿")
with col2:
    st.metric("ผ่อนรวมทั้งหมด/เดือน", f"{total_monthly_debt:,.2f} ฿")
with col3:
    st.metric("เงินคงเหลือหลังผ่อน", f"{remaining_balance:,.2f} ฿")
with col4:
    ratio_color = "normal" if debt_ratio <= 0.15 else "inverse"
    st.metric("สัดส่วนหนี้ต่อรายได้", f"{debt_ratio:.1%}", delta_color=ratio_color)

st.write("---")

# ROW 2: Status & Visualization
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.subheader("✅ สถานะการผ่อน")
    if debt_ratio <= 0.10:
        st.success("🟢 **ปลอดภัยมาก:** ยอดผ่อนไม่เกิน 10% เงินเก็บคุณยังอยู่ครบ")
    elif debt_ratio <= 0.15:
        st.warning("🟡 **พอรับได้:** เริ่มมีความเสี่ยงเล็กน้อย ควรวางแผนการใช้อื่นเพิ่ม")
    else:
        st.error("🔴 **ตึงมือเกินไป:** แนะนำให้ลดราคาสินค้าหรือเพิ่มจำนวนเดือน")
    
    st.info(f"💡 **คำแนะนำ:** เป้าเงินเก็บ 20% ของคุณคือ {recommended_savings:,.2f} ฿")

with col_right:
    st.subheader("📈 สัดส่วนการใช้เงิน")
    # สร้าง Dataframe สำหรับ Chart
    chart_data = pd.DataFrame({
        'Category': ['ผ่อนสินค้า', 'ออมเงิน (20%)', 'ค่าใช้จ่ายคงเหลือ'],
        'Amount': [total_monthly_debt, recommended_savings, max(0, spending_money)]
    })
    st.bar_chart(chart_data.set_index('Category'))

# ROW 3: Reference Table (จากตารางอ้างอิงใน Excel)
with st.expander("📊 ดูตารางอ้างอิงความปลอดภัย"):
    st.write("เกณฑ์การผ่อนที่แนะนำตามช่วงรายได้ (0% Installment Guide)")
    ref_data = {
        "ระดับความปลอดภัย": ["ปลอดภัย (10%)", "พอรับได้ (15%)", "ขีดจำกัด (20%)"],
        "ยอดผ่อนสูงสุดที่คุณทำได้": [income*0.1, income*0.15, income*0.2]
    }
    st.table(pd.DataFrame(ref_data))

st.caption("Developed by Gemini | BI Analyst Companion")
