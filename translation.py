import streamlit as st
import time
from translate import Translator


# 번역
def translate(input_text):
  translator = Translator(from_lang='ko', to_lang='en')
  translation = translator.translate(input_text)
  return translation

st.title("한국어-영어 변역기")
text=st.text_input("한국어 문장을 입력하세요.")

if st.button('번역'):
    answer_text = translate(text)
    st.write(answer_text)
