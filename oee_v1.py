# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime

# # 페이지 설정
# st.set_page_config(page_title="식품제조 OEE 대시보드", layout="wide")

# # CSS 스타일 적용
# st.markdown("""
# <style>
#     .reportview-container .main .block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 2rem;}
#     .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
#     .stMetric:hover {background-color: #e0e2e6;}
#     .st-emotion-cache-10trblm {font-size: 1.5rem;}
# </style>
# """, unsafe_allow_html=True)

# # OEE 계산 함수
# def calculate_oee(planned_production_time, actual_run_time, actual_output, standard_cycle_time, total_production, defective_products):
#     availability = actual_run_time / planned_production_time if planned_production_time else 0
#     performance = (actual_output * standard_cycle_time) / actual_run_time if actual_run_time else 0
#     quality = (total_production - defective_products) / total_production if total_production else 0
#     oee = availability * performance * quality
#     return availability * 100, performance * 100, quality * 100, oee * 100

# # 데이터 저장 함수
# def save_data(date, line, equipment_data):
#     if 'data' not in st.session_state:
#         st.session_state.data = pd.DataFrame()
#     new_data = pd.DataFrame(equipment_data)
#     new_data['Date'] = date
#     new_data['Line'] = line
#     st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# # Streamlit 앱 시작
# st.title('🏭 식품제조 설비 종합효율(OEE) 대시보드')

# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📊 OEE 데이터 입력")
#     date = st.date_input("📅 날짜 선택", datetime.now())
#     line = st.selectbox("🔧 생산라인 선택", ["A라인", "B라인", "C라인"])
    
#     num_equipment = st.number_input("설비 수", min_value=1, max_value=5, value=1, step=1)
    
#     equipment_data = []
    
#     for i in range(num_equipment):
#         st.subheader(f"설비 {i+1}")
        
#         equipment_name = st.text_input(f"설비 {i+1} 이름", key=f"name_{i}")
#         weight = st.number_input(f"설비 {i+1} 가중치 (0-1)", min_value=0.0, max_value=1.0, value=1.0/num_equipment, step=0.1, key=f"weight_{i}")
        
#         planned_production_time = st.number_input("계획 생산 시간 (분)", min_value=0.0, step=0.1, format="%.1f", key=f"ppt_{i}")
#         actual_run_time = st.number_input("실제 가동 시간 (분)", min_value=0.0, step=0.1, format="%.1f", key=f"art_{i}")
#         actual_output = st.number_input("실제 생산량 (개)", min_value=0, step=1, key=f"ao_{i}")
#         standard_cycle_time = st.number_input("표준 사이클 타임 (분/개)", min_value=0.0, step=0.1, format="%.1f", key=f"sct_{i}")
#         total_production = st.number_input("총 생산량 (개)", min_value=0, step=1, key=f"tp_{i}")
#         defective_products = st.number_input("불량품 수량 (개)", min_value=0, step=1, key=f"dp_{i}")
        
#         availability, performance, quality, oee = calculate_oee(
#             planned_production_time, actual_run_time, actual_output, 
#             standard_cycle_time, total_production, defective_products
#         )
        
#         equipment_data.append({
#             'Equipment': equipment_name,
#             'Weight': weight,
#             'Planned_Production_Time': planned_production_time,
#             'Actual_Run_Time': actual_run_time,
#             'Actual_Output': actual_output,
#             'Standard_Cycle_Time': standard_cycle_time,
#             'Total_Production': total_production,
#             'Defective_Products': defective_products,
#             'Availability': availability,
#             'Performance': performance,
#             'Quality': quality,
#             'OEE': oee
#         })

#     if st.button("🧮 OEE 계산 및 저장"):
#         df = pd.DataFrame(equipment_data)
        
#         # 가중 평균 OEE 계산
#         weighted_oee = (df['OEE'] * df['Weight']).sum() / df['Weight'].sum()
        
#         st.subheader("🎯 OEE 계산 결과")
#         for i, equip in enumerate(equipment_data):
#             st.write(f"설비 {i+1} ({equip['Equipment']}) OEE: {equip['OEE']:.2f}%")
#         st.metric("생산라인 종합 OEE", f"{weighted_oee:.2f}%")

