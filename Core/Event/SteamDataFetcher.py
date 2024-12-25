import requests
from datetime import datetime
import sqlite3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Core.Event.Logger import logger
from Core.Event.ReadConfig import read_config

# 从配置文件中获取Steam API密钥和用户ID
api_key = read_config('steam', 'api_key')
user_id = read_config('steam', 'user_id')

def get_owned_games(api_key, user_id):
    logger.info("获取拥有的游戏列表")
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={user_id}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        games = data.get('response', {}).get('games', [])
        
        # 创建新的数据库连接
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../../GameDB.db'))
        c = conn.cursor()
        
        # 创建表
        c.execute('''CREATE TABLE IF NOT EXISTS games
                     (appid INTEGER PRIMARY KEY, name TEXT, playtime_forever INTEGER)''')
        logger.info("数据库连接已创建并初始化表格")
        
        for game in games:
            appid = game.get('appid')
            name = str(appid)  # 将游戏名换为游戏ID
            playtime_forever = game.get('playtime_forever')
            c.execute('''INSERT OR REPLACE INTO games (appid, name, playtime_forever)
                         VALUES (?, ?, ?)''', (appid, name, playtime_forever))
        conn.commit()
        conn.close()
        logger.info("游戏数据已插入数据库")
    else:
        logger.error(f"请求失败，状态码: {response.status_code}")
