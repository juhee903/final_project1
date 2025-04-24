import streamlit as st
import plotly.graph_objects as go
import pandas as pd
def show(df):
    # 1~50까지의 머신 ID만 선택할 수 있도록 제한
    machine_ids = list(range(1, 51))
    selected_id = st.session_state.get("selected_machine_id", None)
    if selected_id is None:
        st.markdown(f"""
        <h1 style='text-align: center; font-size: 36px;'>
            기계별 센서값 모니터링
        </h1>
        """, unsafe_allow_html=True)
        mdf = df.copy()  # 전체 데이터를 사용
    else:
        st.markdown(f"""
        <h1 style='text-align: center; font-size: 36px;'>
             Machine {selected_id}
        </h1>
        """, unsafe_allow_html=True)
        mdf = df[df['machine_id'] == selected_id]  # 선택된 머신 ID에 해당하는 데이터만 사용
    m_count = len(mdf)
    # :흰색_확인_표시: KPI 값 계산
    maintenance_ratio = mdf['maintenance_required'].mean()
    anomaly_ratio = mdf['anomaly_flag'].mean()
    # 온도-진동 지표 계산 (가중 평균)
    mdf['temperature_vibration_score'] = 0.5 * mdf['temperature'] + 0.5 * mdf['vibration']
    avg_temperature_vibration_score = mdf['temperature_vibration_score'].mean()
    # :흰색_확인_표시: 스타일 정의 (HTML)
    st.markdown("""
        <style>
            .metric-container {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;
                margin-bottom: 30px;
            }
            .metric-card {
                background-color: #F9F9F9;
                padding: 20px 15px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.07);
                flex: 1;
            }
            .metric-title {
                font-size: 16px;
                color: #555;
                margin-bottom: 6px;
            }
            .metric-value {
                font-size: 26px;
                font-weight: 600;
                color: #222;
            }
        </style>
    """, unsafe_allow_html=True)
    # :흰색_확인_표시: KPI 카드 출력
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-title">📦 데이터 수</div>
            <div class="metric-value">{m_count} 건</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">🛠 정비 비율</div>
            <div class="metric-value">{maintenance_ratio * 100:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">⚠️ 이상 감지 비율</div>
            <div class="metric-value">{anomaly_ratio * 100:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">⚙️ 온도-진동 지표</div>
            <div class="metric-value">{avg_temperature_vibration_score:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # :말풍선: KPI 아래 여백 추가
    st.markdown(" ")
    # :흰색_확인_표시: 센서 시각화 + 고장 원인 분석 나란히 배치
    st.markdown("""<h3 style='text-align: center;'>📊 센서별 비교</h3>""", unsafe_allow_html=True)
    sensors = ['temperature', 'vibration', 'humidity', 'pressure', 'energy_consumption']
    # 원래 값 그대로
    if selected_id is None:
        machine_avg = df[sensors].mean()
    else:
        machine_avg = df[df['machine_id'] == selected_id][sensors].mean()
    global_avg = df[sensors].mean()
    fig = go.Figure()
    # 현재 장비의 바 그래프 (기존 값)
    fig.add_trace(go.Bar(
        x=sensors,
        y=machine_avg,
        name="현재 장비",
        marker_color='#1E3A8A',  # 진한 파랑
        text=machine_avg.round(2),  # 숫자 추가
        textposition='outside'  # 바 위에 숫자 표시
    ))
    # 전체 평균 선 그래프
    fig.add_trace(go.Scatter(
        x=sensors,
        y=global_avg,
        name="전체 평균",
        mode='lines+markers',
        line=dict(color='royalblue'),
        text=global_avg.round(2),  # 숫자 추가
        textposition='top center'  # 선 위에 숫자 표시
    ))
    fig.update_layout(
        yaxis=dict(title="센서 값"),
        height=400,
        title="센서별 평균값 비교",
    )
    # 색상 및 해석 설정 (절대값을 기준으로 차이 계산)
    colors = []
    interpretations = []
    for m, g in zip(machine_avg, global_avg):
        ratio = abs(m - g)  # 절대값으로 차이 계산
        if ratio > 0.2:  # 0.2 이상 차이
            colors.append("#1E3A8A")  # 진한 파랑
            interpretations.append("편차 큼")
        elif ratio > 0.1:  # 0.1 이상 0.2 미만 차이
            colors.append("#3B82F6")  # 파랑
            interpretations.append("편차 중간")
        elif ratio > 0.05:  # 0.05 이상 0.1 미만 차이
            colors.append("#93C5FD")  # 하늘색
            interpretations.append("편차 작음")
        else:
            colors.append("#D0F4FF")  # 연한 파랑
            interpretations.append("편차 매우 작음")
    # :막대_차트: 그래프
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sensors,
        y=machine_avg,
        marker_color=colors,
        text=machine_avg.round(2),
        textposition="outside",
        name="현재 장비"
    ))
    fig.add_trace(go.Scatter(
        x=sensors,
        y=global_avg,
        mode="lines+markers",
        name="전체 평균",
        line=dict(color="royalblue")
    ))
    fig.update_layout(
        yaxis_title="센서값",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    # :클립보드: 표
    diff_df = pd.DataFrame({
        "현재값": machine_avg.round(2),
        "전체 평균": global_avg.round(2),
        "차이 (현재 - 평균)": (machine_avg - global_avg).round(2),
        "해석": interpretations
     })
    st.dataframe(diff_df, use_container_width=True)
    
