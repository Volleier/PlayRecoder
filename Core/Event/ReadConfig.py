import configparser
import os

# 读取配置文件
def read_config(section, key):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '../../app.config'))
    return config[section][key]