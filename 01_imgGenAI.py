import streamlit as st
from openai import OpenAI
import os

# OpenAI 클라이언트 초기화
openai_api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key  = openai_api_key)

# Streamlit 앱 레이아웃
st.title("AI 이미지 생성기")
st.write("텍스트 프롬프트를 입력하고 AI 이미지를 생성하세요.")

# 텍스트 입력
prompt = st.text_input("프롬프트를 입력하세요:")

# 이미지 크기 선택
size = st.selectbox("이미지 크기를 선택하세요:", ["256x256", "512x512", "1024x1024"])

if st.button("이미지 생성"):
    if prompt:
        try:
            kwargs = {
                "prompt": prompt,
                "n": 1,
                "size": size
            }

            # OpenAI API를 사용하여 이미지 생성
            response = client.images.generate(**kwargs)

            # 응답에서 이미지 URL 추출
            image_url = response.data[0].url

            # 생성된 이미지 표시
            st.image(image_url, caption="생성된 이미지", use_column_width=True)

        except Exception as e:
            st.error(f"이미지 생성 중 오류 발생: {e}")
    else:
        st.warning("이미지를 생성하려면 프롬프트를 입력하세요.")