import requests
from datetime import datetime
import sqlite3
import configparser
import os
from .Logger import logger  # 使用相对导入

# 读取配置文件
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../app.config'))

# 从配置文件中获取Steam API密钥和用户ID
STEAM_API_KEY = config['steam']['api_key']
STEAM_USER_ID = config['steam']['user_id']

# 创建数据库连接
conn = sqlite3.connect(os.path.join(
    os.path.dirname(__file__), '../steam_games.db'))
c = conn.cursor()

# 创建表
c.execute('''CREATE TABLE IF NOT EXISTS games
             (appid INTEGER PRIMARY KEY, name TEXT, playtime_forever INTEGER)''')

logger.info("数据库连接已创建并初始化表格")


def get_owned_games(api_key, user_id):
    logger.info("获取拥有的游戏列表")
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={
        api_key}&steamid={user_id}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        games = data.get('response', {}).get('games', [])
        logger.info(f"获取到的游戏数量: {len(games)}")
        return games
    else:
        logger.error(f"请求失败，状态码: {response.status_code}")
        return None
