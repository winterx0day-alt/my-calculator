import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Installment Calculator",
    page_icon="💳",
    layout="centered"  # ใช้แบบ Centered จะดูสวยและเป็นระเบียบกว่าบนมือถือ
)

# --- CUSTOM CSS FOR CLEAN & PREMIUM LOOK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
        background-color: #fcfcfc;
    }

    /* Container ปรับแต่งให้ดูเหมือน App มือถือ */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 600px; /* จำกัดความกว้างให้ดูดีทั้งบน Desktop และ Mobile */
    }

    /* ตกแต่ง Card ผลลัพธ์ */
    .stMetric {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }

    /* หัวข้อใหญ่ */
    .main-title {
        text-align: center;
        color: #1a1a1a;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 30px;
    }

    /* ส่วน Input Area */
    .input-section {
        background-color: #f1f3f6;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 25px;
    }
    
    /* ซ่อนขีดข้าง Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-title">💸 น้องช่วยคิด.. ผ่อนไหวไหม?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">เช็กให้ชัวร์ก่อนรูด จะได้มีเงินเก็บเหลือๆ ไม่ตึงมือ</p>', unsafe_allow_html=True)

# --- SECTION 1: INPUTS ---
st.markdown("### 💰 กระเป๋าตังค์ตอนนี้")
col_in1, col_in2 = st.columns(2)
with col_in1:
    income = st.number_input("รายได้เฉลี่ย/เดือน (บาท)", min_value=0, value=30000, step=1000)
with col_in2:
    existing_debt = st.number_input("ยอดที่ผ่อนอยู่อื่นๆ (บาท)", min_value=0, value=0, step=100)

st.markdown("### 🛍️ ของที่เล็งไว้")
product_price = st.number_input("ค่าตัวน้องคนนี้ (บาท)", min_value=0, value=20000)
install_months = st.select_slider("กะจะผ่อนสักกี่เดือน?", options=[3, 6, 10, 12, 18, 24], value=10)

st.write("---")

# --- CALCULATION (คงเดิมไว้) ---
monthly_payment = product_price / install_months if install_months > 0 else 0
total_debt = monthly_payment + existing_debt
debt_ratio = (total_debt / income) if income > 0 else 0
savings_goal = income * 0.20
leftover = income - total_debt - savings_goal

# --- SECTION 2: RESULTS (Metrics) ---
st.markdown("### ✨ สรุปยอดออกมาแล้ว!")
m_col1, m_col2 = st.columns(2)
with m_col1:
    st.metric("ยอดผ่อนใหม่/เดือน", f"{monthly_payment:,.0f} ฿")
with m_col2:
    st.metric("รวมต้องจ่ายต่อเดือน", f"{total_debt:,.0f} ฿")

m_col3, m_col4 = st.columns(2)
with m_col3:
    st.metric("สัดส่วนหนี้ต่อรายได้", f"{debt_ratio:.1%}")
with m_col4:
    st.metric("เงินเหลือไว้กินช้อป", f"{max(0, leftover):,.0f} ฿")

# --- SECTION 3: STATUS & ADVICE (ปรับคำให้ดูเป็นเพื่อน) ---
st.write("")
if debt_ratio <= 0.10:
    st.success("✅ **สถานะ: ชิลมาก จัดเลย!**\n\nยอดผ่อนเบาๆ ไม่กระทบเงินเก็บ สบายใจได้จ้า")
elif debt_ratio <= 0.20:
    st.warning("⚠️ **สถานะ: พอไหวนะ แต่ต้องระวัง**\n\nเริ่มเข้าใกล้ขีดจำกัดแล้ว อย่าเพิ่งงอกของเพิ่มน้า")
else:
    st.error("🚨 **สถานะ: พักก่อน! ตึงมือไปหน่อย**\n\nยอดผ่อนสูงเกิน 20% ของรายได้ ลองเพิ่มเดือนผ่อนหรือลดงบดูก่อนนะ")

# --- SECTION 4: VISUALIZATION ---
with st.expander("📊 เปิดดูภาพรวมเงินในกระเป๋า", expanded=True):
    chart_df = pd.DataFrame({
        'รายการ': ['ผ่อนรวม', 'เงินออม (20%)', 'เงินใช้จ่าย'],
        'จำนวนเงิน': [total_debt, savings_goal, max(0, leftover)]
    })
    st.bar_chart(chart_df.set_index('รายการ'))
