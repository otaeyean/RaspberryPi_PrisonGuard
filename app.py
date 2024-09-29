from flask import Flask, render_template, request
app = Flask(__name__)

# 자바스크립트 코드나 이미지 파일 등에 대해
# 브라우저에게 캐시에 저장한 파일을 사용하지 않도록 지시
app.config['SEND_FILE_MAX_AGE_DEFAULT']=0

@app.route('/')
def index():
        return render_template('hw5viewer.html')

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080, debug=True)

3. cctv , 온도, 습도, 조도그래프,등 출력하는 웹 페이지
