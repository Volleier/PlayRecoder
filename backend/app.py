from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 允许跨域请求

STEAM_API_KEY = ''

@app.route('/api/games/<steam_id>', methods=['GET'])
def get_games(steam_id):
    # 调用 Steam API 获取用户游戏数据
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json'
    response = requests.get(url)
    
    # 检查响应状态码
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Steam API'}), response.status_code
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON response from Steam API'}), 500
    
    return jsonify(data)

@app.route('/')
def index():
    return "Welcome to the PlayRecoder API!"

if __name__ == '__main__':
    app.run(debug=True)