#         save_data(date, line, equipment_data)
#         st.success("✅ 데이터가 성공적으로 저장되었습니다!")

# with col2:
#     if 'data' in st.session_state and not st.session_state.data.empty:
#         st.subheader("📈 OEE 추세 분석")
        
#         lines = st.multiselect("생산라인 선택", options=st.session_state.data['Line'].unique(), default=st.session_state.data['Line'].unique())
#         date_range = st.date_input("기간 선택", [st.session_state.data['Date'].min(), st.session_state.data['Date'].max()])

#         filtered_data = st.session_state.data[
#             (st.session_state.data['Line'].isin(lines)) &
#             (st.session_state.data['Date'] >= date_range[0]) &
#             (st.session_state.data['Date'] <= date_range[1])
#         ]

#         fig = px.line(filtered_data, x='Date', y='OEE', color='Equipment', title='설비별 OEE 추세')
#         fig.update_layout(yaxis_range=[0,100])
#         st.plotly_chart(fig, use_container_width=True)

#         # 생산라인 종합 OEE 추세
#         line_oee = filtered_data.groupby(['Date', 'Line']).apply(lambda x: (x['OEE'] * x['Weight']).sum() / x['Weight'].sum()).reset_index(name='OEE')
#         fig_line = px.line(line_oee, x='Date', y='OEE', color='Line', title='생산라인 종합 OEE 추세')
#         fig_line.update_layout(yaxis_range=[0,100])
#         st.plotly_chart(fig_line, use_container_width=True)




import streamlit as st
import pandas as pd
from datetime import datetime, time

# 페이지 설정
st.set_page_config(page_title="식품제조 OEE 대시보드", layout="wide")

# CSS 스타일 적용
st.markdown("""
<style>
    .reportview-container .main .block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 2rem;}
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    .stMetric:hover {background-color: #e0e2e6;}
    .st-emotion-cache-10trblm {font-size: 1.5rem;}
</style>
""", unsafe_allow_html=True)

# OEE 계산 함수
def calculate_oee(availability, performance, quality):
    return availability * performance * quality / 10000

# 데이터 저장 함수
def save_data(date, hour, line, equipment_data):
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame()
    new_data = pd.DataFrame(equipment_data)
    new_data['Date'] = pd.to_datetime(f"{date} {hour:02d}:00:00")
    new_data['Line'] = line
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# Streamlit 앱 시작
st.title('🏭 식품제조 설비 종합효율(OEE) 대시보드')

