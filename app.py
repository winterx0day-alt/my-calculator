import plotly.express as px

# --- เปลี่ยนส่วน SECTION 4: VISUALIZATION เป็นโค้ดนี้ ---
with st.expander("ดูแผนภูมิสัดส่วนรายได้", expanded=True):
    chart_df = pd.DataFrame({
        'รายการ': ['ผ่อนรวม', 'เงินออม (20%)', 'ค่าใช้จ่ายทั่วไป'],
        'จำนวนเงิน': [total_debt, savings_goal, max(0, leftover)]
    })
    
    # สร้างกราฟ Donut
    fig = px.pie(
        chart_df, 
        values='จำนวนเงิน', 
        names='รายการ', 
        hole=0.5,
        color_discrete_sequence=['#FF4B4B', '#29B045', '#0068C9'] # แดง, เขียว, น้ำเงิน
    )
    
    # ปรับแต่งให้ตัวหนังสืออยู่ในกราฟและซ่อนคำอธิบายด้านข้างเพื่อให้ดูสะอาดตา
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    
    st.plotly_chart(fig, use_container_width=True)
