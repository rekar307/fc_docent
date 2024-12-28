import os
import cv2
import numpy as np
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from streamlit_webrtc import webrtc_streamer

# .env 파일 로드
load_dotenv()

# OpenAI API 클라이언트 초기화
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# OpenAI API 요청 함수
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
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ],
        max_tokens=1024,
    )
    return response.choices[0].message.content


# Streamlit 앱 UI
st.title("AI 도슨트: 이미지를 설명해드려요!")

# **1. URL 입력으로 이미지 설명 요청**
input_url = st.text_area("이미지 URL을 입력하세요:")

if st.button("URL 해설"):
    if input_url:
        try:
            st.image(input_url, width=300)
            result = describe(input_url)
            st.success(result)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("URL을 입력해주세요!")

# **2. 카메라를 사용하여 이미지 캡처**
st.write("---")
st.write("또는 카메라로 이미지를 촬영하세요!")


# WebRTC 설정
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    return frame


webrtc_ctx = webrtc_streamer(
    key="camera",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

if st.button("카메라 해설"):
    if webrtc_ctx and webrtc_ctx.video_processor:
        # 영상에서 캡처
        frame = webrtc_ctx.video_processor.last_frame
        if frame is not None:
            # 이미지를 로컬에 저장 (예: 'captured_image.jpg')
            img_path = "captured_image.jpg"
            cv2.imwrite(img_path, frame)
            st.image(frame, caption="촬영한 이미지", use_column_width=True)

            # 업로드된 이미지를 처리하고 OpenAI 요청 (URL 필요 시 추가 처리 필요)
            st.warning("촬영한 이미지를 URL로 변환해야 OpenAI 요청이 가능합니다.")
        else:
            st.warning("이미지를 캡처하지 못했습니다.")
    else:
        st.warning("카메라가 활성화되지 않았습니다.")
