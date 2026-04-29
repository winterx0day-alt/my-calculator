import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG ---
st.set_page_config(page_title="Check-Porn", layout="centered")

# --- CSS: ปรับ UI ให้เนี๊ยบขึ้น ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .main-title { text-align: center; color: #1E3A8A; font-weight: bold; margin-bottom: 20px; }
    /* ปรับแต่ง Metric ให้ดูเด่นขึ้น */
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💸 น้องช่วยเช็ก.. ผ่อนไหวไหม?</h1>', unsafe_allow_html=True)

# --- INPUT AREA ---
with st.container():
    st.subheader("👛 เล่ารายได้ให้ฟังหน่อย")
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=30000, step=1000)
    with col_in2:
        existing_debt = st.number_input("ยอดที่ผ่อนอยู่อื่นๆ (บาท)", min_value=0, value=0, step=100)

    st.subheader("🛍️ ของที่อยากได้รอบนี้")
    col_in3, col_in4 = st.columns(2)
    with col_in3:
        product_price = st.number_input("ราคาสินค้า (บาท)", min_value=0, value=20000)
    with col_in4:
        install_months = st.selectbox("ผ่อนกี่เดือนดี?", [3, 6, 10, 12, 18, 24], index=2)

# --- CALCULATION ---
if income > 0:
    pay_per_month = product_price / install_months
    total_monthly = pay_per_month + existing_debt
    ratio = (total_monthly / income) * 100
    savings = income * 0.20
    # คำนวณเงินคงเหลือโดยไม่ให้ติดลบ
    leftover = max(0, income - total_monthly - savings)

    # --- DISPLAY ---
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("ยอดผ่อนชิ้นใหม่", f"{pay_per_month:,.0f} ฿")
    c2.metric("ภาระหนี้รวม/เดือน", f"{total_monthly:,.0f} ฿")

    if ratio <= 10:
        st.success(f"✨ **จัดเลย! ปลอดภัยมาก** | ภาระหนี้ทั้งหมด {ratio:.1f}% ของรายได้")
    elif ratio <= 20:
        st.warning(f"⚠️ **พอรับได้นะ** | ภาระหนี้รวม {ratio:.1f}% เริ่มต้องระวังแล้ว")
    else:
        st.error(f"🚨 **พักก่อนดีไหม?** | หนี้สูงถึง {ratio:.1f}% ของรายได้ จะตึงมือเกินไปนะ")

    # --- DONUT CHART ---
    st.subheader("🍕 สัดส่วนเงินของคุณ")
    data = pd.DataFrame({
        'รายการ': ['ภาระผ่อนรวม', 'เงินออม (20%)', 'เงินเหลือใช้จ่าย'],
        'จำนวนเงิน': [total_monthly, savings, leftover]
    })
    
    fig = px.pie(data, values='จำนวนเงิน', names='รายการ', hole=0.5,
                 color_discrete_sequence=['#FF4B4B', '#29B045', '#0068C9'])
    
    # ปรับให้โชว์ Legend ด้านล่างและแสดง % ในกราฟ (เหมาะกับมือถือ)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 กรุณากรอกรายได้เพื่อเริ่มคำนวณจ้า")

st.divider()
st.caption("วางแผนการเงินดี ชีวิตแฮปปี้ | พัฒนาด้วย Streamlit & Plotly")
