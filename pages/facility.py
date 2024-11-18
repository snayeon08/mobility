import streamlit as st
import pandas as pd

# Initialize session state
if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# Load the data
data = pd.read_csv("배리어프리.csv")

st.title('배리어프리 문화관광시설이 어디에 있지?')
st.subheader("""
아래 지도는 서울에 있는 배리어프리 문화예술관광지를 보여줍니다.
시설에 표시된 점의 크기는 장애인용 출입문, 장애인 화장실, 장애인 전용 주차장, 점자 가이드 여부와 
시각장애인 안내견 동반 가능 여부에 따라 더 많이 충족할수록 크게 설정했습니다.
점의 색상은 시설의 카테고리에 따라 분류하였는데, 전시/공연은 빨강, 레저/체육/공원은 초록, 기타는 회색으로 표시했습니다.
""")

# Filter data for '서울특별시'
data = data[data['시도 명칭'] == '서울특별시']

data

# Calculate size based on specified columns
columns_to_count = [
    "장애인용 출입문", 
    "장애인 화장실 유무", 
    "장애인 전용 주차장 여부", 
    "시각장애인 안내견 동반 가능 여부", 
    "점자 가이드 여부"
]

data = data.copy().fillna(0)
data['size'] = data[columns_to_count].apply(lambda row: row.value_counts().get('Y', 0) * 20, axis=1)  # 크기를 10배로 조정

# Assign colors based on 카테고리
category_colors = {
    '전시/공연': '#FF5733',  # 예: 빨강
    '레저/체육/공원': '#33FF57',  # 예: 초록
    '기타': '#3357FF'  # 기본 색상 (필요 시 추가)
}

# Set a default color for unmapped categories
default_color = '#CCCCCC'  # 회색
data['color'] = data['카테고리'].map(category_colors).fillna(default_color)

# Display map
st.map(data, latitude="위도",
       longitude="경도",
       size="size",
       color="color")
