# app.py

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
import plotly.express as px

@st.cache_data
def load_data():
    # GitHub에서 직접 데이터를 로드합니다.
    # 이 URL은 실제 데이터 파일의 raw GitHub URL로 교체해야 합니다.
    url = "https://raw.githubusercontent.com/hwa0mb0y/202408-AI/main/fulldata_koreantemple.csv"
    return pd.read_csv(url)

def create_map(data, selected_sects):
    center_lat = data['Latitude'].mean()
    center_lon = data['Longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    # 마커 클러스터 생성
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in data.iterrows():
        if row['소속단체(종단)'] in selected_sects:
            popup_content = f"""
            <b>사찰명:</b> {row['사찰명']}<br>
            <b>구분:</b> {row['구분']}<br>
            <b>시도:</b> {row['시도']}<br>
            <b>상세주소:</b> {row['상세주소']}<br>
            <b>위도:</b> {row['Latitude']}<br>
            <b>경도:</b> {row['Longitude']}<br>
            <b>소속단체(종단):</b> {row['소속단체(종단)']}
            """
            
            # 종단에 따라 다른 아이콘 사용
            if row['소속단체(종단)'] == '조계종':
                icon = folium.Icon(color='red', icon='info-sign')
            elif row['소속단체(종단)'] == '태고종':
                icon = folium.Icon(color='blue', icon='cloud')
            else:
                icon = folium.Icon(color='green', icon='leaf')

            # 해결 방법 2: FeatureGroup 사용
            fg = folium.FeatureGroup(name=row['소속단체(종단)'])
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=row['사찰명'],
                icon=icon
            ).add_to(fg)
            fg.add_to(m)
    
    return m


def main():
    st.title('한국 전통사찰 지도')

    data = load_data()

    # 종단 선택
    all_sects = sorted(data['소속단체(종단)'].unique())
    
    # '전체 선택' 버튼 포함
    selected_sects = st.multiselect(
            '표시할 소속단체(종단)를 선택하세요',
            all_sects,
            default=all_sects
        )
    if st.button('전체 종단 선택'):
        selected_sects = all_sects
    
    # 지도 생성
    if selected_sects:
        m = create_map(data, selected_sects)
        folium_static(m)
    else:
        st.warning('하나 이상의 소속단체(종단)를 선택해주세요.')

    # 데이터 통계
    st.subheader('데이터 통계')
    st.write(f'총 사찰 수: {len(data)}')
    st.write(f'선택된 사찰 수: {len(data[data["소속단체(종단)"].isin(selected_sects)])}')
    
    # 종단별 사찰 수 차트
    st.subheader('종단별 사찰 수')
    sect_counts = data['소속단체(종단)'].value_counts()
    fig_sect = px.bar(x=sect_counts.index, y=sect_counts.values, labels={'x': '종단', 'y': '사찰 수'})
    st.plotly_chart(fig_sect)

    # 시도별 사찰 수 차트
    st.subheader('시도별 사찰 수')
    city_counts = data['시도'].value_counts()
    fig_city = px.bar(x=city_counts.index, y=city_counts.values, labels={'x': '시도', 'y': '사찰 수'})
    st.plotly_chart(fig_city)

if __name__ == "__main__":
    main()