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

    # 색상 매핑 정의
    color_map = {
        '조계종': 'red',
        '태고종': 'blue',
        '선학원': 'green',
        '그 외': 'gray'
    }

    # 각 종단별로 FeatureGroup을 만듭니다.
    sect_groups = {sect: folium.FeatureGroup(name=sect) for sect in selected_sects}

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
            
            # 종단에 따라 다른 색상으로 마커를 표시합니다.
            if row['소속단체(종단)'] == '조계종':
                color='red'
            elif row['소속단체(종단)'] == '태고종':
                color='blue'
            elif row['소속단체(종단)'] == '선학원':
                color='purple'
            else:
                color='green'

            
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=4,
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=row['사찰명'],
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
            ).add_to(sect_groups[row['소속단체(종단)']])
    
    # 각 FeatureGroup을 지도에 추가합니다.
    for group in sect_groups.values():
        group.add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m


def main():
    st.title('한국 전통사찰 지도')

    data = load_data()

    # 종단을 갯수로 세어서 종단 리스트를 만듭니다.
    sect_counts = data['소속단체(종단)'].value_counts()
    all_sects = sect_counts.index.tolist()
    
    # '전체 선택' 옵션 추가
    all_sects_with_select_all = ['전체 선택'] + all_sects
    
    selected_sects = st.multiselect(
        '표시할 소속단체(종단)를 선택하세요 (갯수 많은 순)',
        all_sects_with_select_all,
        default=None
    )
    
    # '전체 선택' 처리
    if '전체 선택' in selected_sects:
        selected_sects = all_sects
    else:
        selected_sects = [sect for sect in selected_sects if sect != '전체 선택']
    
    
    # 지도 생성
    if selected_sects:
        m = create_map(data, selected_sects)
        folium_static(m, width=1000, height=600)
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