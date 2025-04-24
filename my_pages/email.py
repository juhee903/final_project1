import streamlit as st
from email.mime.text import MIMEText
import smtplib

# 이메일 알림 기능을 구현하기 위한 함수
def send_email(subject, body, to_email):
    from_email = "your_email@example.com"  # 발신자 이메일
    from_password = "your_email_password"  # 발신자 이메일 비밀번호

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        st.success(f"이메일 알림이 성공적으로 전송되었습니다: {to_email}")
    except Exception as e:
        st.error(f"이메일 전송 실패: {str(e)}")

def show(df):
    # Machine ID가 1에서 50 사이의 값만 필터링하여 드롭다운 목록에 제공
    machine_ids = sorted([machine_id for machine_id in df['machine_id'].unique() if 1 <= machine_id <= 50])

    # 드롭다운에서 선택
    selected_id = st.selectbox("Select Machine ID", options=machine_ids)

    # 선택된 Machine ID에 해당하는 데이터 필터링
    machine_data = df[df['machine_id'] == selected_id]


    # 고장 유형에서 "Normal"을 제외한 데이터만 필터링
    maintenance_needed_data = machine_data[machine_data['failure_type'] != "Normal"]

    # 가장 비율이 높은 고장 유형을 찾기
    if not maintenance_needed_data.empty:
        failure_counts = maintenance_needed_data['failure_type'].value_counts()
        most_common_failure = failure_counts.idxmax()
        most_common_failure_count = failure_counts.max()

        # 이메일 알림 메시지 표시 (가장 비율이 높은 고장 유형)
        email_subject = f"Machine {selected_id} 고장 경고"
        email_body = f"""
        안녕하세요. 품질관리 부서입니다.

        Machine {selected_id} 정비와 관련하여 유지보수 팀에게 안내드립니다.

        - 고장 유형: {most_common_failure} 
        - 기계 상태: 유지보수 필요

        이 기계는 정비가 필요할 수 있습니다. 즉시 점검을 진행해 주세요.

        감사합니다.
        """

        st.markdown(f"""
        <div style="border: 2px solid green; border-radius: 10px; padding: 20px; background-color: white;">
            <h3 style="color: black; text-align: center;">이메일 형식 알림</h3>
            <p><b>제목</b>: {email_subject}</p>
            <p><b>내용</b>: {email_body}</p>
        </div>
        """, unsafe_allow_html=True)

        # 가상의 알림 전송 버튼
        if st.button("메일 발송"):
            st.success("이메일을 발송했습니다.")
    else:
        st.info(f"Machine {selected_id}는 정비가 필요하지 않습니다.")
