import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Installment Calculator", layout="centered")

st.title("📊 เครื่องมือคำนวณการผ่อน 0% ฉบับคุมเงินเก็บ")
st.write("คำนวณหาจุดสมดุล เพื่อให้คุณผ่อนของที่อยากได้โดยไม่กระทบแผนการเงิน")

# ส่วนรับข้อมูล (Input)
price = st.number_input("ราคาสินค้า (บาท)", min_value=0, value=10000, step=500)
months = st.slider("จำนวนเดือนที่ผ่อน (0%)", 3, 48, 10)
savings_per_month = st.number_input("เงินเก็บปกติของคุณต่อเดือน (บาท)", min_value=0, value=5000)

# สูตรคำนวณ (ซ่อนอยู่หลังบ้าน)
installment_step = price / months
remaining_savings = savings_per_month - installment_step
impact_percent = (installment_step / savings_per_month) * 100 if savings_per_month > 0 else 0

# ส่วนแสดงผล (Output)
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.metric("ยอดผ่อนต่อเดือน", f"{installment_step:,.2f} บาท")

with col2:
    st.metric("เงินเก็บคงเหลือ", f"{remaining_savings:,.2f} บาท", delta_color="normal")

# การแจ้งเตือนเชิงวิเคราะห์ (Data Insight)
if impact_percent > 50:
    st.error(f"⚠️ คำเตือน: ยอดผ่อนนี้ดึงเงินเก็บคุณไปถึง {impact_percent:.1f}% อาจเสี่ยงเกินไป!")
elif impact_percent > 30:
    st.warning(f"⚠️ ยอดผ่อนคิดเป็น {impact_percent:.1f}% ของเงินเก็บ อยู่ในระดับที่ต้องระวัง")
else:
    st.success(f"✅ ยอดผ่อนชิลล์มาก! กระทบเงินเก็บเพียง {impact_percent:.1f}% เท่านั้น")