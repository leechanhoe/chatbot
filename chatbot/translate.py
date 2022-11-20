import urllib.request
import json

'''
네이버의 파파고 API를 이용하여 영어 한국어간 번역
'''

def ko_to_en(korean):
    client_id = "Yf8pIXHfziTxI7Noq45o" # api 호출을 위한 아이디 비번
    client_secret = "367NI3T0ES"

    encText = urllib.parse.quote(korean)
    data = "source=ko&target=en&text=" + encText # http 요청에 보낼 내용
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url) # http 요청 생성
    request.add_header("X-Naver-Client-Id", client_id) # 헤더에 아이디 비번 추가
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8")) # 응답 받아옴
    rescode = response.getcode() # http 응답코드

    if rescode == 200:
        response_body = response.read()
        json_data = json.loads(response_body.decode('utf-8')) # json 데이터 읽기
        return json_data['message']['result']['translatedText']
    else:
        return "Error Code:" + rescode

def en_to_ko(english):
    client_id = "Yf8pIXHfziTxI7Noq45o" # api 호출을 위한 아이디 비번
    client_secret = "367NI3T0ES"

    encText = urllib.parse.quote(english)
    data = "source=en&target=ko&text=" + encText # http 요청에 보낼 내용
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url) # http 요청 생성
    request.add_header("X-Naver-Client-Id", client_id) # 헤더에 아이디 비번 추가
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8")) # 응답 받아옴
    rescode = response.getcode() # http 응답코드

    if rescode == 200:
        response_body = response.read()
        json_data = json.loads(response_body.decode('utf-8')) # json 데이터 읽기
        return json_data['message']['result']['translatedText']
    else:
        return "Error Code:" + rescode