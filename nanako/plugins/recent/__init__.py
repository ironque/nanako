import ast
import time

import httpx
import nonebot
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.plugin import on_command

# env.globals.update(set_damageColor=set_damageColor, set_winColor=set_winColor, set_upinfo_color=set_upinfo_color,
#                    time=time, int=int, abs=abs, enumerate=enumerate)


headers = {
    'Authorization': "2148094154:EeROi2gN1dyeACPBNMSuBfnYllDsYSRqybIeNss",
}

wws_recent_30 = on_command('wws', priority=50)


@wws_recent_30.handle()
async def _(bot: Bot, event: Event):
    accountID = int(event.get_user_id())
    # data = await httpx.AsyncClient(headers=headers)
    params, day = None, 0
    params = {
        "server": "QQ",
        "accountId": accountID,
        "day": day,
        "status": 0
    }
    async with httpx.AsyncClient(headers=headers) as client:
        url = "https://api.wows.shinoaki.com//api/wows/recent/v2/recent/info"
        resp = await client.get(url, params=params, timeout=None)
        print(resp.json()['code'] )
        if resp.json()['code'] != 200:
            ans = f"[CQ:at,qq={accountID}]该日期未找到游戏记录"
        else :
            data = resp.json()['data']['shipData'][0]['shipData']
        # ans = ast.literal_eval(str(data))
            ans = convert_to_ans(data)
            ans = f"[CQ:at,qq={accountID}]\t\t\t" + ans
    # print(data)
    # print(type(ans))
    await bot.send(event, ans)


# https://api.wows.shinoaki.com/public/wows/account/recent/list?accountId=879157739&server=QQ

def today():
    time_str = time.strftime("%Y%m%d") + "\n"
    return time_str


def convert_to_ans(data: list[dict]):
    battles = 0
    result = today()  # 时间
    for ship in data:
        battles += ship['shipInfo']['battles']
        result += "\t" + ship['shipInfo']['shipInfo']['nameCn'] + ' :\n'  # 船名
        result += "场数: " + str(ship['shipInfo']['battles']) + '\t\t\t\t\t胜率: ' + str(
            ship['shipInfo']['wins']) + "%\n"
        result += "Pr: " + str(ship['shipInfo']['pr']['value']) + "\t伤害:" + str(ship['shipInfo']['damage']) + '\t' + \
                  ship['shipInfo']['pr']['name'] + '\n'

    return result
