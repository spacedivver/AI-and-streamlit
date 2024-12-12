# AI 기반 코디 추천 서비스

import streamlit as st
from PIL import Image
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# OpenAI API 키 설정
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# GPT-4 모델 초기화
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY
)

# CLIP 모델 초기화
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# BLIP 모델 초기화 (이미지 캡셔닝)
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Streamlit 제목
st.title("👗 AI 기반 코디 추천 서비스")

# 이미지 업로드 섹션
st.sidebar.header('이미지 업로드')
uploaded_file = st.sidebar.file_uploader("이미지를 업로드하세요 (옷을 입은 사람의 사진)", type=["jpg", "jpeg", "png"])


if uploaded_file:
    # 이미지 로드 및 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    # 사용자 프롬프트 입력
    user_prompt = st.text_input("프롬프트를 입력하세요 (예: '캐주얼한 모임에 어울리는 코디')")

    if user_prompt and st.button("분석 시작"):
        with st.spinner("이미지 및 프롬프트 분석 중..."):
            # BLIP 모델로 이미지 캡셔닝
            inputs = blip_processor(image, return_tensors="pt")
            out = blip_model.generate(**inputs)
            caption = blip_processor.decode(out[0], skip_special_tokens=True)

            # CLIP 모델로 텍스트와 이미지 유사도 분석 (추가적인 분석 가능)
            inputs_clip = clip_processor(text=[user_prompt], images=image, return_tensors="pt", padding=True)
            outputs_clip = clip_model(**inputs_clip)
            logits_per_image = outputs_clip.logits_per_image  # 이미지와 텍스트 간 유사도 점수

            # GPT-4를 사용하여 코디 추천 생성
            prompt_template = PromptTemplate(
                input_variables=["image_caption", "user_prompt"],
                template="""
                사용자 프롬프트: {user_prompt}

                업로드된 이미지 설명: {image_caption}

                사용자가 요청한 상황에 맞게 코디를 제안해주세요. 
                - 상의, 하의, 신발 등 변경이 필요한 항목을 구체적으로 설명하고 추천해주세요.
                """
            )

            # GPT-4로 코디 추천 생성
            reasoning_input = {
                "image_caption": caption,
                "user_prompt": user_prompt,
            }
            recommendation = llm.predict(prompt_template.format(**reasoning_input))

        # 결과 출력
        st.success("분석 완료!")
        # st.write("## 이미지 캡셔닝 결과")
        # st.write(f"**이미지 설명:** {caption}")
        st.write("## 코디 추천 결과")
        st.write(recommendation)
