import json
import random
import time
from typing import List, Dict

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message

BOT_NAME = "七七子"
__plugin_info__ = {
    "name": "答案之书",
    "des": "通过马纳姆效应解决历史难题",
    "usage": {
        f"{BOT_NAME}，……": "告诉你如何解决",
    },
    "author": "ironque",
    "version": "1.0",
    "permission": 50,
}

AnswerBook = on_command(f"{BOT_NAME}，", aliases={f"{BOT_NAME} ", f"{BOT_NAME},", f"{BOT_NAME}.", f"{BOT_NAME}。"},
                        permission=GROUP, block=True,
                        priority=50)


@AnswerBook.handle()
async def handle_receive(bot: Bot, event: MessageEvent):
    with open(f"nanako/plugins/answerbook/atri.json", "r", encoding="utf-8") as file:
        data: List[Dict[str, str]] = json.load(file)
    s = random.Random()
    s.seed(time.localtime())
    index = s.randint(0, 941)
    answer_string = data[index]["s"]
    await bot.send(event, Message(Message(f"[CQ:reply,id={event.message_id}]{answer_string}")))