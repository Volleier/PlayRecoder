import os
import seaborn as sns
import matplotlib.pyplot as plt


def calculate_game_statistics(games):
    total_playtime = sum(game['playtime_forever']
                         for game in games if game['playtime_forever'] > 0)
    significant_games = [
        game for game in games if game['playtime_forever'] / total_playtime > 0.05]

    return significant_games


def plot_game_statistics(games):
    names = [game['name'] for game in games]
    playtimes = [game['playtime_forever'] for game in games]

    plt.figure(figsize=(10, 5))
    sns.barplot(x=names, y=playtimes, palette='Blues_d')
    plt.xlabel('Games')
    plt.ylabel('Playtime (minutes)')
    plt.title('Significant Games Playtime')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as a static image
    plot_path = os.path.join(os.path.dirname(
        __file__), '../../Template/static/images/game_statistics.png')
    plt.savefig(plot_path)
    plt.close()

    return plot_path
