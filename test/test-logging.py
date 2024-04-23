# -*- coding:utf_8 -*-


import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')

#根记录器吗？级别设置为NOTSET不行，变成了默认值warning。
#刚不会有低于warning的logRecord传递给处理器handler
logger.setLevel(level=logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(level=logging.INFO)

file_handler = logging.FileHandler('log.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(level=logging.DEBUG)

logger.addHandler(handler)
logger.addHandler(file_handler)

logger.debug('Debugging')
logger.info('This is a log info')
logger.warning('Warning exists')
logger.error('this is a error')
