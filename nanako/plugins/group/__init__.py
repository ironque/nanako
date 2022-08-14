from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot import on_message
from nonebot.plugin.on import on_command
import ast
test = on_command('test')


@test.handle()
async def _(bot: Bot, event: Event):
    # call_api的写法一
    data = await bot.call_api('get_group_info', **{
        'group_id': 783088390
    })
    # 对json进行转义
    data = ast.literal_eval(str(data))
    msg = f"群号  ：{data['group_id']}\
          \n群名称：{data['group_name']}\
          \n成员数：{data['member_count']}"
    # call_api的写法二
    await bot.send(
        event=event,
        message=msg
    )
    # 不过，这里更推荐直接用响应器的send方法
    # await test.send(msg)
