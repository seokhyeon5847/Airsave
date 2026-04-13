from flask import Flask, render_template, request, jsonify
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import os

app = Flask(__name__)

# 1. 공항 데이터 로드
try:
    locations_df = pd.read_csv('locations.csv')
except Exception as e:
    print(f"데이터 파일을 찾을 수 없습니다: {e}")
    locations_df = pd.DataFrame()

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
    # 드롭다운 메뉴에 표시할 공항 목록 전달
    airports = locations_df['name'].tolist() if not locations_df.empty else []
    return render_template('index.html', airports=airports)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    origin_name = data.get('origin')
    dest_name = data.get('destination')

    try:
        # 출발지/도착지 좌표 찾기
        origin = locations_df[locations_df['name'] == origin_name].iloc[0]
        dest = locations_df[locations_df['name'] == dest_name].iloc[0]

        # 거리 계산
        distance = haversine(origin['longitude'], origin['latitude'], 
                             dest['longitude'], dest['latitude'])

        # 예시: 거리당 유류할증료 계산 로직 (기장님의 기준에 맞춰 수정 가능)
        fuel_surcharge = round(distance * 0.15, -1) # km당 15원 예시

        return jsonify({
            "status": "success",
            "distance": f"{round(distance, 2)} km",
            "fuel_surcharge": f"{int(fuel_surcharge):,} 원"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": "계산 중 오류가 발생했습니다."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
