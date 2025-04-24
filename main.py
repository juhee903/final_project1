import streamlit as st
import pandas as pd
from my_pages import home, monitoring, prediction, email  # email 페이지 추가

# 페이지 설정
st.set_page_config(page_title="IoT 장비 모니터링 대시보드", layout="wide")

# 페이지 타이틀 설정
st.markdown("""
    <h1 style='text-align: center; margin-top: 10px; color: #222;'>
        📡 IoT 장비 모니터링 대시보드 📡
    </h1>
""", unsafe_allow_html=True)

# 데이터 로드 함수
@st.cache_data
def load_default_data():
    df = pd.read_csv("C:/Users/문주희/Documents/내배캠/merge_data.csv")
    df['machine_id'] = df['machine_id'].abs()  # machine_id의 부호를 절대값으로 변경
    return df

# 데이터 로딩
if "df_data" not in st.session_state or st.session_state["df_data"].empty:
    st.session_state["df_data"] = load_default_data()

# 페이지 네비게이션
nav1, nav2, nav3, nav4, filter_col1, filter_col2 = st.columns([1, 1, 1, 1, 1.5, 2])
with nav1:
    if st.button("🏠 잔여 수명", use_container_width=True):
        st.session_state.page = "home"
with nav2:
    if st.button("📊 모니터링", use_container_width=True):
        st.session_state.page = "monitoring"
with nav3:
    if st.button("🔍 유지 보수", use_container_width=True):
        st.session_state.page = "prediction"
with nav4:
    if st.button("📧 이메일 알림", use_container_width=True):  # 이메일 알림 페이지 버튼 추가
        st.session_state.page = "email"

# 필터는 'monitoring' 페이지에서만 표시되도록 제한
if st.session_state.page == "monitoring":
    with filter_col1:
        view_option = st.radio("범위", ["전체", "machine 선택"], label_visibility="collapsed", horizontal=True)
    with filter_col2:
        # 데이터에서 Machine ID 추출하여 오름차순 정렬
        machine_ids = sorted(st.session_state["df_data"]['machine_id'].dropna().unique())
        if view_option == "전체":
            st.session_state.selected_machine_id = None
        else:
            selected_id = st.selectbox("Machine ID", machine_ids, label_visibility="collapsed")
            st.session_state.selected_machine_id = selected_id

# 페이지 호출
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home.show()
elif st.session_state.page == "monitoring":
    monitoring.show(st.session_state["df_data"])  # monitoring 페이지에서 데이터 전달
elif st.session_state.page == "prediction":
    prediction.show(st.session_state["df_data"])  # prediction 페이지에서 데이터 전달
elif st.session_state.page == "email":
    email.show(st.session_state["df_data"])  # email 페이지로 이메일 알림 처리
