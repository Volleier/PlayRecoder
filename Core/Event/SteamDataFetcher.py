import requests
import sqlite3
import configparser
import os
from .Logger import logger


class SteamDataFetcher:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SteamDataFetcher, cls).__new__(
                cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(
            os.path.dirname(__file__), '../../app.config'))
        self.STEAM_API_KEY = config['steam']['api_key']
        self.STEAM_USER_ID = config['steam']['user_id']
        self.conn = sqlite3.connect(os.path.join(
            os.path.dirname(__file__), '../steam_games.db'))
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS games
                          (appid INTEGER PRIMARY KEY, name TEXT, playtime_forever INTEGER)''')
        logger.info("数据库连接已创建并初始化表格")

    def get_owned_games(self, api_key, user_id):
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


steam_data_fetcher = SteamDataFetcher()


def get_owned_games(api_key, user_id):
    return steam_data_fetcher.get_owned_games(api_key, user_id)