# 레이아웃 구성
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📊 OEE 데이터 입력")
    date = st.date_input("📅 날짜 선택", datetime.now())
    hour = st.number_input("⏰ 시간 선택 (0-23)", min_value=0, max_value=23, value=datetime.now().hour)
    line = st.selectbox("🔧 생산라인 선택", ["A라인", "B라인", "C라인"])
    
    num_equipment = st.number_input("설비 수", min_value=1, max_value=5, value=1, step=1)
    
    equipment_data = []
    
    for i in range(num_equipment):
        st.subheader(f"설비 {i + 1}")

        equipment_name = st.text_input(f"설비 {i + 1} 이름", key=f"name_{i}")
        weight = st.number_input(f"설비 {i + 1} 가중치 (0-1)", min_value=0.0, max_value=1.0, value=1.0 / num_equipment,
                                 step=0.1, key=f"weight_{i}")

        st.subheader("⏰ 시간")
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            scheduled_time = st.number_input("계획 가동 시간 (분)", min_value=0.0, step=0.1, format="%.1f", key=f"scheduled_time_{i}")
        with time_col2:
            operating_time = st.number_input("실제 가동 시간 (분)", min_value=0.0, max_value=scheduled_time, step=0.1, format="%.1f", key=f"operating_time_{i}")
        availability = (operating_time / scheduled_time * 100) if scheduled_time else 0

        st.subheader("🎯 생산")
        prod_col1, prod_col2 = st.columns(2)
        with prod_col1:
            units_produced = st.number_input("총 생산량 (개)", min_value=0, step=1, key=f"units_produced_{i}")
        with prod_col2:
            defective_units = st.number_input("불량품 수 (개)", min_value=0, max_value=units_produced, step=1, key=f"defective_units_{i}")
        quality = ((units_produced - defective_units) / units_produced * 100) if units_produced else 0

        st.subheader("⚙️ 성능")
        performance_col1, performance_col2 = st.columns(2)
        with performance_col1:
            ideal_cycle_time = st.number_input("이상적인 사이클 타임 (초/개)", min_value=0.0, step=0.1, format="%.1f", key=f"ideal_cycle_time_{i}")
        with performance_col2:
            performance = ((units_produced * ideal_cycle_time) / (operating_time * 60) * 100) if operating_time and ideal_cycle_time else 0

        oee = calculate_oee(availability, performance, quality)

        equipment_data.append({
            'Equipment': equipment_name,
            'Weight': weight,
            'Scheduled_Time': scheduled_time,
            'Operating_Time': operating_time,
            'Units_Produced': units_produced,
            'Defective_Units': defective_units,
            'Ideal_Cycle_Time': ideal_cycle_time,
            'Availability': availability,
            'Performance': performance,
            'Quality': quality,
            'OEE': oee
        })

    if st.button("🧮 OEE 계산 및 저장"):
        df = pd.DataFrame(equipment_data)
        
        # 가중 평균 OEE 계산
        weighted_availability = (df['Availability'] * df['Weight']).sum() / df['Weight'].sum()
        weighted_performance = (df['Performance'] * df['Weight']).sum() / df['Weight'].sum()
        weighted_quality = (df['Quality'] * df['Weight']).sum() / df['Weight'].sum()
        weighted_oee = calculate_oee(weighted_availability, weighted_performance, weighted_quality)
        
        st.subheader("🎯 OEE 계산 결과")
        result_col1, result_col2, result_col3, result_col4 = st.columns(4)
        with result_col1:
            st.metric("Availability", f"{weighted_availability:.2f}%")
        with result_col2:
            st.metric("Performance", f"{weighted_performance:.2f}%")
        with result_col3:
            st.metric("Quality", f"{weighted_quality:.2f}%")
        with result_col4:
            st.metric("OEE", f"{weighted_oee:.2f}%")
        
        for i, equip in enumerate(equipment_data):
            st.write(f"설비 {i+1} ({equip['Equipment']}) OEE: {equip['OEE']:.2f}%")

        save_data(date, hour, line, equipment_data)
        st.success("✅ 데이터가 성공적으로 저장되었습니다!")

with col2:
    if 'data' in st.session_state and not st.session_state.data.empty:
        st.subheader("📊 저장된 OEE 데이터")
        
        # 필터 옵션
        lines = st.multiselect("생산라인 선택", options=st.session_state.data['Line'].unique(), default=st.session_state.data['Line'].unique())
        date_range = st.date_input("기간 선택", [st.session_state.data['Date'].min().date(), st.session_state.data['Date'].max().date()])

        # 데이터 필터링
        filtered_data = st.session_state.data[
            (st.session_state.data['Line'].isin(lines)) &
            (st.session_state.data['Date'].dt.date >= date_range[0]) &
            (st.session_state.data['Date'].dt.date <= date_range[1])
        ]

        # 데이터 정렬
        filtered_data = filtered_data.sort_values('Date', ascending=False)

        # 표시할 컬럼 선택
        display_columns = ['Date', 'Line', 'Equipment', 'Availability', 'Performance', 'Quality', 'OEE']

        # 소수점 둘째자리까지 반올림
        for col in ['Availability', 'Performance', 'Quality', 'OEE']:
            filtered_data[col] = filtered_data[col].round(2)

        # 테이블 표시
        st.dataframe(filtered_data[display_columns], use_container_width=True)

        # 데이터 요약 통계
        st.subheader("📈 OEE 요약 통계")
        summary = filtered_data.groupby('Line')[['Availability', 'Performance', 'Quality', 'OEE']].mean().round(2)
        st.dataframe(summary, use_container_width=True)

        # CSV 다운로드 버튼
        csv = filtered_data[display_columns].to_csv(index=False)
        st.download_button(
            label="📥 CSV로 다운로드",
            data=csv,
            file_name="oee_data.csv",
            mime="text/csv",
        )