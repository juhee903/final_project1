import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show():
    if "df_data" in st.session_state:
        df = st.session_state["df_data"]
    else:
        st.session_state["df_data"] = pd.DataFrame()
        df = st.session_state["df_data"]

    if not df.empty:
        # 제목: 가운데 정렬하고 글자 크기 증가
        st.markdown("""<h2 style='text-align: center; margin-top: 30px; font-size: 36px;'>🔧 기계별 잔여 수명 </h2>""", unsafe_allow_html=True)

        # Machine ID가 1에서 50 사이의 값만 필터링하여 드롭다운 목록에 제공
        machine_ids = sorted([machine_id for machine_id in df['machine_id'].unique() if 1 <= machine_id <= 50])

        # 드롭다운에서 선택
        selected_id = st.selectbox("Select Machine ID", options=machine_ids)

        # 선택된 Machine ID에 해당하는 데이터 필터링
        machine_data = df[df['machine_id'] == selected_id]


        # x축은 잔여 수명 (0~600분), y축은 빈도수
        bins = list(range(0, 601, 50))  # 0부터 600까지 50 간격으로 구간 생성

        # 잔여 수명에 따른 빈도수 구하기
        histogram, bin_edges = pd.cut(machine_data['predicted_remaining_life'], bins=bins, include_lowest=True, right=False).value_counts().sort_index().values, pd.cut(machine_data['predicted_remaining_life'], bins=bins, include_lowest=True, right=False).value_counts().sort_index().index

        # 범위 객체에서 숫자만 추출하여 색상 지정
        bin_edges_str = [str(b) for b in bin_edges]
        colors = []

        for b in bin_edges_str:
            if '[0,' in b:  # 0~50 구간
                colors.append('red')
            elif '[50,' in b and '100' in b:  # 50~100 구간
                colors.append('pink')
            else:  # 그 외의 구간
                colors.append('pink')

        # 그래프 그리기
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=bin_edges_str,
            y=histogram,
            marker=dict(
                color=colors,
                showscale=False
            ),
            name="교체 필요"
        ))

        fig.update_layout(
            xaxis=dict(title="잔여 수명"),
            yaxis=dict(title="빈도수"),
            height=500,
            margin=dict(t=30, r=30, b=50, l=40),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("데이터가 없어서 정비 필요 Top 5 장비를 표시할 수 없습니다.")

    st.markdown("---")
