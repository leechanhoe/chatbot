# 맛집 추천 챗봇

2022년 2학기 인공지능개론 팀 과제인 챗봇 개발입니다.

<br>

**사용기술 : Flask, AJAX, Html, Css, JavaScript, 네이버 검색 API, 네이버 파파고 API**

<br>
<br>
<br>

## 주요 개발 내용

### 1. 파파고 API를 활용한 번역
교수님께서 예제로 주신 코드를 기반으로 개발을 진행했습니다. 하지만, 예제에 있는 `wordnet` 유의어 모듈은 한글을 지원하지 않기 때문에 번역을 하거나 한국어 자연어 처리 라이브러리인 `KONLPY`를 사용해야 했습니다.

해결책으로 네이버 파파고 API를 사용했습니다. 사용자 입력을 영어로 번역하여 그 결과에 `wordnet`을 적용할 수 있었습니다.

<br>

### 2. 사용자 인터페이스 개발
백엔드 개발을 목표로 하고 있는 제가 가장 흥미를 느낄 수 있었던 부분입니다. 개강 전 열심히 공부했던 내용이 과연 어떻게 도움이 될지 궁금했습니다.

사용자 인터페이스는 정해진 것은 아니지만, 팀 수준에 맞게 터미널, 웹, 앱 등을 활용해야 했습니다. 어떻게 할 지 고민하다 7달전 html과 css 공부를 할 때 [카카오톡 클론코딩](https://github.com/leechanhoe/kokoa-clone-2020)을 했던 것이 생각나 그 화면을 활용하기로 했습니다.

<img width=300 src="https://github.com/user-attachments/assets/50184b55-ef1d-406f-b8ff-cb129032af7f">


위와 같은 화면입니다.

화면 개발을 하며 이전에 배웠던 HTML, CSS, Javascript등의 개념을 복습할 수 있었습니다.

<br>

#### ● 어려웠던 점
가장 어려웠던 점은 **비동기 통신 구현**입니다. 입력 버튼을 누르면 `form`태그의 효과때문인지 새로고침이 되어 초기화가 되었습니다. 화면 새로고침 없이 내가 원하는 부분만 리로드 될 수 있게 만들고 싶었습니다.

JQuery와 AJAX를 활용하여 구현할 수 있었습니다. 아래는 코드의 일부입니다.

```javascript
var request = {'data':userText}; // json 형식으로 만들기
        $.ajax({ // ajax로 서버와 비동기 통신하는 코드 -> 새로고침 하지 않고 통신 가능
          type : "POST",
          url : '{{url_for("data")}}',
          dataType : "JSON", // json으로 통신
          data : JSON.stringify(request),
          contentType: "application/json",
          error : function(){
            console.log("서버와 통신 실패");
            alert('서버와 통신 실패');
          },
          success : function(response){
            console.log("서버와 통신 성공");
            console.log(time)
            time[0].innerText = response['time'];
            text[0].innerHTML = response['chatbotText'];
            ...
         
```

<br>
<br>

### 3. Flask 모듈을 활용한 간단한 서버 개발
저는 사실 개강 전 열심히 공부했던 `Spring` 프레임워크를 사용해보고 싶었지만, python으로만 개발해야 했기 때문에, `Flask`라는 
웹 프레임워크를 사용해보았습니다. 프레임워크가 달라도 근본적인 내용들은 비슷할 것이라고 생각했습니다.

실제로 개발을 해보니, Spring을 공부했던 것이 큰 도움이 되었습니다.

화면도 하나뿐인 간단한 프로젝트라 서버 개발은 아래의 코드가 전부입니다.

```python
from flask import Flask, render_template, request, jsonify
import chatbot
import datetime
import translate
from pytz import timezone

app = Flask(__name__)

@app.route('/') # '/' == 'index.html'
def index():
    today = translate.en_to_ko(datetime.date.today().strftime('%A %B %d, %Y')) # 날짜 데이터 보내주기
    time = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%p %I:%M')
    return render_template('index.html', today=today, time=time) # 채팅창 랜더링

@app.route('/data', methods = ['POST']) # 
def data():
    req = request.get_json() # 요청에 사용자 입력에서 값을 가져옴
    text = req['data']
    print("사용자 입력 :",text)

    response = chatbot.pick_response(text) # 사용자 입력에 대한 챗봇의 응답
    print("챗봇 응답 : ", response)

    time = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%p %I:%M')
    data = {'chatbotText' : response, 'time' : time}
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
```

추가로 파이썬으로 구현된 웹 어플리케이션을 웹 호스팅해주는 서비스인 `Pythonanywhere`을 통하여 배포도 할 수 있었습니다.

'서버를 이렇게 배포하는구나' 라는 것도 어느정도 알게 되었습니다.

<br>
<br>

### 4. 네이버 검색 API를 활용한 챗봇의 맛집 추천
사용자가 맛집을 추천해달라고 지역과 음식 이름을 입력하면, 네이버 검색 API를 활용하여 `지역` + `이름` + '맛집' 으로 검색된 상위 10개 식당정보를 가져옵니다. 그 정보를 활용하여 응답을 구성합니다.

<img width=300 src="https://github.com/user-attachments/assets/c2834e12-1a93-4e9b-bc03-1209a2772722">

<br>
<br>
<br>
<br>
<br>

## 프로젝트를 하며 느낀점
제가 복학 전 주로 공부했던 내용들을 실제 과제에 써볼 수 있어 이제까지 공부했던 것들이 도움이 되는 보람찬 느낌을 받았습니다.

보통 과제 하나를 할때는 많게는 3일이 걸렸는데, 이 과제는 일주일정도 시간을 들인 진심을 다한 과제였습니다. 다른 공부도 할 것이 많아 이 프로젝트에 더 시간을 투자하기 어려운게 아쉬웠습니다.

비록 매우 작지만, 드디어 한 걸음을 내딛은 느낌입니다. 이후 하게될 더 큰 프로젝트들은 더 개선된 모습을 볼 수 있을 것이라고 생각합니다.
