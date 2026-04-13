from flask import Flask, render_template, request, jsonify
import pandas as pd
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)

# 하버사인 공식 (거리 계산)
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 지구 반지름 (km)
    return c * r

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # 여기에 기장님의 계산 로직이 들어갑니다.
    # 일단 서버가 잘 도는지 확인하기 위한 기본 응답입니다.
    return jsonify({"status": "success", "message": "에어세이브 엔진 가동 중!"})

if __name__ == '__main__':
    app.run(debug=True)
