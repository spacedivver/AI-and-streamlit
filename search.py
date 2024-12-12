import streamlit as st
import urllib.request
import json

search_text=st.text_input("검색어를 입력하세요.")
if st.button("검색"):
    client_id = "5sVOiN1murNE_nGoIJpe"
    client_secret = "F0w0nSa9vG"
    encText = urllib.parse.quote(search_text)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        # st.write(response_body.decode('utf-8'))
        # 전달받은 데이터는 바이트 형식이므로 디코딩이 필요함
        # response_body를 UTF-8로 디코딩한 후,
        # json.loads()으로 JSON 문자열을 파이썬 객체로 변환
        # JSON 구조에 접근하여 데이터를 추출
        json_result = json.loads(response_body.decode('utf-8'))
        #  JSON 객체에서 'items' 키에 해당하는 값을 추출하여 items 변수에 할당
        #  items는 블로그 포스트 정보를 담고 있는 사전들의 리스트
        items = json_result['items']
        for item in items:
            st.write(item['title'].replace('<b>', '').replace('</b>', ''))  # HTML 태그 제거
    else:
        print("Error Code:" + rescode)








