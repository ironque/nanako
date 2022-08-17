from nanako.plugins.recent.helper_def import get_account, convert_to_ans, day_get, account_get
from nonebot.adapters.onebot.v11.message import Message
import httpx
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nanako.plugins.recent.token import token


headers = {
    'Authorization': "",  # 请从benxin开发者群获取token
}

headers['Authorization'] = token
wws_recent_30 = on_command('ww', priority=50)


@wws_recent_30.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    params, day = None, 0
    accountID = account_get(event, args)
    day = day_get(event, args)
    params = {
        "server": "QQ",
        "accountId": accountID,
        "day": day,
        "status": 0
    }
    async with httpx.AsyncClient(headers=headers) as client:
        url = "https://api.wows.shinoaki.com//api/wows/recent/v2/recent/info"
        resp = await client.get(url, params=params, timeout=None)
        print(resp.json()['code'])
        if resp.json()['code'] != 200:
            ans = f"[CQ:at,qq={accountID}]该日期未找到游戏记录"
        else:
            data = resp.json()['data']['shipData'][0]['shipData']
            ans = convert_to_ans(data)
            ans = f"[CQ:at,qq={accountID}]\t\t\t" + ans
    await bot.send(event, ans)
