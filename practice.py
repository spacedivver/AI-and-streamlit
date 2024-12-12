import streamlit as st
import time

# 주제 작성하기
st.title("안녕하세요.")

# 글
st.write('반갑습니다.')

# 버튼
st.button('노크하기')

# 조건문
if st.button('노크하기2'):
    st.write("사람있어요")

st.write("동의하시면 아래 내용에 체크해주세요.")
agree=st.checkbox('동의합니다!')

if agree:
    st.write('감사합니다')

# 슬라이더
age=st.slider("당신은 몇 살인가요?",0,130,25)
st.write(f"저는{age}살 입니다.")

# 텍스트 입력
text1=st.text_input("이름을 입력하세요")
text2=st.text_area("자기소개 해주세요")
st.write(f"이름:{text1}")
st.write(f"{text2}")

# 이미지
if st.button("랜덤 이미지 생성"):
    st.image(f'https://picsum.photos/250/250?t={time.time()}') # 버튼 누를 때마다 다른 값 보이기 위해 time() 함수 사용

