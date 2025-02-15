from flask import Flask, request, jsonify, render_template, redirect, url_for
import webbrowser
from threading import Timer
import os
import configparser
from Core.Event.Facade import steam_facade


class Server:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Server, cls).__new__(cls, *args, **kwargs)
            cls._instance.app = Flask(
                __name__, template_folder='UI/templates', static_folder='UI/static')
        return cls._instance

    def config_exists(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'app.config'))
        return 'steam' in config and config['steam'].get('api_key') and config['steam'].get('user_id')

    def run(self):
        app = self.app

        @app.route('/')
        def index():
            if self.config_exists():
                api_key = steam_facade.read_config("steam", "api_key")
                user_id = steam_facade.read_config("steam", "user_id")
                if steam_facade.validate_steam_credentials(api_key, user_id):
                    return redirect(url_for('games'))
            return render_template('SignUP.html')

        @app.route('/save', methods=['POST'])
        def save():
            api_key = request.form['api_key']
            user_id = request.form['user_id']

            if not steam_facade.validate_steam_credentials(api_key, user_id):
                return jsonify({"message": "Invalid Steam API Key or User ID"}), 400

            steam_facade.save_steam_credentials(api_key, user_id)
            return jsonify({"message": "Steam API Key and User ID have been saved."})

        @app.route('/games')
        def games():
            try:
                games = steam_facade.fetch_owned_games()
                return render_template('games.html', games=games)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        def open_browser():
            webbrowser.open_new("http://127.0.0.1:5000")

        if __name__ == "__main__":
            Timer(1, open_browser).start()
            app.run(debug=True)


server = Server()
server.run()
