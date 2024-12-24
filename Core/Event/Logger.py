import logging
import os
from datetime import datetime

# 获取当前时间戳
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# 创建日志目录
log_dir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), 'log')
os.makedirs(log_dir, exist_ok=True)

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("")
file_handler = logging.FileHandler(os.path.join(
    log_dir, f"app_{timestamp}.log"), encoding="utf-8")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
