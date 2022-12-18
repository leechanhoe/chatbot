import re
from nltk.corpus import wordnet
from itertools import combinations
import translate
import sys
import data

list_words = ['restaurant', 'hello', 'recommendation', 'suggestion', 'eat', 'what', 'any', 'anywhere']
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
    keywords['인사']=[]
    for synonym in list(list_syn['hello']):
        keywords['인사'].append('.*\\b'+synonym+'\\b.*')

    keywords['추천']=[]
    for synonym in list(list_syn['recommendation']):
        keywords['추천'].append('.*\\b'+synonym+'\\b.*')
    keywords['추천'].append('.*\\b'+'recommend'+'\\b.*')

    keywords['맛집']=[]
    for synonym in list(list_syn['restaurant']):
        keywords['맛집'].append('.*\\b'+synonym+'\\b.*')
    for synonym in list(list_syn['eat']):
        keywords['맛집'].append('.*\\b'+synonym+'\\b.*')
    keywords['맛집'].append('.*\\b'+'restaurants'+'\\b.*')
    keywords['맛집'].append('.*\\b'+'eat'+'\\b.*')
    keywords['맛집'].append('.*\\b'+'drink'+'\\b.*')

    keywords['아무거나']=[]
    for synonym in list(list_syn['any']):
        keywords['아무거나'].append('.*\\b'+synonym+'\\b.*')
    for synonym in list(list_syn['anywhere']):
        keywords['아무거나'].append('.*\\b'+synonym+'\\b.*')
    keywords['아무거나'].append('.*\\b'+'any'+'\\b.*')
    keywords['아무거나'].append('.*\\b'+'anywhere'+'\\b.*')
    keywords['아무거나'].append('.*\\b'+'anything'+'\\b.*')

    for intent, keys in keywords.items():
        keywords_dict[intent]=re.compile('|'.join(keys))

def set_response():
    global responses
    responses = { # |로 키워드 중첩가능, 사전순으로 나열해야함 -> greet|timings(O) / timings|greet (X)
        # 응답에 매개변수가 필요하면 ""처럼 빈칸으로 놓고 get_response함수에 작성
        'fallback':"죄송합니다. 이해하지 못했어요.. 다시 말씀해 주시겠어요?",
        '인사':'안녕하세요. 저는 맛봇이입니다. 어떤 맛집을 추천해드릴까요?',
        '지역':"",
        '음식':"",
        '맛집':'어떤 음식을 좋아하시나요?',
        '추천':'어떤 음식을 좋아하시나요?',
        '아무거나|음식':"",
        '아무거나|지역':"",
        '맛집|음식':"",
        '맛집|지역':"",
        '음식|지역':""
    }

def get_response(key, location = "", food = ""):
    global responses, intendFood, intendLocation

    if responses[key] != "":
        return responses[key]

    elif key == '지역':
        if food == "":
            return "어떤 음식을 좋아하시나요?"
        
    elif key == '음식':
        if location == "":
            return "지역도 말해주세요. 시,군,구,동을 붙이면 더 정확합니다. 대학교도 잘 알고있어요."

    name, category, restaurantloc = data.searchRestaurant(location, food)
    if name == "":
        return "그런 맛집은 없는 것 같아요.."

    intendFood = ""
    intendLocation = ""
    if location == "":
        return f'우리나라의 유명한 {food} 맛집은 <a href="http://search.naver.com/search.naver?query={name}" target="_blank" style="color:blue; text-decoration : underline;">{name}</a>!<br><br>분류 : {category}<br><br>{restaurantloc} 에 있습니다.'
    
    return f'{location}에 가면 무조건 들러야 할 {food} 맛집은 <a href="http://search.naver.com/search.naver?query={name}" target="_blank" style="color:blue; text-decoration : underline;">{name}</a>!<br><br>분류 : {category}<br><br>{restaurantloc} 에 있습니다.'

intendLocation = ""
intendFood = ""
def pick_response(user_input): # 키워드에 따른 의도 파악 & 의도에 따른 응답 생성
    matched_intents = set()

    global intendLocation, intendFood
    locations = data.getLocations() # 사용자 입력에 음식이 들어갔나 확인용 음식 데이터 불러오기
    for location in locations:
        if location in user_input:
            print("지역 :", location)
            intendLocation = location
            matched_intents.add('지역')
            break

    foods = data.getFoods() # 사용자 입력에 음식이 들어갔나 확인용 음식 데이터 불러오기
    for food in foods:
        if food in user_input:
            print("음식 :", food)
            intendFood = food
            matched_intents.add('음식')
            break

    user_input = translate.ko_to_en(user_input).lower() # 일단 wordnet이 영어라 영어로 번역
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
    print("사용자의 의도 :", matched_intents)
    response = get_response(key, intendLocation, intendFood)
    return response

def main(): # 터미널용 실행함수 (웹을 이용할때는 사용x)
    set_keyword() # 키워드 목록 작성
    set_intent_dictionary() # 의도 사전 작성
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