from flask import Flask, render_template, request, jsonify
import chatbot
import datetime
import translate
app = Flask(__name__)

'''
실행법 : server.py를 실행 후 크롬 주소창에 127.0.0.1:5000입력
'''

@app.route('/') # '/' == 'index.html'
def index():
    today = translate.en_to_ko(datetime.date.today().strftime('%A %B %d, %Y')) # 날짜 데이터 보내주기
    time = datetime.datetime.now().strftime('%p %I:%M')
    return render_template('index.html', today=today, time=time) # 채팅창 랜더링

@app.route('/data', methods = ['POST']) # 
def data():
    req = request.get_json() # 요청에 사용자 입력에서 값을 가져옴
    text = req['data']
    print("사용자 입력 :",text)
    response = chatbot.pick_response(text) # 사용자 입력에 대한 챗봇의 응답
    print("챗봇 응답 : ",response)
    time = datetime.datetime.now().strftime('%p %I:%M')
    data = {'chatbotText' : response, 'time' : time}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)