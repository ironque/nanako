from nonebot.log import logger, default_format
import time


def savelog():
    time_str = time.strftime("%Y%m%d")
    name = "log" + time_str + ".log"
    logger.add(name, level="INFO", format=default_format, rotation="1 day")
