import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def describe(image_url):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "이 이미지에 대해서 설명해줘.",
                    },
                    {
                        "type": "image_url",
                        # "image_url": {"url": image_url},
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ],
        max_tokens=1024,
    )
    return response.choices[0].message.content


st.title("진수의 AI 도슨트: 이미지를 설명해드려요!")

input_url = st.text_area("여기에 이미지 주소를 입력하세요")

if st.button("해설"):
    if input_url:
        try:
            st.image(input_url, width=300)
            result = describe(input_url)
            print(result)
            st.success(result)
        except:
            st.error("요청 오류가 발생하였습니다.")
    else:
        st.warning("텍스트를 입력하에요!")
