import configparser
import os


class ConfigReader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigReader, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.config = configparser.ConfigParser()
            cls._instance.config.read(os.path.join(
                os.path.dirname(__file__), '../../app.config'))
        return cls._instance

    def read_config(self, section, key):
        return self.config[section][key]


config_reader = ConfigReader()


def read_config(section, key):
    return config_reader.read_config(section, key)
