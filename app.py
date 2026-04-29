import streamlit as st

st.set_page_config(page_title="0% Installment Calculator", layout="centered")

# --- Header ---
st.title("🏦 ตารางคำนวณการผ่อนสินค้า 0%")
st.subheader("ผ่อนให้ไม่กระทบเงินเก็บ | ดอกเบี้ย 0%")
st.markdown("---")

# --- ส่วนที่ 1: กรอกข้อมูล (Input) ---
st.header("📥 กรอกข้อมูลของคุณ")
col1, col2 = st.columns(2)

with col1:
    price = st.number_input("ราคาสินค้า (บาท)", min_value=0, value=20000, step=1000)
    months = st.number_input("จำนวนเดือนที่ผ่อน", min_value=1, value=10, step=1)

with col2:
    income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=30000, step=1000)
    other_installments = st.number_input("ยอดผ่อนอื่นๆ ที่มีอยู่/เดือน (บาท)", min_value=0, value=0, step=100)

# --- Logic การคำนวณ (อ้างอิงจากไฟล์ Excel) ---
new_installment = price / months
total_installment = new_installment + other_installments
income_ratio = (total_installment / income) if income > 0 else 0
remaining_after_pay = income - total_installment
recommended_savings = income * 0.20 # เป้าเงินเก็บ 20% ตามไฟล์ Excel
spending_balance = remaining_after_pay - recommended_savings

# --- ส่วนที่ 2: ผลการคำนวณ (Result) ---
st.header("📊 ผลการคำนวณ")
res1, res2 = st.columns(2)

with res1:
    st.metric("ยอดผ่อนต่อเดือน (สินค้าใหม่)", f"{new_installment:,.2f} บาท")
    st.metric("ยอดผ่อนรวมทั้งหมด/เดือน", f"{total_installment:,.2f} บาท")
    st.metric("% ของรายได้ที่ใช้ผ่อน", f"{income_ratio:.2%}")

with res2:
    st.metric("เงินคงเหลือหลังผ่อน", f"{remaining_after_pay:,.2f} บาท")
    st.metric("เป้าเงินเก็บแนะนำ (20%)", f"{recommended_savings:,.2f} บาท")
    st.metric("เงินเหลือใช้จ่ายหลังเก็บ", f"{spending_balance:,.2f} บาท")

# --- ส่วนที่ 3: สถานะการผ่อน (Status) ---
st.divider()
st.header("✅ สถานะการผ่อน")

if income_ratio > 0.40:
    st.error(f"❌ หนี้สินสูงเกินไป ({(income_ratio*100):.1f}% ของรายได้) ไม่แนะนำให้ผ่อนเพิ่ม")
elif spending_balance < 0:
    st.warning("⚠️ ผ่อนได้แต่เงินเก็บจะลดลง หรือไม่พอเก็บ 20% ตามเป้าหมาย")
else:
    st.success("✅ สถานะทางการเงินปลอดภัย สามารถผ่อนได้ตามแผน")

# เพิ่มข้อมูลสรุปท้ายตาราง
st.info(f"ราคารวมที่จ่ายทั้งหมด: {price:,.2f} บาท (ดอกเบี้ย 0%)")
