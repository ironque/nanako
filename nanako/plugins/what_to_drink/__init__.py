import ast

import nonebot
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.plugin import on_command
from random import choice

drink = {
    "pepsi": {
        "可乐", "佳得乐", "美年达", "七喜", "果缤纷", "bubly微笑趣泡",
    },
    "coca-cola": {
        "雪菲力盐汽水", "可乐", "雪碧", "怡泉", "芬达", "酷儿",
    },
    "农夫山泉": {
        "东方树叶", "NFC果汁", "苏打水", "水溶C100", "茶Π", "Vitamin", "尖叫", "炭仌咖啡", "汽茶",
    },
    "康师傅": {
        "冰红茶", "酸梅汤", "绿茶", "金桔柠檬", "蜜桃乌龙茶", "茉莉清茶", "茉莉绿茶", "冰糖雪梨", "蜂蜜柚子",
        "青梅绿茶", "贝纳斯咖啡拿铁", "小酪多多",
    },
    "统一": {
        "阿萨姆奶茶", "绿茶", "冰红茶", "鲜橙多", "青梅绿茶", "番茄汁", "海之言", "雅哈冰咖啡", "冰糖雪梨", "小茗同学",
        "水趣多", "仙草凉茶",
    },
    "维他奶": {
        "柠檬茶", "豆奶", "果泡茶", "蜜桃茶",
    },
    "哇哈哈": {
        "AD钙", "爽歪歪", "乳酸菌", "营养快线",
    },
    "Others": {
        "元气森林气泡水", "醇香燃茶", "雀巢咖啡", "营养快线", "王老吉",
    }
}

drink_what = on_command("喝啥", priority=50)


@drink_what.handle()
async def _(bot: Bot, event: Event):
    brand = choice(list(drink.keys()))
    drk = choice(list(drink[brand]))
    msg = str(brand) + "->" + str(drk)
    await bot.call_api('send_msg', **{
        "user_id": str(event.get_user_id()),
        "message": msg,
        "message_type": "group",
        "group_id": str(event.group_id)
    })


