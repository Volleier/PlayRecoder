from .Logger import logger
from .ReadConfig import read_config
from .SteamDataFetcher import get_owned_games


class SteamFacade:
    def __init__(self):
        self.logger = logger
        self.read_config = read_config
        self.get_owned_games = get_owned_games

    def validate_steam_credentials(self, api_key, user_id):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={
            api_key}&steamid={user_id}&format=json"
        response = requests.get(url)
        return response.status_code == 200

    def save_steam_credentials(self, api_key, user_id):
        config = configparser.ConfigParser()
        config.read(os.path.join(
            os.path.dirname(__file__), '../../app.config'))
        if 'steam' not in config.sections():
            config.add_section('steam')
        config.set('steam', 'api_key', api_key)
        config.set('steam', 'user_id', user_id)
        with open(os.path.join(os.path.dirname(__file__), '../../app.config'), 'w') as configfile:
            config.write(configfile)
        self.logger.info("Steam API Key and User ID have been saved.")

    def fetch_owned_games(self):
        api_key = self.read_config("steam", "api_key")
        user_id = self.read_config("steam", "user_id")
        try:
            self.logger.info("开始获取游戏列表")
            games = self.get_owned_games(api_key, user_id)
            self.logger.info(f"获取到的游戏列表: {games}")
            return games
        except Exception as e:
            self.logger.error(f"获取游戏列表失败: {e}")
            raise e


steam_facade = SteamFacade()
