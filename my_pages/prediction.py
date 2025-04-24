import streamlit as st
import pandas as pd
import plotly.express as px
from email.mime.text import MIMEText
import smtplib

def show(df):
    # Machine ID가 1에서 50 사이의 값만 필터링하여 드롭다운 목록에 제공
    machine_ids = sorted([machine_id for machine_id in df['machine_id'].unique() if 1 <= machine_id <= 50])

    # 드롭다운에서 선택
    selected_id = st.selectbox("Select Machine ID", options=machine_ids)

    # 선택된 Machine ID에 해당하는 데이터 필터링
    machine_data = df[df['machine_id'] == selected_id]

    # `maintenance_required`가 1인 행만 필터링
    maintenance_needed_data = machine_data[machine_data['maintenance_required'] == 1]
    
    # ✅ 정비 필요 개수 및 전체 개수 계산
    total_count = len(machine_data)
    maintenance_count = machine_data['maintenance_required'].sum()

    # ✅ 제목에 함께 표시
    st.markdown(f"### 기계별 정비 필요 현황 ({int(maintenance_count)} / {total_count})")

    # `maintenance_required`가 1인 데이터를 스타일로 표시
    def highlight_maintenance_required(row):
        return ['background-color: red' if row['maintenance_required'] == 1 else '' for _ in row]

    # `maintenance_required`가 1인 행을 빨간색으로 표시하고 데이터 출력
    machine_data_styled = machine_data.style.apply(highlight_maintenance_required, axis=1)
    
    # 데이터프레임 출력
    st.dataframe(machine_data_styled)
    
    # 고장 유형에서 "Normal"을 제외한 데이터만 필터링
    maintenance_needed_data = maintenance_needed_data[maintenance_needed_data['failure_type'] != 'Normal']

    # 가장 비율이 높은 고장 유형 찾기
    if not maintenance_needed_data.empty:
        failure_counts = maintenance_needed_data['failure_type'].value_counts()
        most_common_failure = failure_counts.idxmax()

        # 고장 유형별로 파이 차트 그리기
        fig = px.pie(failure_counts, names=failure_counts.index, values=failure_counts.values,
                     title=f"Machine {selected_id}의 고장 유형")

        # 제목과 폰트 크기 조정
        fig.update_layout(
            title=dict(
                text=f"Machine {selected_id}의 고장 유형",  # 제목 내용
                font=dict(
                    size=30,  # 제목 폰트 크기
                    color="black"
                )
            )
        )

        # 파이 차트를 상단에 출력
        st.plotly_chart(fig, use_container_width=True)

       