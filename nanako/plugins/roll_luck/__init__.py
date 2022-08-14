import random
from datetime import date
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message


def luck_define(num):
    if num < 18:
        return '大吉'
    elif num < 53:
        return '吉'
    elif num < 58:
        return '半吉'
    elif num < 62:
        return '小吉'
    elif num < 65:
        return '末小吉'
    elif num < 71:
        return '末吉'
    else:
        return '凶'


luck_roll = on_keyword({'luck', '运势'}, priority=50)


@luck_roll.handle()
async def luck_roll_handle(bot: Bot, event: Event):
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    luck = rnd.randint(1, 100)
    await luck_roll.finish(Message(f'[CQ:at,qq={event.get_user_id()}]您今天的运势为"{luck_define(luck)}"'))
