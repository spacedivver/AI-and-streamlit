import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.title("📕📝🔍 PDF 검색 서비스")

# 1. Load
# PDF 문서들에서 텍스트 추출
def get_pdf_texts(pdf_docs):
    texts = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            texts += page.extract_text()

    return texts

# 2. Chunk
# 텍스트 청크 분할
def get_text_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # 청크의 크기
        chunk_overlap=50  # 청크 사이의 중복 정도
    )

    chunks = text_splitter.split_text(raw_text)
    return chunks

# 3. Embed + Store
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    return vectorstore

# =========================================================================================
# torch 사용 버전(용량 크고 오류 많음)

# from sentence_transformers import SentenceTransformer
# from langchain_community.vectorstores import FAISS
# import torch

# def get_vectorstore(text_chunks):
#     # Use a free, open-source embedding model from Hugging Face
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#
#     # Create embeddings
#     embeddings = model.encode(text_chunks)
#
#     # Create FAISS vector store
#     vectorstore = FAISS.from_embeddings(
#         text_embedding_pairs=list(zip(text_chunks, embeddings)),
#         embedding=None  # We'll pass None since we've already created embeddings
#     )
#
#     return vectorstore

# =========================================================================================

# 4. Chain
def get_conversation_chain(vectorstore):
    # ConversationBufferWindowMemory에 이전 대화 저장
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",  # 사용할 모델 이름
        temperature=0.7,  # 생성된 답변의 일관성을 높이기 위해 temperature=0으로 설정
        openai_api_key=OPENAI_API_KEY  # OpenAI API 키 입력
    )

    # RAG 시스템 (RetrievalQA 체인) 구축
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,  # 언어 모델
        chain_type="stuff",  # 검색된 모든 문서를 합쳐 전달 ("stuff" 방식)
        retriever=vectorstore.as_retriever(),  # 벡터 스토어 리트리버
        return_source_documents=False,  # 답변에 사용된 문서 출처 반환
    )
    return qa_chain


user_uploads = st.file_uploader("PDF 파일을 업로드해 주세요~ 📂", accept_multiple_files=True)
if user_uploads:
    if st.button("PDF 업로드 🥳"):
        with st.spinner("PDF 처리 중이에요~ 잠시만 기다려 주세요! ⏳"):
            # 1. PDF 문서들에서 텍스트 추출 (Load)
            raw_text = get_pdf_texts(user_uploads)
            # 2. 텍스트 청크 분할 (Chunk)
            chunks = get_text_chunks(raw_text)
            # 3. 벡터 저장소 만들기 (Embed+Store)
            vectorstore = get_vectorstore(chunks)
            # 4. 대화 체인 만들기 (Chain)
            st.session_state.conversation = get_conversation_chain(vectorstore)

            st.success("PDF 업로드 완료! 대화 시작해 보세요~ 😊")
            ready = True


if user_query := st.chat_input("궁금한 걸 입력해 주세요! 🎤"):
    if 'conversation' in st.session_state:
        with st.spinner("답변 준비 중이에요~ 🧐"):
            result = st.session_state.conversation.invoke({"query": user_query})
            response = result['result']
    else:
        response = "PDF를 먼저 업로드해 주세요! 🥺"

    with st.chat_message("assistant"):
        st.write(response)