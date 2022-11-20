import re
from nltk.corpus import wordnet
from itertools import combinations
import translate
import sys

'''
아직 챗봇 주제는 미정
일단 예제 데이터대로 챗봇에게 안녕이나 시간 이라고 말해보면 의도에 대답해줌
'''


list_words = ['hello','timings', 'hi']
list_syn={}
def set_keyword(): # 키워드 목록 작성
    for word in list_words:
        synonyms=[]
        for syn in wordnet.synsets(word):
            for lem in syn.lemmas():
                # Remove any special characters from synonym strings
                lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
                synonyms.append(lem_name)
        list_syn[word]=set(synonyms)


# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={} # 경합 집합
def set_intent_dictionary(): # 의도 사전 작성
    keywords['greet']=[]
    for synonym in list(list_syn['hello']):
        keywords['greet'].append('.*\\b'+synonym+'\\b.*')

    keywords['timings']=[]
    for synonym in list(list_syn['timings']):
        keywords['timings'].append('.*\\b'+synonym+'\\b.*')

    for intent, keys in keywords.items():
        keywords_dict[intent]=re.compile('|'.join(keys))


responses = {}
def set_response(): # 응답 사전 작성
    global responses
    responses = { # |로 키워드 중첩가능, 사전순으로 나열해야함 -> greet|timings(O) / timings|greet (X)
        #
        'greet':'Hello! How can I help you?',
        'timings':'We are open from 9AM to 5PM, Monday to Friday. We are closed on weekends and public holidays.',
        'fallback':'I dont quite understand. Could you repeat that?',
        'greet|timings': 'greet, timings',
    }


def pick_response(user_input): # 키워드에 따른 의도 파악 & 의도에 따른 응답 생성
    user_input = translate.ko_to_en(user_input).lower() # 일단 wordnet이 영어라 영어로 번역
    matched_intents = set()
    for intent, pattern in keywords_dict.items(): # 의도에 맞는 키워드가 있으면 추가
        if re.search(pattern, user_input):
            matched_intents.add(intent)

    key ='fallback' # 의도를 찾지 못할 경우를 위한 디폴트 설정
    matched_intents = sorted(list(matched_intents)) # 사용자 입력에서 찾아낸 의도들을 조합돌림
    for i in range(len(matched_intents), 0, -1): # 의도를 여러개 결합해 자세한 의도부터 찾기 위함
        for intent in combinations(matched_intents, i): # 예를들어 사용자 입력에서 '서울, 관광지' 키워드를 찾으면
            intent = '|'.join(intent) # '서울' 이나 '관광지' 보다 '서울|관광지' 이렇게 조합된 것을 우선 찾기 위함
            if intent in responses:
                key = intent
                break

        if key != 'fallback':
            break

    response = translate.en_to_ko(responses[key]) # 한국어로 번역해서 반환
    return response

def main(): # 터미널용 실행함수 (웹을 이용할때는 사용x)
    set_keyword() # 키워드 목록 작성
    set_intent_dictionary() # 의도 사전 작성
    set_response() # 응답 사전 작성
    print ('\n' + translate.en_to_ko("Welcome to MyBank. How may I help you?"))
    while (1):  
        user_input = translate.ko_to_en(input()).lower() # 영어로 번역
        if user_input == 'quit': 
            print(translate.en_to_ko("Thank you for using."))
            break

    print(pick_response(user_input))

    
set_keyword() # 키워드 목록 작성
set_intent_dictionary() # 의도 사전 작성
set_response() # 응답 사전 작성