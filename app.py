import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="업무지원요청 대시보드", layout="wide")

st.title("📊 업무지원요청 데이터 대시보드")
st.write("업무지원요청_합성자료 CSV 파일을 업로드하면 현황을 분석하여 시각화합니다.")

# 1. 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 2. 데이터 불러오기
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding='cp949')
    
    # 날짜 데이터 타입 변환
    if 'request_date' in df.columns:
        df['request_date'] = pd.to_datetime(df['request_date'])

    # 3. 데이터 미리보기
    st.subheader("📋 전체 데이터 확인")
    st.dataframe(df)
    
    # 4. 요약 통계(Metric) 보여주기
    st.subheader("💡 주요 통계 요약")
    col1, col2, col3, col4 = st.columns(4)
    
    total_req = len(df)
    completed_req = len(df[df['status'] == '완료']) if 'status' in df.columns else 0
    urgent_req = len(df[df['urgency'] == '상']) if 'urgency' in df.columns else 0
    ai_req = len(df[df['ai_handling'] == '전용AI가능']) if 'ai_handling' in df.columns else 0
    
    col1.metric("총 요청 건수", f"{total_req}건")
    col2.metric("처리 완료", f"{completed_req}건")
    col3.metric("긴급(상) 요청", f"{urgent_req}건")
    col4.metric("전용 AI 가능", f"{ai_req}건")
    
    st.divider()

    # 5. 데이터 시각화 구역
    st.subheader("📈 상세 시각화 분석")
    
    # 레이아웃 나누기 (2단 구성)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # 카테고리별 요청 건수
        if 'category' in df.columns:
            st.write("#### 📌 카테고리별 요청 현황")
            category_counts = df['category'].value_counts().reset_index()
            category_counts.columns = ['카테고리', '건수']
            # Streamlit 내장 막대그래프 사용
            st.bar_chart(category_counts.set_index('카테고리'))
            
        # 긴급도별 요청 현황
        if 'urgency' in df.columns:
            st.write("#### 🚨 긴급도별 현황")
            urgency_counts = df['urgency'].value_counts().reset_index()
            urgency_counts.columns = ['긴급도', '건수']
            st.bar_chart(urgency_counts.set_index('긴급도'))

    with chart_col2:
        # 처리 상태별 현황
        if 'status' in df.columns:
            st.write("#### ✅ 처리 상태별 현황")
            status_counts = df['status'].value_counts().reset_index()
            status_counts.columns = ['상태', '건수']
            st.bar_chart(status_counts.set_index('상태'))
            
        # AI 처리 방식 현황
        if 'ai_handling' in df.columns:
            st.write("#### 🤖 AI 처리(ai_handling) 방식 비율")
            ai_counts = df['ai_handling'].value_counts().reset_index()
            ai_counts.columns = ['AI처리방식', '건수']
            st.bar_chart(ai_counts.set_index('AI처리방식'))

    # 일자별 추이 (선 그래프 - 전체 너비 사용)
    if 'request_date' in df.columns:
        st.write("#### 📅 일자별 업무 요청 추이")
        # 날짜별로 건수를 세기
        date_counts = df.groupby('request_date').size().reset_index(name='건수')
        # Streamlit 라인 차트 사용
        st.line_chart(date_counts.set_index('request_date'))

else:
    st.info("👆 위 영역에 '업무지원요청_합성자료 (1).csv' 파일을 업로드해주세요.")
