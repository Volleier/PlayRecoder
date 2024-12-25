import sqlite3
import os

def fetch_Games():
    # 链接数据库
    db_path = os.path.join(os.path.dirname(__file__), '../../GameDB.db')
    conn = sqlite3.connect(db_path)
    return conn

def sort_games_by_time():
    conn = fetch_Games()
    cursor = conn.cursor()
    # 获取游戏数据，按照从高到低的方式排列
    query = """
    SELECT name, playtime_forever
    FROM games
    ORDER BY playtime_forever DESC
    """
    
    cursor.execute(query)
    games = cursor.fetchall()

    conn.close()

    return games