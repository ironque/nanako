from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11.permission import GROUP_MEMBER, GROUP_OWNER
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import nonebot

tie_tie = on_command('贴贴',
                     aliases={'mua'},
                     permission=GROUP_OWNER | GROUP_MEMBER,
                     priority=50)


@tie_tie.handle()
async def _(bot: Bot, event: Event):
    msg_1 = Message(f'[CQ:at,qq={event.get_user_id()}]')
    # msg_2 = Message('贴贴')
    msg_3 = str(event.get_message())
    # nonebot.logger.debug(str(event.get_message()))
    await bot.send(event=event, message=msg_1 + msg_3)
    # await tie_tie.finish(msg_1+msg_2)
