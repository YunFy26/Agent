import logging


# TODO：记录程序运行日志
logger = logging.getLogger(__name__)

# 设置日志记录器的日志级别
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器对象，将日志写入文件
file_handler = logging.FileHandler('app.log')

# 创建一个日志格式化器对象
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将格式化器添加到文件处理器
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)