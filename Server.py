from flask import Flask, request, jsonify, render_template, redirect, url_for
import webbrowser
from threading import Timer
import configparser
import os
import requests
from Core.Event.Logger import logger
from Core.Event.SteamDataFetcher import get_owned_games
from Core.Event.ReadConfig import read_config

app = Flask(__name__, template_folder='UI', static_folder='UI')


def config_exists():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'app.config'))
    return 'steam' in config and config['steam'].get('api_key') and config['steam'].get('user_id')


def validate_steam_credentials(api_key, user_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={
        api_key}&steamid={user_id}&format=json"
    response = requests.get(url)
    return response.status_code == 200


@app.route('/')
def index():
    if config_exists():
        return redirect(url_for('games'))
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save():
    api_key = request.form['api_key']
    user_id = request.form['user_id']

    if not validate_steam_credentials(api_key, user_id):
        return jsonify({"message": "Invalid Steam API Key or User ID"}), 400

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'app.config'))
    if 'steam' not in config.sections():
        config.add_section('steam')
    config.set('steam', 'api_key', api_key)
    config.set('steam', 'user_id', user_id)

    with open(os.path.join(os.path.dirname(__file__), 'app.config'), 'w') as configfile:
        config.write(configfile)

    logger.info("Steam API Key and User ID have been saved.")
    return jsonify({"message": "Steam API Key and User ID have been saved."})


@app.route('/games')
def games():
    api_key = read_config("steam", "api_key")
    user_id = read_config("steam", "user_id")

    try:
        logger.info("开始获取游戏列表")
        games = get_owned_games(api_key, user_id)
        logger.info(f"获取到的游戏列表: {games}")
        return render_template('games.html', games=games)
    except Exception as e:
        logger.error(f"获取游戏列表失败: {e}")
        return jsonify({"error": str(e)}), 500


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)
