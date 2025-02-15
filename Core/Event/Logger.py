import logging
import os
from datetime import datetime


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        log_dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))), 'log')
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("")
        file_handler = logging.FileHandler(os.path.join(
            log_dir, f"app_{timestamp}.log"), encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)


logger = Logger().logger
