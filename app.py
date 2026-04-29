import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Installment Calculator",
    page_icon="💳",
    layout="centered"  # ใช้แบบ Centered จะดูสวยและเป็นระเบียบกว่าบนมือถือ
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
st.markdown('<h1 class="main-title">เครื่องคำนวณผ่อน 0%</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">วางแผนการเงินส่วนตัวตามหลักความปลอดภัย 10-20%</p>', unsafe_allow_html=True)

# --- SECTION 1: INPUTS (วางหน้าหลักแบบยาว) ---
st.markdown("### 📥 ข้อมูลการเงิน")
col_in1, col_in2 = st.columns(2)
with col_in1:
    income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=30000, step=1000)
with col_in2:
    existing_debt = st.number_input("ยอดผ่อนเดิมที่มี (บาท)", min_value=0, value=0, step=100)

st.markdown("### 🛍️ รายละเอียดสินค้า")
product_price = st.number_input("ราคาสินค้าที่จะซื้อ (บาท)", min_value=0, value=20000)
install_months = st.select_slider("ระยะเวลาผ่อนชำระ (เดือน)", options=[3, 6, 10, 12, 18, 24], value=10)

st.write("---")

# --- CALCULATION ---
monthly_payment = product_price / install_months if install_months > 0 else 0
total_debt = monthly_payment + existing_debt
debt_ratio = (total_debt / income) if income > 0 else 0
savings_goal = income * 0.20
leftover = income - total_debt - savings_goal

# --- SECTION 2: RESULTS (Metrics) ---
st.markdown("### 📊 ผลการคำนวณ")
m_col1, m_col2 = st.columns(2)
with m_col1:
    st.metric("ยอดผ่อนใหม่/เดือน", f"{monthly_payment:,.0f} ฿")
with m_col2:
    st.metric("ภาระหนี้รวม/เดือน", f"{total_debt:,.0f} ฿")

m_col3, m_col4 = st.columns(2)
with m_col3:
    st.metric("% ที่ใช้ผ่อนรายได้", f"{debt_ratio:.1%}")
with m_col4:
    st.metric("เงินเหลือใช้หลังเก็บออม", f"{max(0, leftover):,.0f} ฿")

# --- SECTION 3: STATUS & ADVICE ---
st.write("")
if debt_ratio <= 0.10:
    st.success("✅ **สถานะ: ปลอดภัยมาก**\n\nยอดผ่อนอยู่ในเกณฑ์ดีเยี่ยม ไม่กระทบแผนการเงิน")
elif debt_ratio <= 0.20:
    st.warning("⚠️ **สถานะ: พอรับได้**\n\nเริ่มเข้าใกล้ขีดจำกัด ควรระมัดระวังค่าใช้จ่ายอื่น")
else:
    st.error("🚨 **สถานะ: ตึงมือเกินไป**\n\nยอดผ่อนสูงเกิน 20% ของรายได้ แนะนำให้เพิ่มเวลาผ่อนหรือลดงบประมาณ")

# --- SECTION 4: VISUALIZATION ---
with st.expander("ดูแผนภูมิสัดส่วนรายได้", expanded=True):
    chart_df = pd.DataFrame({
        'รายการ': ['ผ่อนรวม', 'เงินออม (20%)', 'ค่าใช้จ่ายทั่วไป'],
        'จำนวนเงิน': [total_debt, savings_goal, max(0, leftover)]
    })
    st.bar_chart(chart_df.set_index('รายการ'))

# --- FOOTER ---
st.write("---")
st.caption("วางแผนการเงินอย่างยั่งยืน | ตารางอ้างอิงอิงตามหลักความเสี่ยงสูงสุดไม่เกิน 20%")
