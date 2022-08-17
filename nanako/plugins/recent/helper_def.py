import re
import time
from nonebot.adapters.onebot.v11.message import Message
import httpx
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent
from nonebot.plugin import on_command
from nonebot.params import CommandArg


def get_account(id_string: str):
    account = ""
    for i in id_string:
        if i.isdigit():
            account += i
        elif i == 'd':
            break
    return account


def today():
    time_str = time.strftime("%Y%m%d") + "\n"
    return time_str


def convert_to_ans(data: list[dict]):
    result = today()  # 时间
    for ship in data:
        temp = ""
        temp += "\t" + ship['shipInfo']['shipInfo']['nameCn'] + ' :\n'  # 船名
        temp += "场数: " + str(ship['shipInfo']['battles']) + '\t\t\t\t\t胜率: ' + str(
            ship['shipInfo']['wins']) + "%\n"
        temp += "Pr: " + str(ship['shipInfo']['pr']['value']) + "\t伤害:" + str(ship['shipInfo']['damage']) + '\t' + \
                str(ship['shipInfo']['pr']['name']) + '\n'
        if ship['shipInfo']['battles'] != 0:
            result += temp
    return result


def account_get(event: MessageEvent, args: Message = CommandArg()) -> int:
    try:
        message = event.raw_message
        pattern = re.compile(r"\[CQ:at,qq=(.+?)\]")
        accountID = int(pattern.findall(message)[0])  # accountID
    except Exception:
        plain_text = args.extract_plain_text()
        if plain_text == "" or len(plain_text) < 7:
            accountID = int(event.get_user_id())
        else:
            accountID = int(get_account(plain_text))
    return accountID


def day_get(event: MessageEvent, args: Message = CommandArg()) -> int:
    try:
        message = event.raw_message
        pattern = re.compile(r'(?:d)\d+\.?\d*')
        day = int(pattern.findall(message)[0][1:])  # day
    except Exception:
        day = 0
    return day
