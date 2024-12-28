import os
import streamlit as st
from openai import OpenAI
from github import Github
from dotenv import load_dotenv
from PIL import Image

# .env 파일 로드
load_dotenv()

# OpenAI API 클라이언트 초기화
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# GitHub API 클라이언트 초기화
github_token = os.getenv("GITHUB_TOKEN")
github_repo = os.getenv("GITHUB_REPO")
g = Github(github_token)
repo = g.get_repo(github_repo)


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


def upload_to_github(file_path, repo, commit_message="Add captured image"):
    with open(file_path, "rb") as file:
        content = file.read()
    try:
        # 파일이 이미 존재하는지 확인
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, commit_message, content, contents.sha)
    except:
        repo.create_file(file_path, commit_message, content)
    # 원시 URL 반환
    return f"https://raw.githubusercontent.com/{repo.full_name}/main/{file_path}"


st.title("진수의 AI 도슨트\n이미지를 설명해드려요!")

# 수평 막대 생성
col1, col2 = st.columns(2)

with col1:
    st.header("이미지 주소 입력")
    input_url = st.text_area(
        "여기에 이미지 주소를 입력하세요!",
        value="data:image/jpeg;base64,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",
    )

    if st.button("이미지 주소 해설"):
        if input_url:
            try:
                st.session_state["input_url"] = input_url
                st.session_state["result_url"] = describe(input_url)
            except Exception as e:
                st.error(f"요청 오류가 발생했습니다: {e}")
        else:
            st.warning("이미지 주소를 입력하세요!")

    if "input_url" in st.session_state:
        st.image(st.session_state["input_url"], width=300, caption="입력된 이미지")
    if "result_url" in st.session_state:
        st.success(st.session_state["result_url"])

with col2:
    st.header("이미지 파일 업로드")
    uploaded_file = st.file_uploader(
        "이미지 파일을 업로드하세요", type=["jpg", "jpeg", "png"]
    )

    if st.button("파일 업로드 해설"):
        if uploaded_file is not None:
            # 업로드된 파일을 저장
            img_path = f"uploaded_{uploaded_file.name}"
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 이미지를 화면에 표시
            st.session_state["img_path"] = img_path

            # 이미지 형식 확인
            try:
                img = Image.open(img_path)
                img_format = img.format.lower()
                if img_format not in ["png", "jpeg", "gif", "webp"]:
                    st.error(
                        "지원되지 않는 이미지 형식입니다. png, jpeg, gif, webp 형식의 이미지를 업로드하세요."
                    )
                else:
                    # 업로드된 이미지를 GitHub에 업로드
                    try:
                        img_url = upload_to_github(img_path, repo)
                        st.session_state["img_url"] = img_url
                        st.session_state["result_file"] = describe(img_url)
                    except Exception as e:
                        st.error(f"이미지 업로드에 실패했습니다: {e}")
            except Exception as e:
                st.error(f"이미지 형식을 확인하는 중 오류가 발생했습니다: {e}")
        else:
            st.warning("이미지 파일을 업로드하세요!")

    if "img_path" in st.session_state:
        st.image(
            st.session_state["img_path"],
            caption="업로드된 이미지",
            use_container_width=True,
        )
    if "result_file" in st.session_state:
        st.success(st.session_state["result_file"])
