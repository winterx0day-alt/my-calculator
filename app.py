from streamlit_gsheets import GSheetsConnection

# ฟังก์ชันกลางสำหรับบันทึกข้อมูลแบบเงียบ (Silent Logger)
def silent_log(data_type, payload=None):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # เลือก Worksheet ตามประเภทกิจกรรม
        sheet_name = "visits" if data_type == "visit" else "calculations"
        
        # ดึงข้อมูลเดิม
        df = conn.read(worksheet=sheet_name).dropna(how="all")
        
        # เตรียม Data ใหม่
        new_entry = {"Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}
        if payload:
            new_entry.update(payload)
            new_entry["Event_Type"] = "Calculation"
        else:
            new_entry["Event_Type"] = "Visit"
            
        # รวมและอัปเดต
        updated_df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        conn.update(worksheet=sheet_name, data=updated_df)
    except:
        pass # ปล่อยผ่านหากบันทึกไม่ได้ เพื่อไม่ให้หน้าเว็บค้างหรือแสดง Error

import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(
    page_title="น้องช่วยคิด.. ผ่อนไหวไหม?",
    page_icon="💸",
    layout="centered" 
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
        background-color: #fcfcfc;
    }

    .header-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #eee;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    .main-title { color: #1E3A8A; font-weight: 600; margin-bottom: 5px; }
    .sub-title { color: #666; font-size: 1rem; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">💸 น้องช่วยคิด.. ผ่อนไหวไหม?</h1>
        <p class="sub-title">เช็กให้ชัวร์ก่อนรูด จะได้มีเงินเก็บเหลือๆ ไม่ตึงมือ</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION 1: INPUTS ---
st.markdown("### 💰 กระเป๋าตังค์ตอนนี้")
col_in1, col_in2 = st.columns(2)
with col_in1:
    income = st.number_input("รายได้เฉลี่ย/เดือน (บาท)", min_value=0, value=20000, step=1000)
with col_in2:
    existing_debt = st.number_input("ยอดที่ผ่อนอยู่อื่นๆ (บาท)", min_value=0, value=0, step=100)

st.markdown("### 🛍️ ของที่เล็งไว้")
col_in3, col_in4 = st.columns(2)
with col_in3:
    product_price = st.number_input("ค่าตัวน้องคนนี้ (บาท)", min_value=0, value=20000)
with col_in4:
    install_months = st.selectbox("กะจะผ่อนสักกี่เดือน?", [3, 6, 10, 12, 18, 24], index=2)

st.write("---")

# --- CALCULATION ---
if income > 0:
    pay_per_month = product_price / install_months
    total_debt = pay_per_month + existing_debt
    debt_ratio = (total_debt / income)
    savings_goal = income * 0.20
    leftover = max(0, income - total_debt - savings_goal)

    # --- SECTION 2: RESULTS ---
    st.markdown("### ✨ สรุปยอดออกมาแล้ว!")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("ยอดผ่อนชิ้นใหม่", f"{pay_per_month:,.0f} ฿")
    with m_col2:
        st.metric("รวมต้องจ่ายต่อเดือน", f"{total_debt:,.0f} ฿")

    m_col3, m_col4 = st.columns(2)
    with m_col3:
        st.metric("สัดส่วนหนี้ต่อรายได้", f"{debt_ratio:.1%}")
    with m_col4:
        st.metric("เงินเหลือไว้กินช้อป", f"{leftover:,.0f} ฿")

    # --- SECTION 3: STATUS & ADVICE ---
    st.write("")
    if debt_ratio <= 0.10:
        st.success("✅ **สถานะ: ชิลมาก จัดเลย!**\n\nยอดผ่อนเบาๆ ไม่กระทบเงินเก็บ สบายใจได้จ้า")
    elif debt_ratio <= 0.20:
        st.warning("⚠️ **สถานะ: พอไหวนะ แต่ต้องระวัง**\n\nเริ่มเข้าใกล้ขีดจำกัดแล้ว อย่าเพิ่งงอกของเพิ่มน้า")
    else:
        st.error("🚨 **สถานะ: พักก่อน! ตึงมือไปหน่อย**\n\nยอดผ่อนสูงเกิน 20% ของรายได้ ลองเพิ่มเดือนผ่อนดูนะ")

    # --- SECTION 4: VISUALIZATION (แสดง % และ จำนวนเงินในกราฟสีแยกกัน) ---
    st.write("")
    with st.expander("📊 เปิดดูภาพรวมเงินในกระเป๋า", expanded=True):
        # คำนวณเปอร์เซ็นต์
        p_debt = (total_debt / income) * 100
        p_save = (savings_goal / income) * 100
        p_spend = (leftover / income) * 100

        # เตรียมข้อมูลสำหรับกราฟ โดยใส่ค่า % และ จำนวนเงินไว้ที่ชื่อ Label เลย
        data = {
            f'ยอดผ่อนรวม ({p_debt:.1f}% | {total_debt:,.0f} ฿)': [total_debt, 0, 0],
            f'เงินออม 20% ({p_save:.1f}% | {savings_goal:,.0f} ฿)': [0, savings_goal, 0],
            f'เงินกินช้อป ({p_spend:.1f}% | {leftover:,.0f} ฿)': [0, 0, leftover]
        }
        
        chart_df = pd.DataFrame(data, index=['ผ่อน', 'ออม', 'ใช้จ่าย'])
        
        # แสดงกราฟแท่งแบบแยกสีชัดเจน
        # Streamlit จะดึงสีที่แตกต่างกันให้โดยอัตโนมัติเมื่อข้อมูลอยู่คนละ Column
        st.bar_chart(chart_df)
        st.caption("💡 กราฟแสดงสัดส่วนเงินแต่ละก้อนเทียบกับรายได้ทั้งหมดของคุณ")

else:
    st.info("👆 รบกวนกรอกรายได้ก่อนน้า น้องจะได้ช่วยคำนวณให้จ้า")

# --- FOOTER ---
st.write("---")
st.markdown("<p style='text-align: center; color: #aaa; font-size: 0.8rem;'>วางแผนการเงินดี ชีวิตแฮปปี้ :) <br> อ้างอิงหลักการผ่อนไม่เกิน 20% ของรายได้</p>", unsafe_allow_html=True)
