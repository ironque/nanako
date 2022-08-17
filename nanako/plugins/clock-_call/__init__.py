import time
from nonebot.plugin import on_message

def int_clock(local_time: time.struct_time):
    if local_time.tm_min==0 and local_time.tm_sec==0:
        return True
    else:
        return False


message=on_message(rule=int_clock(time.localtime()))


