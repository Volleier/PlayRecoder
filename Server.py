from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import configparser
import requests
import logging
import webbrowser
from threading import Timer
from Core.Event.Logger import logger
from Core.Event.SteamDataFetcher import get_owned_games

app = Flask(__name__, template_folder='UI', static_folder='UI')

# 配置日志记录
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(message)s')

def config_exists():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'app.config'))
    return 'steam' in config and config['steam'].get('api_key') and config['steam'].get('user_id')

def read_config(section, key):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'app.config'))
    return config.get(section, key)

def validate_steam_credentials(api_key, user_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={user_id}&format=json"
    response = requests.get(url)
    
    # 记录请求的 URL 和响应状态码
    logging.info(f"Request URL: {url}")
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Content: {response.content}")
    
    if response.status_code == 401:
        logging.error("Unauthorized: Invalid API Key or Steam ID")
    
    return response.status_code == 200

@app.route('/')
def index():
    api_key = ''
    user_id = ''
    if config_exists():
        api_key = read_config('steam', 'api_key')
        user_id = read_config('steam', 'user_id')

    return render_template('SignUP.html', api_key=api_key, user_id=user_id)

@app.route('/save', methods=['POST'])
def save():
    api_key = request.form.get('api_key')
    user_id = request.form.get('user_id')

    # 打印接收到的数据
    logging.info(f"Received data: api_key={api_key}, user_id={user_id}")

    if not api_key or not user_id:
        return jsonify({"message": "API Key and User ID are required"}), 400

    if not validate_steam_credentials(api_key, user_id):
        return jsonify({"message": "Invalid Steam API Key or User ID"}), 401

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'app.config'))
    if 'steam' not in config.sections():
        config.add_section('steam')
    config.set('steam', 'api_key', api_key)
    config.set('steam', 'user_id', user_id)

    with open(os.path.join(os.path.dirname(__file__), 'app.config'), 'w') as configfile:
        config.write(configfile)

    logging.info("Steam API Key and User ID have been saved.")
    return jsonify({"message": "Steam API Key and User ID have been saved.", "redirect": url_for('games')})

@app.route('/games')
def games():
    api_key = read_config("steam", "api_key")
    user_id = read_config("steam", "user_id")
    games = get_owned_games(api_key, user_id)
    logging.info(f"获取到的游戏列表: {games}")
    return render_template('MainWindow.html', games=games)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=False)
