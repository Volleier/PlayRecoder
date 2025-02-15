import ast
import matplotlib.pyplot as plt

# 读取 temp.txt 文件内容
file_path = ''
games_data = []

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read().replace('获取到的游戏列表: ', '')
    games_data = ast.literal_eval(content)

games = []
durations = []

for game in games_data:
    appid = game['appid']
    duration = game['playtime_forever']
    if duration > 0:
        games.append(appid)
        durations.append(duration)

# 计算总时长
total_duration = sum(durations)

# 筛选出占总游戏时长不小于3%的游戏
filtered_games = []
filtered_durations = []

for game, duration in zip(games, durations):
    if duration / total_duration >= 0.03:
        filtered_games.append(game)
        filtered_durations.append(duration)

# 绘制饼图
plt.figure(figsize=(10, 7))
plt.pie(filtered_durations, labels=filtered_games,
        autopct='%1.1f%%', startangle=140)
plt.title('Distribution of game duration')
plt.axis('equal')  # 保证饼图是一个正圆
plt.show()
